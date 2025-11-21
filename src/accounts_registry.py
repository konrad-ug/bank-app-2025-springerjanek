from src.account import Account

class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: Account):
        self.accounts.append(account)
    
    def search_account(self, pesel):
        for acc in self.accounts:
            if acc.pesel == pesel:
                return acc
        return None
    
    def list_accounts(self):
        return self.accounts

    def accounts_number(self):
        return len(self.accounts)