import requests
from twilio.rest import Client
from locationServer import location
import os
from dotenv import load_dotenv

class SmsNotifier:
    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number
        

    def get_location_info(self):
        try:
           
            location_text = f"{location['address']}"
            maps_link = f"https://www.google.com/maps?q={location['latitude']},{location['longitude']}"
            return location_text, maps_link
        except Exception as e:
            print(f"[Location] Error fetching location info: {e}")
            return "Unknown", ""

    def send_sms(self, message_body,target_number):
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.twilio_number,
                to=target_number
            )
            print(f"[Twilio] SMS sent: {message.sid}")
            return True
        except Exception as e:
            print(f"[Twilio] Error sending SMS: {e}")
            return False
        


load_dotenv()

account_sid = os.getenv("ACCOUNT_SID_ME")
auth_token = os.getenv("AUTH_TOKEN_ME")
twilio_number = os.getenv("TWILIO_NUMBER_ME")

sms_notifier = SmsNotifier(account_sid, auth_token, twilio_number)

# Example usage:
# keys = Your keys object or dictionary containing account_sid, auth_token, twilio_number, and target_number
# notifier = SmsNotifier(keys.account_sid, keys.auth_token, keys.twilio_number, keys.target_number)
# location_text, maps_link = notifier.get_location_info()
# message_body = f"🚨 Hazard Detected! Driver unresponsive for 5+ seconds.\nLocation: {maps_link}"
# notifier.send_sms(message_body)