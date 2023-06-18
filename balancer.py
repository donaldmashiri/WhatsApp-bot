def account(loan_balance, settled_balance):
    if((loan_balance - settled_balance) < 0):
        return loan_balance - settled_balance
    return 0