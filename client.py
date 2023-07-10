import asyncio
import aiohttp


async def user_get():
    async with aiohttp.ClientSession() as session:
        response = await session.get("http://127.0.0.1:8080/users")
        print()
        print(response.status)
        text = await response.json()
        print(text)


async def user_post(data):
    async with aiohttp.ClientSession() as session:
        response = await session.post("http://127.0.0.1:8080/users", json=data)
        print()
        print(response.status)
        text = await response.text()
        print(text)


async def advert_get():
    async with aiohttp.ClientSession() as session:
        response = await session.get("http://127.0.0.1:8080/adverts")
        print()
        print(response.status)
        text = await response.text()
        print(text)


async def advert_post(data, auth):
    async with aiohttp.ClientSession(auth=auth) as session:
        response = await session.post("http://127.0.0.1:8080/adverts", json=data)
        print()
        print(response.status)
        text = await response.text()
        print(text)


async def advert_delete(auth, adv_id):
    async with aiohttp.ClientSession(auth=auth) as session:
        response = await session.delete(f"http://127.0.0.1:8080/adverts/{adv_id}")
        print()
        print(response.status)
        text = await response.text()
        print(text)


if __name__ == "__main__":
    user1 = {
        "username": "Yura",
        "email": "Yura@mail.ru",
        "password": "111",
    }

    user2 = {
        "username": "Nastya",
        "email": "Nastya@mail.ru",
        "password": "222",
    }

    auth1 = aiohttp.BasicAuth(login=user1["email"], password=user1["password"])
    auth2 = aiohttp.BasicAuth(login=user2["email"], password=user2["password"])
    auth3 = aiohttp.BasicAuth(login=user2["email"], password="333")

    data1 = {
        "header": "Car",
        "description": "Buy a car",
    }

    data2 = {
        "header": "House",
        "description": "Buy a house",
    }

    asyncio.run(user_post(user1))  # 200 Пользователь 'Yura' создан
    asyncio.run(user_post(user1))  # 500 Пользователь 'Yura' уже существует
    asyncio.run(user_post(user2))  # 200 Пользователь 'Nastya' создан
    asyncio.run(user_get())  # 200

    asyncio.run(advert_post(data1, auth1))  # 200 Объявление создано
    asyncio.run(advert_post(data2, auth2))  # 200 Объявление создано
    asyncio.run(advert_post(data2, auth3))  # 401 Некорректный логин или пароль
    asyncio.run(advert_get())  # 200

    asyncio.run(advert_delete(auth2, 1))  # 409 Нельзя удалить чужое объявление
    asyncio.run(advert_delete(auth2, 3))  # 404 Объявления не существует
    asyncio.run(advert_delete(auth2, 2))  # 200 Объявление удалено
