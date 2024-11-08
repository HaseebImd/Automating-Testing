import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]  # Adjust according to your structure
sys.path.append(str(project_root))
import time
from utils.logger import setup_logging
from tests.local import *
base_url = BASE_URL

# Set up logging
logger, error_logger = setup_logging()

def add_hst_for_client(page, client_name, hst_method="Monthly"):
    logger.info("********** HST addition Test Case Running **********")
    try:
        # Ensure we are on the HST page
        page.goto(f"{base_url}/apps/hst/")
        time.sleep(5)
        page.click('a:has-text("Add")')
        page.click('input[id="id_client"]')
        time.sleep(5)
        # Wait for the dropdown list to load and become visible
        page.wait_for_selector('ul[role="listbox"]', timeout=20000)  # Adjust selector as needed

        # Now that the list is loaded, type the client name
        page.fill('input[id="id_client"]', client_name)

        # Wait briefly for the matching client name to appear
        page.wait_for_timeout(500)  # Adjust this timeout if needed

        time.sleep(2)
        # Select the exact match from the dropdown list
        # This assumes the client name appears in an `li` element within the dropdown
        page.click(f'ul[role="listbox"] >> text="{client_name}"')

        # Click the HST Method radio button label based on the provided method
        page.click(f'text="{hst_method}"')

        time.sleep(1)

        start_date = time.strftime("%Y-%m-%d")  # Use the current date
        page.fill('input[id="start_date"]', start_date)
        page.dispatch_event('input[id="start_date"]', 'input')  # Trigger input event

        time.sleep(1)

        # end_date = "2024-12-31"  # Adjust the end date as needed
        # page.fill('input[id="end_date"]', end_date)
        # page.dispatch_event('input[id="end_date"]', 'input')  # Trigger input event

        time.sleep(1)

        page.click('button:text("Create")')
        logger.info(f"HST added for client {client_name} with method {hst_method}")
        logger.info("********** HST addition Test Case Passed **********")

    except Exception as e:
        logger.info("********** HST addition Test Case Failed **********")
        error_logger.error(f"Error occurred while adding HST: {str(e)}", exc_info=True)
        raise e  # Re-raise to ensure the script stops on failure
