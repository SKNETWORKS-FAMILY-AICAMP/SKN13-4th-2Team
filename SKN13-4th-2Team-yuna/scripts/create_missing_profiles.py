from django.contrib.auth.models import User
from mypage.models import Profile

def run():
    users_without_profile = User.objects.filter(profile__isnull=True)
    for user in users_without_profile:
        Profile.objects.create(user=user)
        print(f'Created profile for user: {user.username}')
    print('Finished creating missing profiles.')
