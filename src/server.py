from fastapi import FastAPI
import json
from dotenv import load_dotenv
from uuid import uuid4
import yagmail
import secrets
import os

load_dotenv()

app = FastAPI()

@app.post('/register')
def register(email: str):
    with open('../../../../blocked_emails.json', 'r') as be:
        blocked_emails = json.load(be)
    with open('../../../../users.json', 'r') as u:
        users = json.load(u)

    if email in blocked_emails:
        return {'message': 'This email has been blocked from logging in.'}
    else:
        if email in users.values():
            return {'message': 'This email is already in use.'}
        else:
            v_code = secrets.token_hex(3)
            yag = yagmail.SMTP(os.getenv('TSLHDPY_EMAIL'), os.getenv('TSLHPY_PASSWORD'))
            yag.send(email, 'Verification', f"Your verification code: {v_code}, If it's not you, don't share the code with anyone.")

            with open('../../../../codes.json', 'r') as c:
                codes = json.load(c)

            codes[email] = v_code

            with open('../../../../codes.json', 'w') as f:
                json.dump(codes, f, indent=4)
            return {'status_code': 200}

@app.post('/verify')
def verify(email: str, code: str):
    with open('../../../../codes.json', 'r') as c:
        codes = json.load(c)
    with open('../../../../users.json', 'r') as u:
        users = json.load(u)
    if code == codes[email]:
        while True:
            id = str(uuid4())
            if id in users:
                continue
            else:
                users[id] = email
                with open('../../../../users.json', 'w') as u:
                    json.dump(users, u, indent=4)
                del codes[email]
                with open('../../../../codes.json', 'w') as c:
                    json.dump(codes, c, indent=4)
                break
        return {'message': 'You have successfully signed up!'}
    else:
        return {'message': 'Invalid code.'}
    


