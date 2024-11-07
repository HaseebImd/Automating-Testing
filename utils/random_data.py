import random
import string
from datetime import datetime

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_email():
    random_name = generate_random_string(5).lower()
    return f"{random_name}@test.com"

def generate_random_phone():
    return f"03{random.randint(0, 9)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_random_company_name():
    current_datetime = datetime.now().strftime("%H%M%S-%Y%m%d")
    return f"[Testing]-{current_datetime}-{generate_random_string(5)}"

def client_personal_info():
    return (
        generate_random_company_name(),
        generate_random_string(6),  # share_holder
        generate_random_email(),    # email
        generate_random_email(),    # secondary_email
        f"{random.randint(100000000, 999999999)}", #random business number
        generate_random_phone()     # phone_number
    )

def client_address_info():
    return (
        generate_random_string(10),
        generate_random_string(6),
        generate_random_string(6),
        # generate random zip code of max 6 digits
        f"{random.randint(100000, 999999)}"
    )