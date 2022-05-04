import pytest
import requests

# REQUEST_URL = "http://127.0.0.1:5000"
REQUEST_URL = "http://localhost:8080"


test_user_data = {
    "username": "testuser1",
    "password": "testpassword1",
    "email": "testemail1"
}

test_user_data_bad = {
    "username": "testuser1",
    "password": "testpassword1",

}


class TestClass:

    def test_create_user_bad_request(self):
        responce = requests.post(f'{REQUEST_URL}/create/', json=test_user_data_bad)
        assert 'incomplete information, please add' in responce.text
        assert responce.status_code == 400

    @pytest.mark.dependency()
    def test_create_user(self):
        responce = requests.post(f'{REQUEST_URL}/create/', json=test_user_data)
        pytest.shared = str(responce.json().get('id'))
        assert 'User testuser1 created at' in responce.text
        assert responce.status_code == 200

    @pytest.mark.dependency(depends=["TestClass::test_create_user"])
    def test_get_created_user(self):
        responce = requests.get(f'{REQUEST_URL}/user/{pytest.shared}')
        test_username = responce.json().get(pytest.shared).get('username')
        test_email = responce.json().get(pytest.shared).get('email')
        test_password = responce.json().get(pytest.shared).get('password')
        assert test_username == 'testuser1'
        assert test_email == 'testemail1'
        assert test_password != test_user_data.get('password')
        assert responce.status_code == 200

    def test_create_user_again(self):
        responce = requests.post(f'{REQUEST_URL}/create/', json=test_user_data)
        assert 'this username is already in use ' in responce.text
        assert responce.status_code == 400

    @pytest.mark.dependency(depends=["TestClass::test_create_user"])
    def test_user_patch_method(self):
        self.test_patch_user_data = {
            "username": "testuser3",
            "email": "testemail3"
        }
        responce = requests.patch(f'{REQUEST_URL}/user/{pytest.shared}', json=self.test_patch_user_data)
        test_username = responce.json().get(pytest.shared).get('username')
        test_email = responce.json().get(pytest.shared).get('email')
        assert test_email == self.test_patch_user_data.get('email')
        assert test_username == self.test_patch_user_data.get('username')
        assert responce.status_code == 200

    @pytest.mark.dependency(depends=["TestClass::test_create_user"])
    def test_user_put_method(self):
        self.test_put_user_data = {"username": "testuser2", "password": "testpassword2", "email": "testemail2"}
        responce = requests.put(f'{REQUEST_URL}/user/{pytest.shared}', json=self.test_put_user_data)
        test_username = responce.json().get(pytest.shared).get('username')
        test_email = responce.json().get(pytest.shared).get('email')
        test_password = responce.json().get(pytest.shared).get('password')
        assert test_username != test_user_data.get('username')
        assert test_email != test_user_data.get('email')
        assert test_password != test_user_data.get('password')
        assert test_password != self.test_put_user_data.get('password')
        assert responce.status_code == 200

    @pytest.mark.dependency(depends=["TestClass::test_create_user"])
    def test_user_put_method_bad_request(self):
        self.test_put_user_data_bad_request = {
            "username": "testuser4",
            "email": "testemail4"
            }
        responce = requests.put(f'{REQUEST_URL}/user/{pytest.shared}', json=self.test_put_user_data_bad_request)
        check_responce = requests.get(f'{REQUEST_URL}/user/{pytest.shared}')
        print(responce.text)
        assert 'not full info try to use patch method' in responce.text
        assert check_responce.json().get(pytest.shared).get('username') \
               != self.test_put_user_data_bad_request.get('username')
        assert check_responce.json().get(pytest.shared).get('email') != self.test_put_user_data_bad_request.get('email')
        assert responce.status_code == 400

    @pytest.mark.dependency(depends=["TestClass::test_create_user"])
    def test_user_delete(self):
        responce = requests.delete(f'{REQUEST_URL}/user/{pytest.shared}')
        assert responce.status_code == 200
