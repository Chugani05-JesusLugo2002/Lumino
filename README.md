# DSW-Lumino

## Content
- [Description](#description)
- [Structure](#structure)

## Description
Repositorio para el proyecto de Lumino, gestor académico en Django

## Structure

### Apps
- main
- shared
- users (Profile and Enrollement models)
- accounts => (manage Authentification)
- subjects => (Subject model)
- lessons => (Lesson model)

### Modelos
1. Subjects:
   - Code (Unique) (like PRO, DSW)
   - Name
   - Teacher (FK)
   - Students (ManyToManyField = Enrollment model)

2. Lessons:
   - Title
   - Content (Null)
   - Subject (FK)

3. Profile:
   - Role (Enum: Student and Teacher)
   - User (OneToOneField)
   - Avatar
  
4. Enrollment:
   - Student (FK => User)
   - Subject (FK)
   - Mark (Integer, Null)
     Enrolled_at (DateField with auto_now_add)
   
## URLs
1. Accounts:
   - /login
   - /signup
   - /logout

2. Subjects:
   - /: Home page (Redirect a /subjects/)
   - /subjects/: Redirect from /login
   - /subjects/enroll/: Enroll to subjects form
   - /subjects/unroll/: Unroll to subjects form
   - /subjects/<subject_code>/: View subject
   - /subjects/<subject_code>/marks/: List of all the students and their marks
   - /subjects/<subject_code>/marks/add: Add marks to all the students
   - /subjects/<subject_code>/marks/edit: Edit marks of all the students
   - /subjects/<subject_code>/members/: List of all the students and the teacher from that subject

3. Lessons:
   - /subjects/<subject_code>/lessons/: List of all the lessons from a subject
   - /subjects/<subject_code>/lessons/add/: Add lesson
   - /subjects/<subject_code>/lessons/<lesson_pk>/: View lesson detail
   - /subjects/<subject_code>/lessons/<lesson_pk>/edit/: Edit lesson
   - /subjects/<subject_code>/lessons/<lesson_pk>/delete/: Delete lesson

4. Users:
    - /user/: Redirect to my profile
    - /user/edit: Edit profile
    - /user/certificate/: Generate and send marks certificat
    - /users/<username>/: View profile of other users
