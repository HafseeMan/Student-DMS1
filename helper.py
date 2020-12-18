import sqlite3
import re

#1. Defining Lists: editable_tables and table_column
#2. (ADDING RECORD) Validatation

#1
conn = sqlite3.connect('Students.db')
cur = conn.cursor()
cur = conn.cursor()
cur.execute('''
                CREATE TABLE IF NOT EXISTS Students
                (   REG TEXT PRIMARY KEY NOT NULL,
                    FNAME TEXT NOT NULL,
                    LNAME TEXT NOT NULL,
                    AGE INTEGER NOT NULL,
                    EMAIL TEXT,
                    COURSE TEXT,
                    USERNAME TEXT);
            ''')
conn.commit()
print("Database OPENED successfully")
cur = conn.execute('select * from Students')

table_columns = [description[0] for description in cur.description]
editable_columns = table_columns[1:]

#***************************************************************************************************

#2 ADD RECORD VALIDATION

# REG: error if not string and format Uxxx
def add_validation(reg, fn, ln, age, email, course, user, courses_available):

    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    course = course.upper()  # convert course input to uppercase

    # REG: error if not string and format Uxxx
    if (not (isinstance(reg, str))):
       error_message("Invalid REGISTRATION NUMBER. \n(Accepted Format: Uxxx)")

        # FIRST NAME: error if not string and not length 2-15
    elif (not (isinstance(fn, str)) or not (len(fn) < 15 and len(fn) > 2)):
        error_message("Invalid FIRST NAME. \nLength must be 2-15 characters")

        # LAST NAME: error if not string and not length 2-15
    elif (not (isinstance(ln, str)) or not (len(ln) < 15 and len(ln) > 2)):
        error_message("Invalid LAST NAME. \nLength must be 2-15 characters")

        # COURSE: error if not string and not in list
    elif (not (isinstance(course, str)) or course not in courses_available):
        error_message("COURSE picked is NOT AVAILABLE. \nRegister with available options :\n"+str(courses_available))

        # USERNAME: error if not string and not length 2 -15
    elif (not (isinstance(user, str)) or not (len(user) < 15 and len(user) > 2)):
        error_message("Invalid USERNAME. \nLength must be 2-15 characters")

        # EMAIL: error if not string and not correct format
    elif (not re.search(email_regex, email)):
        error_message("Invalid EMAIL")

    else:
        try:
            try:
                age = int(age)  # converting age to integer
            # AGE: error if not an integer
            except Exception as err:
                error_message("Invalid AGE input")

            # AGE: error if age is less than 18
            if (18 > age):
                error_message("UNDER AGE. \n" + "Student " + str(reg) + " must be an adult to qualify")

        #ERROR if student already exists in database
        except Exception as err:
            error_message("ERROR: Student "+ str(reg) + " already exists in database")



def error_message(error):
    return error

def display_command():
    print('d')