import base64

import bcrypt
from aiohttp import web
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import Advertisement, Base, Session, User, engine


async def cleanup_engine(app: web.Application):
    print("Start")
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def hash_password(password: str):
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password


def chech_password(password: str, hash_pw: str):
    password = password.encode()
    hash_pw = hash_pw.encode()
    return bcrypt.checkpw(password, hash_pw)


@web.middleware
async def middleware_session(request, handler):
    """
    middleware-функция чтобы взаимодействовать с запросом перед его обработкой и с ответом после обработки.
    Обязательно регистрируем с помощью декоратора. В данном случае мы записываем в запрос сессию работы с БД,
    чтобы не вызывать ее каждый раз в каждой функции.
    :param request:объект запроса
    :param handler: обработчик запроса, получающий на в ход request и выдающий web.Response()
    :return: web.Response()
    """
    async with Session() as session:
        request["session"] = session  # записываем сессию внутрь объекта запроса
        try:
            response = await handler(request)  # передаем управление обработчику
        except SQLAlchemyError:
            return web.Response(text=f"Ошибка базы данных", status=500)
        return response  # возвращаем объект запроса


class UserView(web.View):
    @property
    def session(self):
        return self.request["session"]

    async def get(self):
        users = await self.session.execute(select(User))
        users_data = users.scalars()
        user_list = [
            {"username": user.username, "password": user.password, "email": user.email}
            for user in users_data
        ]
        return web.json_response(user_list)

    async def post(self):
        json_data = await self.request.json()
        username = json_data["username"]
        email = json_data["email"]
        password = hash_password(json_data["password"])
        new_user = User(username=username, email=email, password=password)
        try:
            self.session.add(new_user)
            await self.session.commit()
        except IntegrityError:
            return web.Response(
                text=f"Пользователь '{username}' уже существует", status=500
            )
        return web.Response(text=f"Пользователь '{username}' создан")


class AdvertView(web.View):
    @property
    def session(self):
        return self.request["session"]

    async def authentication(self):
        auth_header = self.request.headers.get("Authorization")
        auth_bytes = auth_header[6:].encode()
        auth_decoded = base64.decodebytes(auth_bytes).decode()
        email, password = auth_decoded.split(":", 1)

        stm = select(User).where(User.email == email)
        result = await self.session.execute(stm)
        user = result.scalar_one()
        user_id = user.id
        user_hash_pass = user.password

        if chech_password(password, user_hash_pass) == True:
            return user_id
        else:
            raise web.HTTPUnauthorized(text="Некорректный логин или пароль")

    async def get(self):
        stmt = select(Advertisement).options(selectinload(Advertisement.users))
        advertisements = await self.session.execute(stmt)
        adv_data = advertisements.scalars()

        adv_list = [
            {
                "header": adv.header,
                "description": adv.description,
                "author": adv.users.username,
            }
            for adv in adv_data
        ]
        return web.json_response(adv_list)

    async def post(self):
        json_data = await self.request.json()
        author_id = await self.authentication()

        new_adv = Advertisement(
            header=json_data["header"],
            description=json_data["description"],
            author_id=author_id,
        )
        try:
            self.session.add(new_adv)
            await self.session.commit()
        except IntegrityError:
            return web.Response(text=f"Не удалось создать объявление", status=500)
        return web.Response(text=f"Объявление создано")

    async def delete(self):
        adv_id = int(self.request.match_info["adv_id"])
        try:
            stmt = (
                select(Advertisement)
                .options(selectinload(Advertisement.users))
                .where(Advertisement.id == adv_id)
            )
            result = await self.session.execute(stmt)
            delete_adv = result.scalar_one()
            author_id = await self.authentication()

            if delete_adv.users.id == author_id:
                await self.session.delete(delete_adv)
                await self.session.commit()
                return web.Response(text="Объявление удалено")
            else:
                return web.Response(text="Нельзя удалить чужое объявление", status=409)

        except:
            raise web.HTTPNotFound(
                text="Объявления не существует", content_type="application/json"
            )


app = web.Application()
app.add_routes(
    [
        web.get("/users", UserView),
        web.post("/users", UserView),
        web.get("/adverts", AdvertView),
        web.post("/adverts", AdvertView),
        web.delete("/adverts/{adv_id:\d+}", AdvertView),
    ]
)
app.cleanup_ctx.append(cleanup_engine)
app.middlewares.append(middleware_session)

if __name__ == "__main__":
    web.run_app(app)
