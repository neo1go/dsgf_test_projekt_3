from saucedemo_users import get_users, get_password
from test_logic import test_user_login
from db_logger import log_failure_to_db

users = get_users()
password = get_password()

for user in users:
    success = test_user_login(user, password)
    if not success:
        log_failure_to_db(user, "Login fehlgeschlagen oder keine Produkte sichtbar")
