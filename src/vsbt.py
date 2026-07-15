import json
from uuid import uuid4
import yagmail
import secrets
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def verif(email):
    v_code = secrets.token_hex(3)
    yag = yagmail.SMTP(os.getenv('TSLHDPY_EMAIL'), os.getenv('TSLHPY_PASSWORD'))
    yag.send(email, 'Verification', f"Your verification code: {v_code}, If it's not you, don't share the code with anyone.")
    return v_code

def join():
    flag = False
    attempts = 5
    with open('users.json', 'r') as e:
        users = json.load(e)
    with open('blocked_emails.json', 'r') as be:
        blocked_emails = json.load(be)
    print('1. Log in')
    print('2. Sign up')
    act = int(input('Enter the action number: '))

    if act == 1:
        while True:
            email = input('Please, enter your email: ')
            if email in blocked_emails:
                print('This email has been blocked from logging in.')
                break

            if email in users.values():
                try:
                    v_code = verif(email=email)
                except yagmail.error.YagInvalidEmailAddress:
                    print('Invalid email, please try again.')
                    break
                code = input(f'Please enter the code from your email {email}: ')
                if v_code == code:
                    print('You have successfully logged in!')
                    flag = True
                    break
                else:
                    if attempts != 1:
                        print('Invalid code. Try again.')
                        attempts -= 1
                        print(f'You have {attempts} attempts')
                        continue
                    else:
                        print('This email has been blocked from logging in.')
                        blocked_emails[email] = str(datetime.now())
                        with open('blocked_emails.json', 'w') as f:
                            json.dump(blocked_emails, f, indent=4)
                        break
            else:
                print('Select "Sign up" to create an account.')
                break

    elif act == 2:
        while True:
            email = input('Please, enter your email: ')

            if email in users.values():
                print('This email is already in use.')
                continue

            try:
                v_code = verif(email=email)
            except yagmail.error.YagInvalidEmailAddress:
                print('Invalid email, please try again.')
                break
            code = input(f'Please enter the code from your email {email}: ')
            success = False
            if v_code == code:
                while True:
                    id = str(uuid4())
                    if id in users:
                        continue
                    else:
                        users[id] = email
                        success = True
                        break
            else:
                if attempts != 1:
                    print('Invalid code. Try again.')
                    attempts -= 1
                    print(f'You have {attempts} attempts')
                    continue
                else:
                    print('This email has been blocked from logging in.')
                    blocked_emails[email] = str(datetime.now())
                    with open('blocked_emails.json', 'w') as f:
                        json.dump(blocked_emails, f, indent=4)
                    break
            if success:
                print('You have successfully signed up!')
                flag = True
                break

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
    else:
        print('Please, select only "1" or "2"')
    return flag
    




