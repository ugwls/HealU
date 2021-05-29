from pymongo import MongoClient
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


# database connectivity
client = MongoClient(
    "mongodb+srv://ujjwal:Ujjwal.16@cluster0.hnhs0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["whatsapp_db"]
patient = db["patient"]
doctor = db["doctor"]


app = Flask(__name__)


@app.route("/sms", methods=["get", "post"])
def reply():
    num = request.form.get("From")
    num = num.replace("whatsapp:", "")
    msg_text = request.form.get("Body")
    x = patient.find_one({"NUMBER": num})
    y = doctor.find_one({"NUMBER": num})
    try:
        status = x["status"]  # Patient
        status1 = y["status"]  # Doctor
    except:
        pass

    if(bool(x) == False or bool(y) == False):
        patient.insert_one({"NUMBER": num, "status": "first"})
        doctor.insert_one({"NUMBER": num, "status": "first"})
        msg = MessagingResponse()
        msg.message('''Namaste 🙏
        Welcome to HealU
        This HelpDesk is to create awareness and help
        you and your family stay safe.

        Please choose from the following options 👇

        1. Patient (Ex: Ujjwal Sharma 1)
        2. Doctor  (Ex: Ujjwal Sharma 2)

        💡 Tip: Your name and option number sperated
        by space that is 'Ujjwal Sharma 1'.''')
        return(str(msg))
    else:
        if(status == "first"):
            if(msg_text[-1] == '1'):
                myquery = {"status": "first"}
                newvalues = {"$set": {"status": "patient"}}
                patient.update_one(myquery, newvalues)
                doctor.delete_one({"NUMBER": num})
                msg = MessagingResponse()
                msg.message('''
                Please select the symptoms from our list-:

                1.) food allergies, insect sting allergies.
                2.) heart failure, heart attack, high blood pressure, or irregular heartbeat.
                3.) for asking or detailing moles, scars, acne, or skin allergies about specific medicines.
                4.) moles, scars, acne, or skin allergies.
                5.) diabetes, thyroid problems, calcium and bone disorders.
                7.) Emergency Case(medicine specialist).
                8.) Fever, cold & cuff, Headache, Clogged Nose, and Body Pain.

                💡 Tip: Select the option number from the list.(Ex.1)''')
                return(str(msg))

            elif(msg_text[-1] == '2'):
                patient.delete_one({"NUMBER": num})
                myquery = {"status": "first"}
                newvalues = {
                    "$set": {"name": msg_text[:-2], "status": "doctor"}}
                doctor.update_many(myquery, newvalues)
                msg = MessagingResponse()
                msg.message('Please tell us your Specializations.')
                return(str(msg))

        # Patient
        elif(status == 'patient'):
            myquery = {"NUMBER": num}
            newvalues = {"$set": {"symptoms": msg_text, "status": "pat_loc"}}
            doctor.update_many(myquery, newvalues)
            msg = MessagingResponse()
            msg.message(
                'If you want to get doctors near your location please share your location and if not please send No.')
            return(str(msg))

        elif(status == "pat_loc"):
            if(msg_text.lower() == 'no'):
                pass
            else:
                lat = request.form.get("Latitude")
                lon = request.form.get("Longitude")
                myquery = {"NUMBER": num}
                newvalues = {
                    "$set":
                    {
                        "Latitude": lat,
                        "Longitude": lon,
                        "status": "send_doc"}}
                doctor.update_many(myquery, newvalues)
                msg = MessagingResponse()
                msg.message('Doctor Info')
                return(str(msg))

        # doctor
        elif(status1 == 'doctor'):
            myquery = {"NUMBER": num}
            newvalues = {"$set": {"special": msg_text, "status": "doc_loc"}}
            doctor.update_many(myquery, newvalues)
            msg = MessagingResponse()
            msg.message('Please share your Location.')
            return(str(msg))

        elif(status1 == 'doc_loc'):
            lat = request.form.get("Latitude")
            lon = request.form.get("Longitude")
            myquery = {"NUMBER": num}
            newvalues = {"$set": {"Latitude": lat,
                                  "Longitude": lon, "status": "done"}}
            doctor.update_many(myquery, newvalues)
            msg = MessagingResponse()
            msg.message('Doctor Added!!')
            return(str(msg))

        elif(status1 == 'done'):
            msg = MessagingResponse()
            msg.message('You have already in our database as a Doctor.')
            return(str(msg))


if (__name__ == "__main__"):
    app.run(debug=True)
