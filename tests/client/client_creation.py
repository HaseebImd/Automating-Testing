from time import sleep
from utils.logger import setup_logging
from utils.random_data import client_personal_info, client_address_info
import random

# Set up logging
logger, error_logger = setup_logging()


def create_client(page):
    logger.info("********** Client Creation Test Case Running **********")
    try:
        """
        Function to create a new client and return the client's name.
        """
        # Wait for "New Client" button and click it
        page.wait_for_selector('text="New Client"', timeout=30000)
        logger.info("New Client button is visible.")
        page.click('text="New Client"')

        # Add a small random delay
        sleep(random.uniform(1, 2))

        # Wait for "Next" button and click it
        page.wait_for_selector('button:text("Next")', timeout=30000)
        logger.info("Next button is visible.")
        page.click('button:text("Next")')

        # Add a small random delay
        sleep(random.uniform(1, 2))

        # Generate client personal information
        (
            company_name,
            share_holder,
            email,
            secondary_email,
            business_number,
            phone_number,
        ) = client_personal_info()
        logger.info("Generated client personal information successfully.")

        # Fill client details
        logger.info("Filling client details.")
        page.fill('input[id="company_name"]', company_name)
        page.fill('input[id="share_holder"]', share_holder)
        page.fill('input[id="email"]', email)
        page.fill('input[id="business_number"]', business_number)
        page.fill('input[id="secondary_email"]', secondary_email)
        page.fill('input[id="phone_number"]', phone_number)

        # Wait for "Next" button and click it
        page.wait_for_selector('button:text("Next")', timeout=30000)
        logger.info("Clicking Next button after filling client details.")
        page.click('button:text("Next")')

        # Generate and fill client address information
        street_address, city, state, zip_code = client_address_info()
        logger.info("Generated client address information successfully.")
        page.fill('input[id="street_address"]', street_address)
        page.fill('input[id="city"]', city)
        page.fill('input[id="state"]', state)
        page.fill('input[id="zip_code"]', zip_code)

        # Wait for "Next" button and click it
        page.wait_for_selector('button:text("Next")', timeout=30000)
        logger.info("Clicking Next button after filling address details.")
        page.click('button:text("Next")')

        # Select services
        logger.info("Selecting services for the client.")
        page.check('label:has-text("Payroll")')
        page.check('label:has-text("HST")')
        page.check('label:has-text("Corporate Tax")')
        page.check('label:has-text("Business Incorporation")')
        page.check('label:has-text("Sole")')

        # Wait for "Next" button and click it
        page.wait_for_selector('button:text("Next")', timeout=30000)
        logger.info("Clicking Next button after selecting services.")
        page.click('button:text("Next")')

        # Wait for "Create" button and click it
        page.wait_for_selector('button:text("Create")', timeout=30000)
        logger.info("Clicking Create button to finalize client creation.")
        page.click('button:text("Create")')

        # Confirm successful client creation
        logger.info(f"Client named {company_name} created successfully.")
        logger.info("********** Client Creation Test Case Passed **********")

        return company_name
    except Exception as e:
        logger.error("********** Client Creation Test Case Failed **********")
        error_logger.error(
            f"Error occurred while creating client: {str(e)}", exc_info=True
        )
        raise e
