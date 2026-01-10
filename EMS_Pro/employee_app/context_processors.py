from django.contrib.auth.models import User

def all_users(request):
    users = User.objects.all()

    return {"all_users": users}