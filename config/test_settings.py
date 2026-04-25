# Переопределяем базу данных на SQLite in-memory
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Для тестов можно упростить проверку паролей
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",  # быстрее, чем PBKDF2
]
