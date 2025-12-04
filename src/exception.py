
class UserExistsException(Exception):
    def __repr__(self, email) -> str:
        return f'Пользователь с {email} уже существует'
