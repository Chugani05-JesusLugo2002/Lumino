import itertools
import random
import string

from faker import Faker
from model_bakery.recipe import Recipe


def product_ascii(*, repeat=1):
    for code in itertools.product(string.ascii_uppercase, repeat=repeat):
        yield ''.join(code)


get_subject_code = product_ascii(repeat=3)
fake = Faker()


subject = Recipe(
    'subjects.Subject',
    code=get_subject_code,
    name=fake.sentence(10),
)

lesson = Recipe(
    'subjects.Lesson',
    content=fake.paragraph(50),
    subject__code=get_subject_code,
)

enrollment = Recipe(
    'subjects.Enrollment',
    mark=lambda: random.randint(1, 10),
    subject__code=get_subject_code,
)
