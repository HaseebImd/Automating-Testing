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

def run():
    try:
        # Start browser and get page
        browser, page = start_browser()

        # This log should now write to the log file, not the console
        logger.info("Running test: Client creation")

        # Navigate to login page
        page.goto(f"{base_url}/sign-in")

        # Perform login
        page.fill('input[name="email"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')

        # Check if login was successful by waiting for the URL to change
        try:
            # Wait for the client page URL
            page.wait_for_url(f"{base_url}/apps/clients/", timeout=5000)
            logger.info("Login successful")

        except Exception:
            # Handle the login failure case by checking for error messages or remaining on the login page
            logger.error("Login failed - Invalid credentials")

            stop_browser(browser)
            return  # Exit the function since login failed

        # Wait for the client page
        page.wait_for_url(f"{base_url}/apps/clients/")
        logger.info("Login successful")

        # Create new client
        page.click('text="New Client"')
        page.click('button:text("Next")')

        company_name, share_holder, email, secondary_email,business_number ,phone_number = client_personal_info()

        page.fill('input[id="company_name"]', company_name)
        page.fill('input[id="share_holder"]', share_holder)
        page.fill('input[id="email"]', email)
        page.fill('input[id="business_number"]', business_number)
        page.fill('input[id="secondary_email"]', secondary_email)
        page.fill('input[id="phone_number"]', phone_number)
        logger.info(f"Client personal information filled: {company_name}, {share_holder}")

        # Fill the rest of the fields
        page.click('button:text("Next")')
        street_address,city, state, zip_code = client_address_info()
        # Fill address
        page.fill('input[id="street_address"]', street_address)
        page.fill('input[id="city"]', city)
        page.fill('input[id="state"]', state)
        page.fill('input[id="zip_code"]', zip_code)
        page.click('button:text("Next")')
        logger.info("Client address information filled")

        # Select services (Checkboxes)
        page.check('label:has-text("Payroll")')
        page.check('label:has-text("HST")')
        page.check('label:has-text("Corporate Tax")')
        page.check('label:has-text("Business Incorporation")')
        page.check('label:has-text("Sole")')

        page.click('button:text("Next")')
        page.click('button:text("Create")')
        logger.info("Client creation successful")

        # Close the browser
        stop_browser(browser)
        logger.info("Test completed successfully")

    except Exception as e:
        error_logger.error(f"Error occurred: {str(e)}", exc_info=True)
        logger.info("Test failed")
        stop_browser(browser)

if __name__ == "__main__":
    logger.info("********** Client addition Test Case **********")
    run()
