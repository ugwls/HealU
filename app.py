from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import db
import main

app = Flask(__name__)


@app.route('/')
def home():
    return "App is Up!"


@app.route('/sms', methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    p_no = request.form.get('From')
    phone_no = p_no.replace('whatsapp:', '')
    lat = request.form.get('Latitude')
    lon = request.form.get('Longitude')

    option = msg[-1]
    if option == '1':
        # p_msg = msg
        # p_phone_no = phone_no
        # p_lat = lat
        # P_lon = lon
        db.add_patient(msg, phone_no)
        main.patient(msg, phone_no)
    elif option == '2':
        pass


if __name__ == '__main__':
    app.run(debug=True)
