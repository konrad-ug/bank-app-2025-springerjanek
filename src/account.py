class Account:
    def __init__(self, first_name, last_name, pesel,promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        if(len(str(pesel)) != 11):
            self.pesel = "Invalid"
        else:
            self.pesel = pesel
        if promo_code and len(promo_code.split('_'))==2 and promo_code.split('_')[0] == "PROM":
            self.balance+=50
        
            