import sqlite3

conn = sqlite3.connect('whatsapp.db')
c = conn.cursor()

# Doctor Table
c.execute("""
CREATE TABLE IF NOT EXISTS doctor (
    doc_name text,
    phone text,
    lat real DEFAULT 0,
    lon real DEFAULT 0,
    specialization text)
""")

# Patient Table
c.execute("""
CREATE TABLE IF NOT EXISTS patient (
    pat_name text,
    phone text,
    lat real DEFAULT 0,
    lon real DEFAULT 0)
""")


def add_patient(msg, phone_no):
    name = msg[:-2]
    data = [name, phone_no]
    c.execute('INSERT INTO patient VALUES(?,?)', data)
