import random
import time

import aiohttp
import asyncio


BASE_URL = 'http://127.0.0.1:8000'

start_time = time.time()


async def call_apis():
    responses = []
    async with aiohttp.ClientSession() as session:
        futures = [sqlite(session), pg_sql(session), service1(session), service2(session)]
        for task in asyncio.as_completed(futures):
            responses.append(await task)

    for response in responses:
        if response:
            print({
                "service": response[2],
                "status_code": response[0],
                "content": response[1],
            })
            print()


async def service1(session):
    # service 1 i.e. agify
    print("service1 started..")
    names = ['Jo', 'Christian', 'Tahir', 'Aleisha', 'Tyreese', 'Talia', 'Kaiser', 'Alfred', 'Philip', 'Nelly']
    random_name = random.choice(names)
    url = f'{BASE_URL}/service1?name={random_name}'
    # await asyncio.sleep(1)
    try:
        async with session.get(url) as resp:
            status = resp.status
            data = await resp.json()
            print("service1 ended..")
            return status, data, "service1"
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(f"Connection error at '{url}': {e}")


async def service2(session):
    print("service2 started..")
    # service 2 i.e. coin_map
    venue_id = random.randrange(1, 1000)
    url = f'{BASE_URL}/service2/{venue_id}'
    # await asyncio.sleep(1)
    try:
        async with session.get(url) as resp:
            status = resp.status
            data = await resp.json()
            print("service2 ended..")
            return status, data, "service2"
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(f"Connection error at '{url}': {e}")


async def sqlite(session):
    print("sqlite started..")
    # sqlite
    limit = 10
    url = f'{BASE_URL}/payments?limit={limit}'
    try:
        async with session.get(url) as resp:
            status = resp.status
            data = await resp.json()
            print("sqlite ended..")
            return status, data, "sqlite"
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(f"Connection error at '{url}': {e}")


async def pg_sql(session):
    print("postgres started..")
    # postgres
    phones = ['989098843', '123321123', '999222333', '765123000', '000000000']
    descriptions = ['Оплата за пиццу', 'Водоканал', 'Электроэнергия', 'Домашний интернет', 'Мобильная связь']
    payload = {
        "phone": random.choice(phones),
        "amount": random.randrange(1, 1000),
        "description": random.choice(descriptions)
    }
    url = f'{BASE_URL}/payments_pg/'
    try:
        async with session.post(url, json=payload) as resp:
            status = resp.status
            data = await resp.json()
            print("postgres ended..")
            return status, data, "pg_sql"
    except aiohttp.client_exceptions.ClientConnectorError as e:
        print(f"Connection error at '{url}': {e}")

asyncio.run(call_apis())
print("--- %s seconds ---" % (time.time() - start_time))
