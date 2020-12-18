from backEnd import BackEnd

interface = BackEnd()

interface.connect()

print("******* WELCOME TO SCA STUDENT DATABASE ********")

def print_options():
    try:
        option = input("PICK A NUMBER : \n1. Display ALL Students Records \n2. Add NEW Student record \n3. Update EXISTING Student Record \n4. Delete Student Record ")
        print("************************************************")
        option = int(option)

        if(option >4 or option<1):
            print("WRONG INPUT. TRY AGAIN")
            print_options()

        elif(option == 1):
            print("*************** DISPLAYING ALL RECORDS IN STUDENTS DATABASE *******************")
            interface.display()

        elif(option == 2):
            print("*************** ADDING NEW RECORD TO STUDENTS DATABASE *******************")
            reg = input("REGISTRATION NUMBER : ")
            fn = input("FIRST NAME : ")
            ln = input("LAST NAME : ")
            age = input("AGE : ")
            email = input("EMAIL : ")
            course = input("COURSE : ")
            user = input("USERNAME : ")

            interface.add(reg,fn,ln,age,email,course,user)

        elif(option == 3):
            print("*************** UPDATING EXISTING STUDENT RECORD IN DATABASE *******************")
            reg = input("REGISTRATION NUMBER : ")
            print("Fields in table : " + str(interface.table_columns))
            targetAttribute = input("FIELD TO UPDATE : ")
            newValue = input("( "+ targetAttribute + ") NEW VALUE : ")

            interface.update(reg,targetAttribute,newValue)

        else:
            print("*************** DELETING STUDENT RECORD FROM DATABASE *******************")
            reg = input("REGISTRATION NUMBER: ")
            interface.delete(reg)

    except Exception as err:
        print("WRONG INPUT. TRY AGAIN")
        print(str(err))
        print_options()

print_options()
interface.close()
