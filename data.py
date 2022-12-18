import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import Settings


Base = declarative_base()
engine = sq.create_engine(Settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "user"
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)


class FoundUser(Base):
    __tablename__ = "founduser"
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    top_photos = sq.Column(sq.String(1000))
    User_id = sq.Column(sq.Integer, sq.ForeignKey("user.id"))
    like = sq.Column(sq.Boolean)
    user = relationship(User)

#создание таблицы
def create_tables():
    Base.metadata.create_all(engine)

# добавляет юзера в базу данных
def add_user(user: User) -> None:
    session.expire_on_commit = False
    session.add(user)
    session.commit()

#добавляет информацию о пользователе в БД
def add_user_list(user: User) -> None:
    session.expire_on_commit = False
    session.add_all(user)
    session.commit()

#получает список юзеров из базы данных
def get_viewed_user(user_id: str, users_list: list) -> list:
    list = session.query(FoundUser).filter(FoundUser.User_id == user_id).all()
    users = set()
    found_users = []
    for item in list:
        users.add(item.vk_id)
    for item in users_list:
        if item["id"] not in users:
            found_users.append(item)
    return found_users
