import asyncio
import sqlite3
import time

import aiosmtplib

db = sqlite3.connect('contacts.db')
contacts = [contact[0] for contact in db.execute("select email from contacts").fetchall()]

HOST = '127.0.0.1'
PORT = 1025

SUBJECT = 'TY'
FROM = 'ad.service@mail.com'


async def send_message(recipient):
    await aiosmtplib.send(
        message=f'From: {FROM}\n'
                f'Subject: {SUBJECT}\n'
                f'\n'
                f'Уважаемый {recipient}!\nСпасибо, что пользуетесь нашим сервисом объявлений.'.encode(),
        sender=FROM,
        recipients=recipient,
        hostname=HOST,
        port=PORT
        )


async def main():
    tasks = [asyncio.create_task(send_message(recipient)) for recipient in contacts]
    await asyncio.wait(tasks)

start = time.time()
event_loop = asyncio.run(main())
print(time.time() - start)
