# DSW-Lumino
Repositorio para el proyecto de Lumino, gestor académico en Django

## Modelos

### Subject
1. Code (Unique) (like PRO, DSW)
2. Name
3. Teacher (FK)
4. Students (ManyToManyField = Enrollment model)

### Lesson
1. Title
2. Content (Null)
3. Subject (FK)

### Profile
1. Role (Enum: Student and Teacher)
2. Avatar
3. User (OneToOneField)

### Enrollment
1. Student (FK -> User)
2. Subject (FK)
3. Mark (Integer, Null)
4. Enrolled_at (DateField with auto_now_add)

## Apps
1. main
2. subjects
3. accounts (manage authentication)
4. lessons
5. users (profile and enrollment models)
6. shared
   
## URLs

1. / -> Redirect a /subjects/
2. /signup, /login, /logout
3. /user/certificate -> Generate and send marks certificat
4. /subjects/enroll/ -> Enroll to subjects form
5. /subjects/unroll/ -> Unroll to subjects form
6. /subjects/<subject_code>/ -> View subject
7. /subjects/<subject_code>/lessons/add/ -> Add lesson
8. /subjects/<subject_code>/lessons/ -> List all lessons from a subject
9. /subjects/<subject_code>/lessons/<lesson_pk>/ -> View lesson detail
10. /subjects/<subject_code>/lessons/<lesson_pk>/edit/ -> Edit lesson
11. /subjects/<subject_code>/lessons/<lesson_pk>/delete/ -> Delete lesson
12. /subjects/<subject_code>/marks/ -> List all students marks
13. /subjects/<subject_code>/marks/add/ -> Add marks to all students
14. /subjects/<subject_code>/marks/edit/ -> Edit marks to all students
15. /subjects/<subject_code>/members/ -> List all students from subject
16. /user/ -> Redirect to my profile
17. /user/edit/ -> Edit profile
18. /users/<username>/ -> View user profile
