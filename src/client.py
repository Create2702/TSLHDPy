import requests

def join(SERVER_URL):
    while True:
        email = input('Please enter your email: ')
        response = requests.post(f'{SERVER_URL}/register', params={'email': email})
        res_data = response.json()

        if res_data.get('message') == 'This email has been blocked from logging in.':
            print(res_data.get('message'))
            continue
        elif res_data.get('message') == 'This email is already in use.':
            print(res_data.get('message'))
            continue
        else:
            code = input(f'Please enter the code from your email {email}: ')
            response_v = requests.post(f'{SERVER_URL}/verify', params={'email': email, 'code': code})
            res_data_v = response_v.json()

            if res_data_v.get('message') == 'You have successfully signed up!':
                print(res_data_v.get('message'))
                break
            else:
                print('Invalid code.')
                continue
