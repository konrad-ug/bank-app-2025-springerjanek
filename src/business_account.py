import os
import requests
from datetime import date
from lib.smtp import SMTPClient

class BusinessAccount:
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip
        self.balance = 0
        self.historia = []

        nip_str = str(nip)

        if len(nip_str) != 10 or not nip_str.isdigit():
            self.nip = "Invalid"
            return
       
        self.nip = nip_str

        if not self.check_nip_status(self.nip):
            raise ValueError("Company not registered!!")
    
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
    
    def check_nip_status(self, nip):
        today = date.today().isoformat()    
        try:
            base_url = os.getenv("BANK_APP_MF_URL", "https://wl-api.mf.gov.pl/api/search/nip")
            url = f"{base_url}/{nip}?date={today}"
            response = requests.get(url)
            data = response.json()

            print("nip status:", data)

            result = data.get("result")
            subject = result.get("subject")
            status = subject.get("statusVat")

            return status == "Czynny"

        except Exception as e:
            print("error:", e)
            return False
        
    def send_history_via_email(self, email):
        today = date.today().isoformat()
        subject = f"Account Transfer History {today}"
        text = f"Company account history: {self.historia}"

        smtp = SMTPClient()
        return smtp.send(subject, text, email)
       
