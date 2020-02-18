"""

Install latest version psycopg2 with command : pip3 install psycopg2
run the file with command : python problem3.py
and proceed according to instructions

the list indexing is done according to the sequence of table coloumns i have created in database tables

You can create the tables with these commands to make the program work perfectly

CREATE TABLE courses(
id integer PRIMARY KEY,
created_at TIMESTAMP NOT NULL,
name VARCHAR (50) UNIQUE NOT NULL,
capacity integer
prerequisite INTEGER REFERENCES courses(id) ON DELETE SET NULL
);

CREATE TABLE users(
id SERIAL PRIMARY KEY,
created_at TIMESTAMP NOT NULL,
name character(35)
);


CREATE TABLE course_enrollment(
id SERIAL PRIMARY KEY,
created_at TIMESTAMP NOT NULL,
user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE
);

Courses has to created manually by you.I didnt include any code to create a course

if you are trying to create database tables, then please try to change the list indexes i have used

"""

import psycopg2


def get_connection():
    """ function to create a postgres connection """
    try:
        connection = psycopg2.connect(user='postgres',
                                      password='61437',
                                      host='127.0.0.1',
                                      port='5432',
                                      database='usercoursesdb')
        return connection

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting  to PostgreSQL", error)


def register_user(user_name):
    """ function to register a user if user with the same name does not exist """
    user = get_user(user_name.strip())
    # if user already exists
    if user:
        print("User already exists with this name\n"
              "Please enter a unique name\n"
              "or Enter 0 to exit")
        user_name = input("Enter here: ")
        if str(user_name) == '0':
            exit(0)
        # register user if user is willing to create a new account
        # recurring function
        register_user(user_name)

    # get DataBase connection
    conn = get_connection()
    curr = conn.cursor()
    sql = """insert into users(name, created_at) values('{}',NOW())""".format(user_name)
    curr.execute(sql)
    print("Succesfully registered\n"
          "do you want to continue\n"
          "\ntype Y/N")
    decision = input("Enter here :")
    if decision.lower() == 'y' or decision.lower() == 'yes':
        conn.close()
        navigate_users()
    else:
        conn.close()
        exit(0)


def get_user(user_name):
    """ get user from database with given username """
    conn = get_connection()
    curr = conn.cursor()
    sql = """select * from users where name = '{}'""".format(user_name)
    curr.execute(sql)
    user = curr.fetchall()
    conn.close()

    if user:
        return user[0]
    else:
        # if user does not exist
        print("Invalid username.Enroll before accessing\n")
        navigate_users()


def get_all_courses():
    """ function to print all the courses available """
    conn = get_connection()
    curr = conn.cursor()
    sql = "select * from courses order by id asc"
    curr.execute(sql)
    courses = curr.fetchall()
    conn.close()
    print('ID       Course Name\n')
    for course in courses:
        print(course[0], "  -->  ", course[2])


def is_course_available(course_id):
    """ function to check if course has any seat available """
    conn = get_connection()
    curr = conn.cursor()
    sql = "select * from courses where id = {}".format(course_id)
    curr.execute(sql)
    courses = curr.fetchall()
    conn.close()

    if courses[0][3] > 0:
        # returning availability and name
        return True, courses[0][2]
    return False, courses[0][2]


def get_course_prerequisites(course_id):
    """ function to print the prerequisites of a course """
    conn = get_connection()
    curr = conn.cursor()
    sql = """select * from courses where id = {}""".format(course_id)
    curr.execute(sql)
    courses = curr.fetchone()
    course = courses

    courses_list = []
    # lopping through the courses table to get all the prerequisite courses
    print('\nPrerequisite Courses\n')
    while course_id:
        courses_list.append(course[2])
        course_id = course[4]
        if course_id:
            sql = """select * from courses where id = {}""".format(course_id)
            curr.execute(sql)
            course = curr.fetchone()

    for course in courses_list[::-1]:
        print(course)

    conn.close()


