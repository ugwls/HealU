import sqlite3

# db
conn = sqlite3.connect('whatsapp.db')
c = conn.cursor()


def patient(msg, phone_no):
    name = msg[:-2]
    data = [name, phone_no]
    try:
        c.execute(
            "SELECT * FROM patient WHERE p_name = ? and phone = ?", data)
        pass
    except:
        pass


def doctor():
    pass
