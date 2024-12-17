from django.http import HttpResponseForbidden


def assert_role(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_profile = args[0].user.profile
            if user_profile.role != role:
                return HttpResponseForbidden()
            return func(*args, **kwargs)

        return wrapper

    return decorator
