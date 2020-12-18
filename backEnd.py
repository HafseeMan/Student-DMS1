import sqlite3
import re
import helper

class BackEnd:

    def __init__(self):
        self.conn = sqlite3.connect('Students.db')
        self.courses_available = ["BIOLOGY", "COMPUTER SCIENCE", "PHYSICS", "ENGINEERING", "LAW", "ART"]
        self.editable_columns = helper.editable_columns


    def connect(self):
        '''connect to database or creates if not existing'''
        print("Opened student database successfully")
        try:
            cur = self.conn.cursor()
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
            self.conn.commit()
            print("Database OPENED successfully")
        except Exception as err:
            print("Error Connecting to database. ERROR : " + str(err))

    def close(self):
        try:
            self.conn.close()
            print("Database CLOSED successfully")

        except Exception as err:
            print("CLOSE FUNCTION ERROR: " + str(err))

    def add(self, reg, fn, ln, age, email, course, user):
        '''function to add new student to database'''
        '''
        Arguments: 
        reg: REG_NO text,    email: Email Text
        fn: First Name Text, course: Course Text
        ln: Last Name Text,  user: Username Text
        age: Age Integer
        '''

        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        course = course.upper()  # convert course input to uppercase

        # REG: error if not string and format Uxxx
        if (not (isinstance(reg, str))):
            print("Invalid REGISTRATION NUMBER. \t(Accepted Format: Uxxx)")
            print("*** Adding Record Failed ***")

            # FIRST NAME: error if not string and not length 2-15
        elif (not (isinstance(fn, str)) or not (len(fn) < 15 and len(fn) > 2)):
            print("Invalid FIRST NAME. \tLength must be 2-15 characters")
            print("*** Adding Record Failed ***")

            # LAST NAME: error if not string and not length 2-15
        elif (not (isinstance(ln, str)) or not (len(ln) < 15 and len(ln) > 2)):
            print("Invalid LAST NAME. \tLength must be 2-15 characters")
            print("*** Adding Record Failed ***")

            # COURSE: error if not string and not in list
        elif (not (isinstance(course, str)) or course not in self.courses_available):
            print("COURSE picked is NOT AVAILABLE. \tRegister with available options : ")
            print(self.courses_available)
            print("*** Adding Record Failed ***")

            # USERNAME: error if not string and not length 2 -15
        elif (not (isinstance(user, str)) or not (len(user) < 15 and len(user) > 2)):
            print("Invalid USERNAME. \tLength must be 2-15 characters")
            print("*** Adding Record Failed ***")

            # EMAIL: error if not string and not correct format
        elif (not re.search(email_regex, email)):
            print("Invalid EMAIL")
            print("*** Adding Record Failed ***")

        else:
            try:
                try:
                    age = int(age)  # converting age to integer
                # AGE: error if not an integer
                except Exception as err:
                    print("Invalid AGE input" + str(err))

                # AGE: error if age is less than 18
                if (18 > age):
                    print("UNDER AGE. \t" + "Student " + str(reg) + " must be an adult to qualify")
                    print("*** Adding Record Failed ***")

                else:
                    cur = self.conn.cursor()
                    cur.execute("INSERT INTO Students Values (?,?,?,?,?,?,?)", (reg, fn, ln, age, email, course, user))
                    self.conn.commit()
                    print("Record successfully added")

            #ERROR if student already exists in database
            except Exception as err:
                print("ERROR: Student "+ str(reg) + " already exists in database")
                print("*** Adding Record Failed ***")

    def display(self):
        '''function to display all student data'''
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM Students")
            rows = cur.fetchall()
            for row in rows:

                print("REGISTRATION_NUMBER = " + str(row[0]))
                print("NAME = " + str(row[1])+" "+str(row[2]))
                print("AGE = "+ str(row[3]))
                print("EMAIL = "+ str(row[4]))
                print("COURSE = "  + str(row[5]))
                print("USERNAME = " + str(row[6]))
                print("======================================")

        except Exception as err:
            print("DISPLAY ERROR: " + str(err))

    def update(self, reg,targetAttribute,newValue):
        #find data of student with Registration no. = reg, and change the "targetAttribute" to the "newValue"
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        newValue = str(newValue)
        targetAttribute = targetAttribute.upper()

        #CHECK if Reg exists in database
        if reg and reg.strip():
            user_nm = (reg.strip(),)
            query = 'select exists(select 1 from Students where REG=? collate nocase) limit 1'
            # 'query' RETURNS 1 IF REG EXISTS OR 0 IF NOT, AS INTEGER(MAYBE). 'collate nocase'= CASE INSENSITIVE, IT'S OPTIONAL
            check = cur.execute(query, user_nm)
            if check.fetchone()[0] == 0:
                print('Registration_Number NOT found')
                print("*** Update Record Failed ***")
            else:
                print('Registeration_Number found')

                #Conditional operations and validation for targetAttribute
                if (targetAttribute == "FNAME"):
                    # FIRST NAME: error if not length 2-15
                    if (not (isinstance(newValue, str)) or not (len(newValue) < 15 and len(newValue) > 2)):
                        print("Invalid FIRST NAME. \tLength must be 2-15 characters")
                        print("*** Updating Record Failed ***")

                    else: #FIRST NAME Update
                        cur.execute("UPDATE Students set FNAME = ? where REG= ?", (newValue, reg))
                        self.conn.commit()
                        print("*** Update Record Successful ***")

                elif (targetAttribute == "LNAME"):
                    # LAST NAME: error if not length 2-15
                    if (not (isinstance(newValue, str)) or not (len(newValue) < 15 and len(newValue) > 2)):
                        print("Invalid LAST NAME. \tLength must be 2-15 characters")
                        print("*** Updating Record Failed ***")

                    else: #LAST NAME Update
                        cur.execute("UPDATE Students set LNAME = ? where REG= ?", (newValue, reg))
                        self.conn.commit()
                        print("*** Update Record Successful ***")

                elif (targetAttribute == "AGE"):
                    try:
                        newValue = int(newValue)
                    # AGE: error if not an integer
                    except Exception as err:
                        print("Invalid AGE input" + str(err))
                        print("*** Update Record Failed ***")

                    # AGE: error if age is less than 18
                    if (18 > newValue):
                        print("UNDER AGE. \t" + "Student " + str(targetAttribute) + " must be an adult to qualify")
                        print("*** Update Record Failed ***")
                    else: #Age Update
                        cur.execute('UPDATE Students SET AGE=? WHERE REG= ?', (newValue, reg))
                        self.conn.commit()
                        print("*** Update Record Successful ***")

                elif (targetAttribute == "EMAIL"):
                    newValue = str(newValue)
                    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w{2,3}$'

                    # EMAIL: error if not correct format
                    if (not (isinstance(newValue, str))):  # not (or re.search(email_regex,email))):
                        print("Invalid EMAIL")
                        print("*** Update Record Failed ***")

                    else: #EMAIL Update
                        cur.execute('UPDATE Students SET EMAIL=? WHERE REG= ?', (newValue, reg))
                        self.conn.commit()
                        print("*** Update Record Successful ***")

                elif (targetAttribute == "COURSE"):
                    # COURSE: error if not string and not in list
                    if (newValue not in self.courses_available):
                        print("COURSE picked is NOT AVAILABLE. \tRegister with available options : ")
                        print(self.courses_available)
                        print("*** Update Record Failed ***")

                    else: #Course Update
                        cur.execute('UPDATE Students SET COURSE=? WHERE REG= ?', (newValue, reg))
                        self.conn.commit()
                        print("*** Update Record Failed ***")

                elif (targetAttribute == "USER"):
                    #USERNAME: error if not length 2-15
                    if (not (len(newValue) < 15 and len(newValue) > 2)):
                        print("Invalid USERNAME. \tLength must be 2-8 characters")
                        print("*** Update Record Failed ***")

                    else: #USERNAME Update
                        cur.execute('UPDATE Students SET USER=? WHERE REG= ?', (newValue, reg))
                        self.conn.commit()
                        print("*** Update Record Successful ***")

                else:
                    print("Columnn Selected does not exist. \tAvailable columns: " + str(self.editable_columns))
                    print("*** Update Record Failed ***")


        else:
            print('Error')

    def delete(self, reg):
        '''function to delete student from database'''
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM Students WHERE REG=?",(reg,))
            self.conn.commit()
            print("Student "+reg+" deleted")

        except Exception as err:
            print("DELETE FUNCTION ERROR : "+ str(err))
