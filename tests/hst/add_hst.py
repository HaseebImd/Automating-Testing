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


def add_hst_for_client(page, client_name, hst_method="Monthly"):
    try:
        print("inside add_hst_for_client")
        # Ensure we are on the HST page
        page.goto(f"{base_url}/apps/hst/")
        logger.info("Navigated to HST page")

        # Use one of these options to click the "Add" button
        # Option 1: Text-based selector
        page.click('a:has-text("Add")')

        # Option 2: Class-based selector
        # page.click('a.MuiButton-containedSecondary')

        # Option 3: href attribute selector
        # page.click('a[href="/apps/hst/new/"]')

        # Option 4: XPath selector
        # page.click('//a[span[text()="Add"]]')

        # Click the client input field to trigger the dropdown
        page.click('input[id="id_client"]')

        # Wait for the dropdown list to load and become visible
        page.wait_for_selector('ul[role="listbox"]', timeout=5000)  # Adjust selector as needed

        # Now that the list is loaded, type the client name
        page.fill('input[id="id_client"]', client_name)

        # Wait briefly for the matching client name to appear
        page.wait_for_timeout(500)  # Adjust this timeout if needed

        # Select the exact match from the dropdown list
        # This assumes the client name appears in an `li` element within the dropdown
        page.click(f'ul[role="listbox"] >> text="{client_name}"')


        logger.info(f"Selected client: {client_name}")

        # Click the HST Method radio button label based on the provided method
        page.click(f'text="{hst_method}"')
        logger.info(f"HST Method selected: {hst_method}")

        start_date = "2024-01-01"  # Adjust the start date as needed
        page.fill('input[id="start_date"]', start_date)
        page.dispatch_event('input[id="start_date"]', 'input')  # Trigger input event
        logger.info(f"Start date set to: {start_date}")

        # Set End Date in YYYY-MM-DD format
        end_date = "2024-12-31"  # Adjust the end date as needed
        page.fill('input[id="end_date"]', end_date)
        page.dispatch_event('input[id="end_date"]', 'input')  # Trigger input event
        logger.info(f"End date set to: {end_date}")

        # Click on "Create" to add the HST for the client
        page.click('button:text("Create")')
        logger.info(f"HST added for client {client_name} with method {hst_method}")

    except Exception as e:
        error_logger.error(f"Error occurred while adding HST: {str(e)}", exc_info=True)
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
        add_hst_for_client(page, client_name, "Monthly")

        logger.info("HST addition completed successfully")
    except Exception as main_e:
        error_logger.error(f"Error in main function: {str(main_e)}", exc_info=True)
    finally:
        # Ensure the browser is closed regardless of success or failure
        stop_browser(browser)


if __name__ == "__main__":
    logger.info("********** HST addition Test Case **********")
    main()
