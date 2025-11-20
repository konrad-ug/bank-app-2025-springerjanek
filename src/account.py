class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.historia = []

        pesel_str = str(pesel)

        if len(pesel_str) != 11 or not pesel_str.isdigit():
            self.pesel = "Invalid"
        else:
            self.pesel = pesel_str

        if self.pesel != "Invalid":
            if self.czy_przyznac_promo(self.pesel):
                if promo_code and len(promo_code.split('_')) == 2 and promo_code.split('_')[0] == "PROM":
                    self.balance += 50

    def czy_przyznac_promo(self, pesel):
        s = str(pesel)
        yy = int(s[0:2])
        mm = int(s[2:4])

        if 1 <= mm <= 12:
            century = 1900
        elif 21 <= mm <= 32:
            century = 2000
        elif 41 <= mm <= 52:
            century = 2100
        elif 61 <= mm <= 72:
            century = 2200
        else:
            return False  # niepoprawny miesiąc

        rok_urodzenia = century + yy
        return rok_urodzenia > 1960
    
    def add_balance(self,kwota):
        self.balance+=kwota
        self.historia.append(kwota)

    def make_a_transfer(self,kwota):
        if kwota > 0 and self.balance>=kwota:
            self.balance-=kwota
            self.historia.append(-kwota)
            return True
        else:
            return False
    
    def make_express_transfer(self, kwota):
        fee = 1
        total = kwota + fee
        if kwota > 0 and self.balance - total >= -fee:
            self.balance -= total
            self.historia.append(-kwota)
            self.historia.append(-fee)     
            return True
        return False
    
    def _last_three_are_deposits(self):
        if len(self.historia) < 3:
            return False
        last_three = self.historia[-3:]
        return all(t > 0 for t in last_three)

    def _sum_last_five_greater_than(self, amount):
        if len(self.historia) < 5:
            return False
        return sum(self.historia[-5:]) > amount

    def submit_for_loan(self, amount):
        if self._last_three_are_deposits():
            self.balance += amount
            return True
        
        if self._sum_last_five_greater_than(amount):
            self.balance += amount
            return True

        return False
        
class BusinessAccount:
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip
        self.balance = 0

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
        
