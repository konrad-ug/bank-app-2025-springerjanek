from src.account import Account

class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: Account):
        if self.search_account(account.pesel):
            return False
        self.accounts.append(account)
        return True
    
    def search_account(self, pesel):
        for acc in self.accounts:
            if acc.pesel == pesel:
                return acc
        return None
    
    def list_accounts(self):
        return self.accounts

    def accounts_number(self):
        return len(self.accounts)
    
    def update_account(self, pesel, new_data):
        acc = self.search_account(pesel)
        if acc is None:
            return None
        
        if "first_name" in new_data:
            acc.first_name = new_data["first_name"]
        if "last_name" in new_data:
            acc.last_name = new_data["last_name"]

        return acc

    def delete_account(self, pesel):
        acc = self.search_account(pesel)
        if acc:
            self.accounts.remove(acc)
            return True
        return False
    
    def clear(self):
        self.accounts = []