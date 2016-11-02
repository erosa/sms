from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('sms.db')
c = conn.cursor()
c.execute('create table if not exists sms (id integer primary key asc, timestamp text, body text, author text, author_number text, recipient text, recipient_number text)')

with open('sms4.xml') as f:
    soup = BeautifulSoup(f.read(), 'xml')

dups = 0
total = 0

for sms in soup.find_all('sms'):
    total += 1
    if c.execute("select count(*) from sms where body = ? and timestamp = ?", (sms.get('body'), sms.get('date'))).fetchone()[0] == 0:
        if sms.get('type') == '2':
            recipient = sms.get('contact_name')
            recipient_number = sms.get('address')
            author = 'Liz Rosa'
            author_number = '+14084767551'
        else:
            recipient = 'Liz Rosa'
            recipient_number = '+14084767551'
            author = sms.get('contact_name')
            author_number = sms.get('address')
        c.execute('insert into sms(timestamp, body, author, author_number, recipient, recipient_number) values(?, ?, ?, ?, ?, ?)', (sms.get('date'), sms.get('body'), author, author_number, recipient, recipient_number))
    else:
        dups += 1

print(dups, 'duplicates found out of', total, 'total')
conn.commit()
