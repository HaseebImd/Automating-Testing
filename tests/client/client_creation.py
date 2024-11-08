from time import sleep
from utils.logger import setup_logging
from utils.random_data import client_personal_info, client_address_info

import time

# Set up logging
logger, error_logger = setup_logging()

def create_client(page):
    logger.info("********** Client Creation Test Case Running **********")
    try:
        """
        Function to create a new client and return the client's name.
        """
        sleep(5)
        page.click('text="New Client"')
        page.click('button:text("Next")')
        time.sleep(5)

        # Generate client personal information
        company_name, share_holder, email, secondary_email, business_number, phone_number = client_personal_info()

        # Fill client details
        page.fill('input[id="company_name"]', company_name)
        page.fill('input[id="share_holder"]', share_holder)
        page.fill('input[id="email"]', email)
        page.fill('input[id="business_number"]', business_number)
        page.fill('input[id="secondary_email"]', secondary_email)
        page.fill('input[id="phone_number"]', phone_number)
        page.click('button:text("Next")')
        time.sleep(1)

        # Generate and fill client address information
        street_address, city, state, zip_code = client_address_info()
        page.fill('input[id="street_address"]', street_address)
        page.fill('input[id="city"]', city)
        page.fill('input[id="state"]', state)
        page.fill('input[id="zip_code"]', zip_code)
        page.click('button:text("Next")')

        # Select services
        page.check('label:has-text("Payroll")')
        page.check('label:has-text("HST")')
        page.check('label:has-text("Corporate Tax")')
        page.check('label:has-text("Business Incorporation")')
        page.check('label:has-text("Sole")')

        page.click('button:text("Next")')
        page.click('button:text("Create")')
        logger.info(f"Client named {company_name} created successfully")
        logger.info("********** Client creation Test Case Passed **********")

        return company_name
    except Exception as e:
        logger.error("********** Client creation Test Case Failed **********")
        error_logger.error(f"Error occurred while creating client: {str(e)}", exc_info=True)
        raise e


