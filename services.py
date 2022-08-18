import random
import aiohttp


BASE_URL = 'http://127.0.0.1:8000'


async def call_apis():
    response = {
        "service1": {},
        "service2": {},
        "payments_sqlite": {},
        "payment_pg": {},
    }
    async with aiohttp.ClientSession() as session:
        # service 1 i.e. agify
        names = ['Jo', 'Christian', 'Tahir', 'Aleisha', 'Tyreese', 'Talia', 'Kaiser', 'Alfred', 'Philip', 'Nelly']
        random_name = random.choice(names)
        url = f'{BASE_URL}/service1?name={random_name}'
        async with session.get(url) as resp:
            response['service1']['status'] = resp.status
            response['service1']['content'] = await resp.json()

        # service 2 i.e. coin_map
        venue_id = random.randrange(1, 1000)
        url = f'{BASE_URL}/service2/{venue_id}'
        async with session.get(url) as resp:
            response['service2']['status'] = resp.status
            response['service2']['content'] = await resp.json()

        # sqlite
        limit = 10
        url = f'{BASE_URL}/payments?limit={limit}'
        async with session.get(url) as resp:
            response['payments_sqlite']['status'] = resp.status
            response['payments_sqlite']['content'] = await resp.json()

        # postgres
        phones = ['989098843', '123321123', '999222333', '765123000', '000000000']
        descriptions = ['Оплата за пиццу', 'Водоканал', 'Электроэнергия', 'Домашний интернет', 'Мобильная связь']
        payload = {
            "phone": random.choice(phones),
            "amount": random.randrange(1, 1000),
            "description": random.choice(descriptions)
        }
        url = f'{BASE_URL}/payments_pg/'
        async with session.post(url, json=payload) as resp:
            response['payment_pg']['status'] = resp.status
            response['payment_pg']['content'] = await resp.json()

    return response
