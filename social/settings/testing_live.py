from .development import *

# For live test we need "test dict to tell django use file database"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "TEST": {
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
}

# Prevent App registery Error
import django
django.setup()
