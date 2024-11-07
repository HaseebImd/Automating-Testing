import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from pathlib import Path
import os
from dotenv import load_dotenv
from utils.logger import setup_logging
from utils.random_data import client_personal_info, client_address_info
from utils.browser import start_browser, stop_browser

# Set up logging
logger, error_logger = setup_logging()

# Load environment variables from the .env file
project_root = Path(__file__).resolve().parents[2]
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

username = os.getenv("LOGIN_USERNAME")
password = os.getenv("LOGIN_PASSWORD")
base_url = os.getenv("BASE_URL")

if not username or not password:
    raise ValueError("Username or password is not loaded correctly from the .env file")


def login(page):
    try:
        # Navigate to login page
        page.goto(f"{base_url}/sign-in")

        # Perform login
        page.fill('input[name="email"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')

        # Check if login was successful by waiting for the /apps/clients/ URL
        page.wait_for_url(f"{base_url}/apps/clients/", timeout=20000)
        logger.info("Login successful, navigated to clients page")

        # After login, navigate explicitly to the HST page
        page.goto(f"{base_url}/apps/hst/")
        logger.info("Manually navigated to HST page")
    except Exception as e:
        logger.error("Login failed - Invalid credentials or timeout", exc_info=True)
        raise e  # Re-raise the exception to handle it in the main function


def delete_hst_for_client(page, client_name):
    try:
        # Navigate to the HST page
        page.goto(f"{base_url}/apps/hst/")
        logger.info("Navigated to HST page for deletion")

        # Wait for the HST table to load and ensure rows are present
        page.wait_for_selector('table tbody tr', timeout=5000)

        # Search for the HST entry by client name
        page.fill('input[placeholder="Search HSTs"]', client_name)
        page.press('input[placeholder="Search HSTs"]', 'Enter')
        logger.info(f"Searched for client: {client_name}")

        # Wait briefly to allow the search results to load
        page.wait_for_timeout(1000)

        # Locate the first HST entry row that matches the client name
        hst_entry_row = page.locator(f'table tbody tr:has-text("{client_name}")').first

        # Hover over the located HST entry row to reveal action icons
        hst_entry_row.hover()

        # Locate the delete button within this row
        delete_icon = hst_entry_row.locator('button[title="Delete"]')  # Adjust the selector if necessary

        # Delete the HST entry if the delete icon is visible
        if delete_icon.is_visible():
            logger.info(f"Deleting HST entry for client: {client_name}")
            delete_icon.click()

            # Confirm the deletion in the confirmation dialog by clicking "Yes"
            confirmation_button = page.locator('button:has-text("Yes")')
            if confirmation_button.is_visible():
                confirmation_button.click()
                logger.info("Confirmed deletion in the dialog")

                # Wait for the deletion request to complete
                page.wait_for_timeout(2000)  # Wait to confirm the deletion takes effect

                # Verify deletion by checking the table again
                if page.locator(f'table tbody tr:has-text("{client_name}")').count() == 0:
                    logger.info(f"HST entry for client {client_name} deleted successfully from the frontend.")
                else:
                    logger.error(f"HST entry for client {client_name} is still present in the frontend.")
            else:
                logger.error("Confirmation dialog did not appear or 'Yes' button was not found.")

        else:
            logger.error(f"No delete button found for client: {client_name}")

    except Exception as e:
        error_logger.error(f"Error occurred while deleting HST: {str(e)}", exc_info=True)
        raise e  # Re-raise to ensure the script stops on failure


def main():
    # Start a browser session
    browser, page = start_browser()
    try:
        # Perform login
        login(page)
        print("login done")

        # Add HST entry for a specific client
        client_name = "[Testing]-130838-20241107-U5CKI"  # Replace with actual client name
        delete_hst_for_client(page, client_name)

        logger.info("HST addition completed successfully")
    except Exception as main_e:
        error_logger.error(f"Error in main function: {str(main_e)}", exc_info=True)
    finally:
        # Ensure the browser is closed regardless of success or failure
        stop_browser(browser)


if __name__ == "__main__":
    logger.info("********** HST Deletion Test Case **********")
    main()
