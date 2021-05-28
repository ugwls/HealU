from pymongo import MongoClient
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


# database connectivity
client = MongoClient(
    "mongodb+srv://ujjwal:Ujjwal.16@cluster0.hnhs0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["whatsapp_db"]
collection = db["test_db"]
collection1 = db["test_db1"]


# flask part
apbot = Flask(__name__)


@apbot.route("/sms", methods=["get", "post"])
def reply():
    num = request.form.get("From")
    num = num.replace("whatsapp:", "")
    msg_text = request.form.get("Body")
    x = collection.find_one({"NUMBER": num})
    y = collection1.find_one({"NUMBER": num})
    try:
        status = x["status"]
        status1 = y["status"]
    except:
        pass

    if(bool(x) == False or bool(y) == False):
        collection.insert_one({"NUMBER": num, "status": "first"})
        collection1.insert_one({
            "NUMBER": num, "name": "null", "special": "null", "Latitude": "0", "Longitude": "0", "status": "first"})
        msg = MessagingResponse()
        msg.message('''
Namaste 🙏
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
                collection.update_one(myquery, newvalues)
                # collection1.delete_one({"NUMBER": num})
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
                # collection.delete_one({"NUMBER": num})
                # collection1.insert_one({
                #     "name": msg_text[:-2], "special": "null", "Latitude": "0", "Longitude": "0", "status": "doctor"})
                myquery = {"name": "null"}
                newvalues = {"$set": {"name": msg_text[:-2]}}
                collection1.update_one(myquery, newvalues)
                myquery = {"status": "first"}
                newvalues = {"$set": {"status": "doctor"}}
                collection1.update_one(myquery, newvalues)
                msg = MessagingResponse()
                msg.message('Please tell us your Specializations.')
                return(str(msg))
        elif(status == 'patient'):
            pass

        # doctor
        elif(status1 == 'doctor'):
            myquery = {"special": "null", }
            newvalues = {"$set": {"special": msg_text}}
            collection1.update_one(myquery, newvalues)
            myquery = {"status": "doctor", }
            newvalues = {"$set": {"status": "doc_loc"}}
            collection1.update_one(myquery, newvalues)
            msg = MessagingResponse()
            msg.message('Please share your Location.')
            return(str(msg))

        elif(status1 == 'doc_loc'):
            lat = request.form.get("Latitude")
            lon = request.form.get("Longitude")
            myquery = {"Latitude": "0", }
            newvalues = {"$set": {"Latitude": lat}}
            collection1.update_one(myquery, newvalues)
            myquery = {"Longitude": "0", }
            newvalues = {"$set": {"Longitude": lon}}
            collection1.update_one(myquery, newvalues)
            myquery = {"status": "doc_loc", }
            newvalues = {"$set": {"status": "done"}}
            collection1.update_one(myquery, newvalues)
            msg = MessagingResponse()
            msg.message('Doctor Added!!')
            return(str(msg))

        elif(status1 == 'done'):
            msg = MessagingResponse()
            msg.message('You have already in our database as a Doctor.')
            return(str(msg))


if (__name__ == "__main__"):
    apbot.run(port=5000)
