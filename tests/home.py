import sys
from pathlib import Path
from hst_tests import HST_test_cases
project_root = Path(__file__).resolve().parents[1]  # Adjust according to your structure
sys.path.append(str(project_root))
from utils.logger import setup_logging
from utils.browser import start_browser, stop_browser
import time
from client.client_creation import create_client
from local import *
# Set up logging
logger, error_logger = setup_logging()

username = LOGIN_USERNAME
password =LOGIN_PASSWORD
base_url = BASE_URL

if not username or not password:
    raise ValueError("Username or password is not loaded correctly from the .env file")


def login(page):
    logger.info("********** Trying to Login **********")
    try:
        # Navigate to login page
        page.goto(f"{base_url}/sign-in")
        time.sleep(5)

        # Perform login
        page.fill('input[name="email"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        time.sleep(5)
    except Exception as e:
        logger.error("********** Login Failed: Exception occurred **********")
        error_logger.error("Login failed - Invalid credentials or timeout", exc_info=True)
        raise e  # Re-raise the exception to handle it in the main function


def main():
    # Start a browser session
    browser, page = start_browser()
    try:
        login(page)
        client_name = create_client(page)
        HST_test_cases(page, client_name, hst_method="Monthly")
    except Exception as main_e:
        error_logger.error(f"Error in main function: {str(main_e)}", exc_info=True)
    finally:
        # Ensure the browser is closed regardless of success or failure
        stop_browser(browser)


if __name__ == "__main__":
    main()
