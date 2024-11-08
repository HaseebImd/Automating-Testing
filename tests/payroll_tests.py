from payroll.add_payroll import add_payroll_for_client


def Payroll_test_cases(page,client_name, payroll_method="Bimonthly"):
    add_payroll_for_client(page, client_name, payroll_method)
