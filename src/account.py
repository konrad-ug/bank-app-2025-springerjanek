from datetime import date
from lib.smtp import SMTPClient

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


    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "history": self.historia,
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(
            data.get("first_name"),
            data.get("last_name"),
            data.get("pesel"),
        )
        account.balance = data.get("balance", account.balance)
        account.history = data.get("history", [])
        return account

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
    
    def last_three_are_deposits(self):
        if len(self.historia) < 3:
            return False
        last_three = self.historia[-3:]
        return all(t > 0 for t in last_three)

    def sum_last_five_greater_than(self, kwota):
        if len(self.historia) < 5:
            return False
        return sum(self.historia[-5:]) > kwota

    def submit_for_loan(self, kwota):
        if self.last_three_are_deposits():
            self.balance += kwota
            return True
        
        if self.sum_last_five_greater_than(kwota):
            self.balance += kwota
            return True

        return False
    
    def send_history_via_email(self, email):
        today = date.today().isoformat()
        subject = f"Account Transfer History {today}"
        text = f"Personal account history: {self.historia}"

        smtp = SMTPClient()
        return smtp.send(subject, text, email)
