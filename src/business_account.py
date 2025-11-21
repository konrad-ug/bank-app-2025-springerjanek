class BusinessAccount:
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip
        self.balance = 0
        self.historia = []

        nip_str = str(nip)

        if len(nip_str) != 10 or not nip_str.isdigit():
            self.nip = "Invalid"
        else:
            self.nip = nip_str
    
    def add_balance(self,kwota):
        self.balance+=kwota

    def make_a_transfer(self,kwota):
        if kwota > 0 and self.balance>=kwota and self.nip != "Invalid":
            self.balance-=kwota
            return True
        else:
            return False
    
    def make_express_transfer(self, kwota):
        fee = 5
        total = kwota + fee
        if kwota > 0 and self.balance - total >= -fee:
            self.balance -= total
            return True
        return False
        
    def take_loan(self, kwota):
        if self.balance >= kwota*2 and -1775 in self.historia:
            self.balance+=kwota
            return True
        return False
