from flask import abort

from sqlalchemy.orm import Session
from API.mappings import User, Base
from sqlalchemy import create_engine
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import exc

# ENGINE = create_engine("postgresql+psycopg2://medtest:123456@127.0.0.1/medtest", future=True)
ENGINE = create_engine("postgresql+psycopg2://medtest:123456@db/medtest", future=True)


def set_password(old_password):
    password = generate_password_hash(old_password)
    return password


class UserSerializer(User):
    def __init__(self, request):
        super(UserSerializer, self).__init__()
        self.username = request.get('username')
        self.password = request.get('password')
        self.email = request.get('email')
        self.register_data = datetime.now()

    def save(self):
        Base.metadata.create_all(ENGINE)
        try:
            self.password = set_password(self.password)
        except AttributeError:
            return 'No password'

        with Session(ENGINE) as session:
            user = User(
                username=self.username,
                password=self.password,
                email=self.email,
                register_data=self.register_data
            )
            session.add(user)
            try:
                session.commit()
                return {
                    'id': user.id,
                    'text': f'User {self.username} created at: {self.register_data}'}
            except exc.IntegrityError as error:
                if 'psycopg2.errors.NotNullViolation' in error.args[0]:
                    return abort(400, 'incomplete information, please add')
                else:
                    return abort(400, 'this username is already in use ')


class GetUserSerializer:
    def __init__(self, request):
        Base.metadata.create_all(ENGINE)
        self.request = request

    def get_all_users(self):
        all_users = dict()
        with Session(ENGINE) as session:
            users = session.query(User).all()
            for one_user in users:
                all_users.update({one_user.id: {
                    'username': one_user.username,
                    'email': one_user.email
                }})
        return all_users

    @staticmethod
    def get_one_user(user_id):
        with Session(ENGINE) as session:
            user = session.query(User).get(ident=user_id)
            user_json = {
                user.id: {
                    'username': user.username,
                    'email': user.email
                }
            }
        return user_json

    @staticmethod
    def delete_user(user_id):
        with Session(ENGINE) as session:
            user = session.query(User).get(ident=user_id)
            session.delete(user)
            session.commit()
        return f"{user.username} deleted!!"

    def put_user(self, user_id):
        with Session(ENGINE) as session:
            user = session.query(User).get(ident=user_id)
            try:
                user.username = self.request.json.get('username')
                new_password = set_password(self.request.json.get('password'))
                user.password = new_password
                user.email = self.request.json.get('email')
                session.add(user)
                session.commit()
            except AttributeError:
                return abort(400, 'not full info try to use patch method')
        return self.get_one_user(user_id)

    def patch_user(self, user_id):
        with Session(ENGINE) as session:
            user = session.query(User).get(ident=user_id)
            user.username = self.request.json.get('username', user.username)
            new_password = set_password(self.request.json.get('password', user.password))
            user.password = new_password
            user.email = self.request.json.get('email', User.email)
            try:
                session.add(user)
                session.commit()
            except exc.IntegrityError:
                return abort(400, 'this username is already in use ')

        return self.get_one_user(user_id)
