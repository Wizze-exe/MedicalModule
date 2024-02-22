
# auth.py

# Место для хранения зарегистрированных пользователей и их паролей
# В реальном приложении пароли должны быть захешированы и храниться в базе данных
USERS = {
    "doctor": "password1",
    "nurse": "password2",
    "admin": "password3"
}


def check_login(username, password):
    """
    Проверяет соответствие логина и пароля зарегистрированным пользователям.
    """
    if username in USERS and USERS[username] == password:
        return True
    return False
