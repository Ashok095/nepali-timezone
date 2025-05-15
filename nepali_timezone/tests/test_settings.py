SECRET_KEY = "test-secret"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.admin",
    "rest_framework",
    "nepali_timezone",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
TIME_ZONE = "Asia/Kathmandu"