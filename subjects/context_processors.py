def subjects(request) -> dict:
    try:
        return {'subjects': request.user.profile.get_subjects()}
    except AttributeError:
        return {}
