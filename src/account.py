class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0

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
        elif 81 <= mm <= 92:
            century = 1800
        else:
            return False  # niepoprawny miesiąc

        rok_urodzenia = century + yy
        return rok_urodzenia > 1960
