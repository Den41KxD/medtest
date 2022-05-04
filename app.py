from flask import Flask, request
from API.resources import GetUserSerializer, UserSerializer

app = Flask(__name__)


@app.route('/users/')
def get_all_users():
    return GetUserSerializer(request).get_all_users()


@app.post('/create/')
def user_create():
    user = UserSerializer(request.json)
    return user.save()


@app.route('/user/<user_id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def get_user(user_id):
    user = GetUserSerializer(request)
    if request.method == 'GET':
        return user.get_one_user(user_id)
    elif request.method == 'DELETE':
        return user.delete_user(user_id)
    elif request.method == 'PUT':
        return user.put_user(user_id)
    elif request.method == 'PATCH':
        return user.patch_user(user_id)


if __name__ == '__main__':
    app.run(debug=True)

