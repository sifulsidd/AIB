# import db
from ai import const
from twilio.rest import Client

# print(db.get_user('mscarn'))

twilio_client = Client(const.TWILIO_ID, const.TWILIO_TOKEN)


def send_sms(content):
    message = twilio_client.messages.create(to="+13474595013", from_="+16174058420", body=content)
    print(message)

send_sms('Hello!')
