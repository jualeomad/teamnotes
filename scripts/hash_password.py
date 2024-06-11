import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamnotes.settings')
settings.configure()

from django.contrib.auth.hashers import make_password

hashed_password = make_password('test_betis')
print(hashed_password)