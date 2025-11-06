import os, sys, django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinak_demo_task.settings")
django.setup()

from django.contrib.auth.models import User

USERNAME = "testuser1"
PASSWORD = "testpass123"

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_user(username=USERNAME, password=PASSWORD)
    print(f"✅ Created user: {USERNAME} / {PASSWORD}")
else:
    print(f"ℹ️ User '{USERNAME}' already exists.")