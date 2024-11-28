import sys
from pathlib import Path

# from hst_tests import HST_test_cases
# from payroll_tests import Payroll_test_cases
import random

project_root = Path(__file__).resolve().parents[1]  # Adjust according to your structure
sys.path.append(str(project_root))
from utils.logger import setup_logging
from utils.browser import start_browser, stop_browser
import time
from client.client_creation import create_client
from local import *
import json
from playwright.sync_api import sync_playwright

# Set up logging
logger, error_logger = setup_logging()


username = LOGIN_USERNAME
password = LOGIN_PASSWORD
base_url = BASE_URL

if not username or not password:
    raise ValueError("Username or password is not loaded correctly from the .env file")


def login(page, context):
    logger.info("********** Trying to Login **********")
    try:
        # Navigate to login page
        logger.info(f"Navigating to {base_url}/sign-in")
        page.goto(f"{base_url}/sign-in")
        page.wait_for_selector('input[name="email"]', timeout=30000)

        # Perform login
        logger.info("Filling login credentials.")
        page.fill('input[name="email"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')

        # Wait for login to complete (e.g., URL change or specific element)
        logger.info("Waiting for the login process to complete.")
        page.wait_for_url(f"{base_url}/apps/clients/", timeout=30000)
        logger.info("********** Login Successful **********")

    except Exception as e:
        logger.error("********** Login Failed: Exception occurred **********")
        error_logger.error(
            "Login failed - Invalid credentials or timeout", exc_info=True
        )
        raise e  # Re-raise the exception for handling in main()


def main():
    """Main function to orchestrate the test flow."""
    browser, context, page = start_browser()
    try:

        login(page, context)

        # Access client creation
        logger.info("Starting client creation.")
        client_name = create_client(page)
        logger.info(
            f"Client creation completed successfully. Client name: {client_name}"
        )
    except Exception as main_e:
        error_logger.error(f"Error in main function: {str(main_e)}", exc_info=True)
    finally:
        # Ensure the browser is closed regardless of success or failure
        logger.info("Closing the browser session.")
        stop_browser(browser)


if __name__ == "__main__":
    main()
