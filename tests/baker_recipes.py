import random
import string

from model_bakery.recipe import Recipe


def get_subject_code():
    return ''.join(random.sample(string.ascii_uppercase, 3))


subject = Recipe(
    'subjects.Subject',
    code=get_subject_code,
)

lesson = Recipe(
    'subjects.Lesson',
    subject__code=get_subject_code,
)

enrollment = Recipe(
    'subjects.Enrollment',
    subject__code=get_subject_code,
)
