import json
from hashlib import sha256
"""
The login and password are encrypted by sha256 algorithm
"""


def parse_json():
    json_path = "app/static/json/credentials.json"
    with open(json_path) as json_file:
        credentials = json.load(json_file)

    return credentials


def authenticate(login: str, password: str) -> bool:
    login = sha256(login.encode()).hexdigest()
    password = sha256(password.encode()).hexdigest()

    credentials = parse_json()
    if login == credentials["login"] and password == credentials["password"]:
        return True
    return False


if __name__ == "__main__":
    print(parse_json())