from hst.add_hst import add_hst_for_client
from hst.delete_hst import delete_hst_for_client

def HST_test_cases(page,client_name, hst_method="Monthly"):
    add_hst_for_client(page, client_name, hst_method)
    # delete_hst_for_client(page, client_name)