def get_user_enrolled_courses(user_name):
    """ function to see how many courses a user has enrolled in """
    user_name = user_name.strip()
    conn = get_connection()
    curr = conn.cursor()
    user = get_user(user_name)
    user_id = user[0]

    sql = """select * from course_enrollment where user_id = {}""".format(user_id)
    curr.execute(sql)
    user_courses = curr.fetchall()

    if len(user_courses) == 0:
        conn.close()
        print("You have currently not enrolled in any courses\n")
        return

    for course in user_courses:
        sql = """select name from courses where id = {}""".format(course[3])
        curr.execute(sql)
        course_name = curr.fetchall()
        print(course_name[0][0])
    conn.close()
    print("\n\n")


def enroll_user_for_course(user_name, course_id):
    """ function to enroll a user for a course if there are seats available in course
    and if user has less then two courses enrolled """

    conn = get_connection()
    curr = conn.cursor()
    user = get_user(user_name)
    user_id = user[0]
    sql = """select * from course_enrollment where user_id = {} and course_id = {}""".format(user_id, course_id)
    curr.execute(sql)
    user_courses = curr.fetchall()

    if user_courses:
        print("You have already enrolled in this course !!\n")
    else:
        sql = """select * from course_enrollment where user_id = {}""".format(user_id)
        curr.execute(sql)
        user_courses = curr.fetchall()
        if len(user_courses) >= 2:
            print("You have already enrolled in two courses."
                  "You cannot join in any other courses"
                  "Thank you.Bye!!!")
            conn.close()
            exit(0)
        else:
            # enroll a user for a particular course
            sql = """insert into course_enrollment(user_id,course_id,created_at) values({},{},NOW())""".format(user_id,
                                                                                                               course_id)
            curr.execute(sql)
            conn.commit()

            # reduce the available seats for a course
            sql = """select capacity from courses where id = {}""".format(course_id)
            curr.execute(sql)
            course_capacity = curr.fetchone()
            capacity = course_capacity[0] - 1

            sql = """update courses set capacity = {} where id = {}""".format(capacity, course_id)
            curr.execute(sql)
            conn.commit()
            conn.close()

            print("\nYou have successfully enrolled in this course.\n")
            navigate_users()
    conn.close()


def navigate_users():
    """ function for user interaction """
    print("welcome! what do you want to do today\n"
          "Enter Related number to select\n"
          "1 : New User ??  Register here !!\n"
          "2 : Enroll for a course\n"
          "3 : See Prerequisites for a course\n"
          "4 : See my courses\n"
          "5 : Exit")

    selection = int(input("Enter here : "))
    if selection == 1:
        print("We need your Name to Register\n"
              "Please enter your name(Must be Unique) :")
        user_name = input("Enter you name here :")
        register_user(user_name)


    elif selection == 2:
        print("We need your Name to Enroll You for a course\n")
        user_name = input("Please enter your registered name here :")

        user = get_user(user_name)
        if not user:
            print("\nUser with name '{}' does not exist.Do you want to register with this name?\n"
                  "Enter Y/Yes to register and continue\n")
            decision = input('Enter here :')

            if decision.lower() == 'y' or decision.lower() == 'yes':
                register_user(user_name)
            else:
                exit(0)

        print("\nselect the course you want to enroll\n"
              'please enter the course ID displayed')
        get_all_courses()

        course_id = input("\nEnter Course id here :")

        print("Checking for Availability to enroll in this course\n")
        available, course_name = is_course_available(course_id)
        if available:
            enroll_user_for_course(user_name, course_id)
        else:
            print("Sorry!!!, the selected {} course does not have any seats available\n".format(course_name))
            navigate_users()

    elif selection == 3:
        print("select the course you want to enroll\n")
        get_all_courses()
        course_id = input("Enter Course id here :")
        get_course_prerequisites(course_id)

    elif selection == 4:
        print("We need your user name to Get the courses")
        user_name = input("Enter you name here :")
        get_user_enrolled_courses(user_name)
        navigate_users()

    elif selection == 5:
        print("see you later.Bye!!!\n")
        exit(0)

    else:
        print("Please Enter Valid Selection Number\n")
        navigate_users()

    return


if __name__ == '__main__':
    navigate_users()
