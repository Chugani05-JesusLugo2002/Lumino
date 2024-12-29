from django.http import HttpResponseForbidden


def assert_role(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_profile = args[0].user.profile
            if user_profile.role != role:
                return HttpResponseForbidden(f'You can\'t do that as {user_profile.get_role_display().lower()}!')
            return func(*args, **kwargs)

        return wrapper

    return decorator
