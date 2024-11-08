from time import sleep
from utils.logger import setup_logging
from tests.local import *
base_url = BASE_URL

# Set up logging
logger, error_logger = setup_logging()


def delete_hst_for_client(page, client_name):
    logger.info("********** HST Delete Test Case Running **********")
    try:
        # Navigate to the HST page
        page.goto(f"{base_url}/apps/hst/")
        logger.info("Navigated to HST page for deletion")
        sleep(5)
        # Wait for the HST table to load and ensure rows are present
        page.wait_for_selector('table tbody tr', timeout=5000)

        # Search for the HST entry by client name
        page.fill('input[placeholder="Search HSTs"]', client_name)
        page.press('input[placeholder="Search HSTs"]', 'Enter')

        # Wait briefly to allow the search results to load
        page.wait_for_timeout(1000)
        sleep(3)
        # Locate the first HST entry row that matches the client name
        hst_entry_row = page.locator(f'table tbody tr:has-text("{client_name}")').first

        # Hover over the located HST entry row to reveal action icons
        hst_entry_row.hover()

        # Locate the delete button within this row
        delete_icon = hst_entry_row.locator('button[title="Delete"]')  # Adjust the selector if necessary

        # Delete the HST entry if the delete icon is visible
        if delete_icon.is_visible():
            delete_icon.click()
            sleep(2)
            # Confirm the deletion in the confirmation dialog by clicking "Yes"
            confirmation_button = page.locator('button:has-text("Yes")')
            if confirmation_button.is_visible():
                confirmation_button.click()
                page.wait_for_timeout(2000)  # Wait to confirm the deletion takes effect

                # Verify deletion by checking the table again
                if page.locator(f'table tbody tr:has-text("{client_name}")').count() == 0:
                    logger.info("********** HST Delete Test Case Passed **********")
                else:
                    error_logger.error(f"HST entry for client {client_name} is still present in the frontend.")
            else:
                error_logger.error("Confirmation dialog did not appear or 'Yes' button was not found.")

        else:
            error_logger.error(f"No delete button found for client: {client_name}")

    except Exception as e:
        logger.info("********** HST Delete Test Case Failed **********")
        error_logger.error(f"Error occurred while deleting HST: {str(e)}", exc_info=True)
        raise e  # Re-raise to ensure the script stops on failure


