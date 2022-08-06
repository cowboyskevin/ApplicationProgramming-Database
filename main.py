#!/usr/bin/python
import sqlite3
from datetime import datetime

#Opens up the database for use in the program.
conn = sqlite3.connect('leopardweb.db')
print("Opened database successfully")
cursor = conn.cursor()

class User: #base class
	def __init__(self,first,last,id):
		self.firstname = first
		self.lastname = last
		self.ID = id

	def printFirstName(self):
		print(self.firstname)

	def printLastName(self):
		print(self.lastname)

	def printID(self):
		print(self.ID)

class instructor(User): #derived class
    def __init__(self, first, last, id):
        super().__init__(first,last,id)
    
    def printRoster(self):
        z = False
        while z == 0:
            print("CRN: ")
            x = input()
            cursor.execute("""SELECT INSTRUCTOR_FIRST FROM COURSE WHERE CRN = '%s' and INSTRUCTOR_FIRST = '%s' """%(x,self.firstname))
            existence = cursor.fetchall()
            if existence:
                z = 1
            else:
                z = 0
                print("That CRN is not valid or you do not teach that course ")
        print("\n Course Roster:\n")
        cursor.execute("SELECT ID FROM STUDENT_COURSE WHERE CRN= %s" "" % (x))
        id_result = cursor.fetchall()
        for i in id_result: # finds the student id of the Student_course table
            cursor.execute("SELECT NAME, SURNAME FROM STUDENT WHERE ID= %s" ""%(i))
            name_result = cursor.fetchall()
            for j in name_result: # finds the student name from Student table
                print(j[0], j[1], "\n")

    def searchCourse(self):
        print("\nCourse List: ")
        cursor.execute("""SELECT * FROM COURSE""")
        course_result = cursor.fetchall()
        for course in course_result:
            if (course[10] == 'YES'):
                day1 = "M "
            else:
                day1 = ""
            if (course[11] == 'YES'):  
                day2 = "T "
            else:
                day2 = ""
            if (course[12] == 'YES'):
                day3 = "W "
            else:
                day3 = ""
            if (course[13] == 'YES'):
                day4 = "TR "
            else:
                day4 = ""
            if (course[14] == 'YES'):
                day5 = "F "
            else:
                day5 = ""
            days = day1 + day2 + day3 + day4 + day5
            print("CRN: ", course[0], "\tDEPARTMENT: ", course[2],"\tTITLE: ", course[1], "\tINSTRUCTOR NAME: ", course[3], " ", course[4], "\tCREDITS: ", course[7], "\tDAYS: ", days, "\tTIME: ", course[8], "-", course[9], "\n")
    
    def searchCourseInput(self):
        print("Search Course By Parameter")
        print("Options:\nCRN\nCOURSE TITLE\nCOURSE DEPARTMENT\nINSTRUCTOR NAME\n")
        print("Enter Search Query: ")
        x = input()
        cursor.execute("""SELECT * 
        FROM COURSE 
        WHERE CRN='%s' OR TITLE='%s' OR DEPARTMENT='%s' OR INSTRUCTOR_FIRST='%s' OR INSTRUCTOR_LAST='%s' OR CREDITS='%s' """% (x, x, x, x, x, x))
        courseInput_result = cursor.fetchall()
        for course in courseInput_result:
            if (course[10] == 'YES'):
                day1 = "M "
            else:
                day1 = ""
            if (course[11] == 'YES'):  
                day2 = "T "
            else:
                day2 = ""
            if (course[12] == 'YES'):
                day3 = "W "
            else:
                day3 = ""
            if (course[13] == 'YES'):
                day4 = "TR "
            else:
                day4 = ""
            if (course[14] == 'YES'):
                day5 = "F "
            else:
                day5 = ""
            days = day1 + day2 + day3 + day4 + day5
            print("CRN: ", course[0], "\tDEPARTMENT: ", course[2],"\tTITLE: ", course[1], "\tINSTRUCTOR NAME: ", course[3], " ", course[4], "\tCREDITS: ", course[7], "\tDAYS: ", days, "\tTIME: ", course[8], "-", course[9], "\n")

    def printSchedule(self):
        cursor.execute("""SELECT TITLE, STARTTIME, ENDTIME, MON, TUES, WED, THUR, FRI 
        FROM COURSE
        WHERE INSTRUCTOR_FIRST = ? and INSTRUCTOR_LAST = ? """, (self.firstname, self.lastname))
        schedule_result = cursor.fetchall()

        print("Semester Course Schedule: ")
        for course in schedule_result:
                if (course[3] == 'YES'):
                    day1 = "M "
                else:
                    day1 = ""
                if (course[4] == 'YES'):  
                    day2 = "T "
                else:
                    day2 = ""
                if (course[5] == 'YES'):
                    day3 = "W "
                else:
                    day3 = ""
                if (course[6] == 'YES'):
                    day4 = "TR "
                else:
                    day4 = ""
                if (course[7] == 'YES'):
                    day5 = "F "
                else:
                    day5 = ""
                days = day1 + day2 + day3 + day4 + day5
                print("TITLE: ", course[0], "\tDAYS: ", days, "\tTIME: ", course[1], "-", course[2], "\n")
 
class student(User): #derived class
    def __init__(self, FirstName, LastName, ID):
        super(student, self).__init__(FirstName, LastName, ID)

    def addCourse(self):
        print("CRN: ")
        x = input()
        cursor.execute(""" SELECT * FROM COURSE WHERE CRN ='%s' """%(x))
        query_result = cursor.fetchall()
        if not query_result:
            x = 0
            print("You have entered the wrong info please try again")
        else:
            cursor.execute("""SELECT * 
            FROM STUDENT_COURSE
            WHERE CRN = ? and ID = ? """ ,(x,self.ID))
            sameCourse_result = cursor.fetchall()

            cursor.execute("""SELECT CRN 
            FROM STUDENT_COURSE
            WHERE ID = '%s' """% (self.ID))
            crn_result = cursor.fetchall()

            if crn_result: 
                for i in crn_result:
                    timeConflict = False
                    checkDay = False
                    courseConflict = False

                    cursor.execute("""SELECT STARTTIME, ENDTIME, MON, TUES, WED, THUR, FRI 
                    FROM COURSE
                    WHERE CRN = ? """ ,(i))
                    schedule_result = cursor.fetchall()

                    start = datetime.strptime(schedule_result[0][0], '%I:%M%p')
                    end = datetime.strptime(schedule_result[0][1], '%I:%M%p')

                    cursor.execute("""SELECT STARTTIME, ENDTIME, MON, TUES, WED, THUR, FRI 
                    FROM COURSE
                    WHERE CRN = ? """ ,(x,))
                    check_result = cursor.fetchall()

                    startCheck = datetime.strptime(check_result[0][0], '%I:%M%p')
                    endCheck = datetime.strptime(check_result[0][1], '%I:%M%p')
                    
                    checkTime = ((startCheck >= start and startCheck <= end) or (endCheck <= end and endCheck >= start))

                    if (x == i[0]):
                        courseConflict = True
                    if ((check_result[0][2]=='YES' and schedule_result[0][2]=='YES') or (check_result[0][3]=='YES' and schedule_result[0][3]=='YES') or (check_result[0][4]=='YES' and schedule_result[0][4]=='YES') or (check_result[0][5]=='YES' and schedule_result[0][5]=='YES') or (check_result[0][6]=='YES' and schedule_result[0][6]=='YES')):
                        checkDay = True
                        if (checkTime and not timeConflict):
                            timeConflict = True

                if(checkDay and timeConflict):
                    if (courseConflict): 
                        print("You have already added this course")
                    else:
                        print("Cannot Add Course: Time Conflict") 
                else:
                    cursor.execute("""INSERT OR IGNORE INTO STUDENT_COURSE VALUES(NULL, ?, ?)""", (x, self.ID))
                    print("\nCourse Added To Schedule")
            else:
                cursor.execute("""INSERT OR IGNORE INTO STUDENT_COURSE VALUES(NULL, ?, ?)""", (x, self.ID))
                print("\nCourse Added To Schedule")
        

    def dropCourses(self):
        print("CRN: ")
        x = input()

        cursor.execute("""SELECT CRN 
        FROM STUDENT_COURSE
        WHERE CRN = ? """ ,(x,))
        crn_result = cursor.fetchall()

        if crn_result:
            cursor.execute("DELETE from STUDENT_COURSE where CRN=? AND ID =?", (x, self.ID))
            print("\n Course Removed From Schedule")
        else:
            print("You Are Not Enrolled In This Course")

    def searchCourse(self):
        print("\nCourse List: ")
        cursor.execute("""SELECT * FROM COURSE""")
        course_result = cursor.fetchall()
        for course in course_result:
            if (course[10] == 'YES'):
                day1 = "M "
            else:
                day1 = ""
            if (course[11] == 'YES'):  
                day2 = "T "
            else:
                day2 = ""
            if (course[12] == 'YES'):
                day3 = "W "
            else:
                day3 = ""
            if (course[13] == 'YES'):
                day4 = "TR "
            else:
                day4 = ""
            if (course[14] == 'YES'):
                day5 = "F "
            else:
                day5 = ""
            days = day1 + day2 + day3 + day4 + day5
            print("CRN: ", course[0], "\tDEPARTMENT: ", course[2],"\tTITLE: ", course[1], "\tINSTRUCTOR NAME: ", course[3], " ", course[4], "\tCREDITS: ", course[7], "\tDAYS: ", days, "\tTIME: ", course[8], "-", course[9], "\n") 
            
    def searchCourseInput(self):
        print("Search Course By Parameter")
        print("Options:\nCRN\nCOURSE TITLE\nCOURSE DEPARTMENT\nINSTRUCTOR NAME\n")
        print("Enter Search Query: ")
        x = input()
        cursor.execute("""SELECT * 
        FROM COURSE 
        WHERE CRN='%s' OR TITLE='%s' OR DEPARTMENT='%s' OR INSTRUCTOR_FIRST='%s' OR INSTRUCTOR_LAST='%s' OR CREDITS='%s' """% (x, x, x, x, x, x))
        courseInput_result = cursor.fetchall()
        for course in courseInput_result:
            if (course[10] == 'YES'):
                day1 = "M "
            else:
                day1 = ""
            if (course[11] == 'YES'):  
                day2 = "T "
            else:
                day2 = ""
            if (course[12] == 'YES'):
                day3 = "W "
            else:
                day3 = ""
            if (course[13] == 'YES'):
                day4 = "TR "
            else:
                day4 = ""
            if (course[14] == 'YES'):
                day5 = "F "
            else:
                day5 = ""
            days = day1 + day2 + day3 + day4 + day5
            print("CRN: ", course[0], "\tDEPARTMENT: ", course[2],"\tTITLE: ", course[1], "\tINSTRUCTOR NAME: ", course[3], " ", course[4], "\tCREDITS: ", course[7], "\tDAYS: ", days, "\tTIME: ", course[8], "-", course[9], "\n")

    def printSchedule(self):
        cursor.execute("""SELECT CRN 
        FROM STUDENT_COURSE
        WHERE ID = '%s' """% (self.ID))
        crn_result = cursor.fetchall()

        for i in crn_result:
            cursor.execute("""SELECT TITLE, INSTRUCTOR_FIRST, INSTRUCTOR_LAST, STARTTIME, ENDTIME, MON, TUES, WED, THUR, FRI
            FROM COURSE
            WHERE CRN = ? """ ,(i))
            schedule_result = cursor.fetchall()

            for course in schedule_result:
                if (course[5] == 'YES'):
                    day1 = "M "
                else:
                    day1 = ""
                if (course[6] == 'YES'):  
                    day2 = "T "
                else:
                    day2 = ""
                if (course[7] == 'YES'):
                    day3 = "W "
                else:
                    day3 = ""
                if (course[8] == 'YES'):
                    day4 = "TR "
                else:
                    day4 = ""
                if (course[9] == 'YES'):
                    day5 = "F "
                else:
                    day5 = ""
                days = day1 + day2 + day3 + day4 + day5
                print("Semester Course Schedule: ")
                print("TITLE: ", course[0], "\tINSTRUCTOR NAME: ", course[1], course[2], "\tDAYS: ", days, "\tTIME: ", course[3], "-", course[4], "\n")

class admin(User): # derived class
    def __init__(self, FirstName, LastName, ID):
        super(admin, self).__init__(FirstName, LastName, ID)

    def addCourseSystem(self):
        print("CRN: ")
        l = input()
        print("Course Title: ")
        m = input()
        print("Department: ")
        n = input()
        print("Instructor First Name: ")
        o = input()
        print("Instructor Last Name: ")
        p = input()
        print("Semester: ")
        q = input()
        print("Year: ")
        r = input()
        print("Credits: ")
        s = input()
        print("Start Time: ")
        t = input()
        print("End Time: ")
        u = input()
        print("Monday (if scheduled for Monday, enter 'YES'): ")
        v = input()
        print("Tuesday (if scheduled for Tuesday, enter 'YES'): ")
        w = input()
        print("Wednesday (if scheduled for Wednesday, enter 'YES'): ")
        x = input()
        print("Thursday (if scheduled for Thursday, enter 'YES'): ")
        y = input()
        print("Friday (if scheduled for Friday, enter 'YES'): ")
        z = input()

        cursor.execute("""INSERT OR IGNORE INTO COURSE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (l, m, n, o, p, q, r, s, t, u, v, w, x, y, z))

        print("\n Course Added To System")

    def dropCourseSystem(self):
        print("Enter CRN To Remove: ")
        x = input()
        cursor.execute("DELETE FROM COURSE WHERE CRN=%s" ""% (x))

        print("\n Course Removed From System")

    def searchCourse(self):
        print("\nCourse List: ")
        cursor.execute("""SELECT * FROM COURSE""")
        course_result = cursor.fetchall()
        for course in course_result:
            if (course[10] == 'YES'):
                day1 = "M "
            else:
                day1 = ""
            if (course[11] == 'YES'):  
                day2 = "T "
            else:
                day2 = ""
            if (course[12] == 'YES'):
                day3 = "W "
            else:
                day3 = ""
            if (course[13] == 'YES'):
                day4 = "TR "
            else:
                day4 = ""
            if (course[14] == 'YES'):
                day5 = "F "
            else:
                day5 = ""
            days = day1 + day2 + day3 + day4 + day5
            print("CRN: ", course[0], "\tDEPARTMENT: ", course[2],"\tTITLE: ", course[1], "\tINSTRUCTOR NAME: ", course[3], " ", course[4], "\tCREDITS: ", course[7], "\tDAYS: ", days, "\tTIME: ", course[8], "-", course[9], "\n")

    def searchCourseInput(self):
        print("Search Course By Parameter")
        print("Options:\nCRN\nCOURSE TITLE\nCOURSE DEPARTMENT\nINSTRUCTOR NAME\n")
        print("Enter Search Query: ")
        x = input()
        cursor.execute("""SELECT * 
        FROM COURSE 
        WHERE CRN='%s' OR TITLE='%s' OR DEPARTMENT='%s' OR INSTRUCTOR_FIRST='%s' OR INSTRUCTOR_LAST='%s' OR CREDITS='%s' """% (x, x, x, x, x, x))
        courseInput_result = cursor.fetchall()
        for course in courseInput_result:
            if (course[10] == 'YES'):
                day1 = "M "
            else:
                day1 = ""
            if (course[11] == 'YES'):  
                day2 = "T "
            else:
                day2 = ""
            if (course[12] == 'YES'):
                day3 = "W "
            else:
                day3 = ""
            if (course[13] == 'YES'):
                day4 = "TR "
            else:
                day4 = ""
            if (course[14] == 'YES'):
                day5 = "F "
            else:
                day5 = ""
            days = day1 + day2 + day3 + day4 + day5
            print("CRN: ", course[0], "\tDEPARTMENT: ", course[2],"\tTITLE: ", course[1], "\tINSTRUCTOR NAME: ", course[3], " ", course[4], "\tCREDITS: ", course[7], "\tDAYS: ", days, "\tTIME: ", course[8], "-", course[9], "\n")
    
    def addStudent():
        print("ID: ")
        i = input()
        print("First Name: ")
        f = input()
        print("Last name: ")
        l = input()
        print("Grad year: ")
        g = input()
        print("Major: ")
        m = input()
        print("Email: ")
        e = input()

        cursor.execute(""""INSERT OR IGNORE INTO STUDENT VALUES(?,?,?,?,?,?)""",(i, f, l, g, m, e))
        print("The student has been added to the database")
    
    def addInstructor(self):
        print("ID: ")
        i = input()
        print("Name: ")
        n = input()
        print("Last name: ")
        l = input()
        print("Title: ")
        t = input()
        print("Hire year: ")
        h = input()
        print("Department: ")
        d = input()
        print("Email")
        e = input()

        cursor.execute("""INSERT OR IGNORE INTO INSTRUCTOR VALUES (?,?,?,?,?,?,?)""" ,(i, n, l, t, h, d, e))
        print("The Instructor has been added to the database")
    
    def linkStudent(self):
        x = 0
        while x == 0:
            print("What is the student's id")
            id = input()
            print("What is the Course CRN")
            crn = input()
            cursor.execute(""" SELECT *
            FROM STUDENT,COURSE
            WHERE STUDENT.ID = '%s' and COURSE.CRN = '%s'
            """ %(id,crn))
            query_result = cursor.fetchall()
            if not query_result:
                print("The Student Id or the CRN is incorrect , isnt correct please enter the correct Id")
            else:
                cursor.execute(""" INSERT OR IGNORE INTO STUDENT_COURSE VALUES (NULL,?,?)""" ,(crn,id))
                print("You have added this student to the course")
                x = 1

    def unlinkStudent(self):
        x = 0
        while x == 0:
                print("What is the student's Id: ")
                id = input()
                print("What is the CRN: ")
                Crn = input()
                cursor.execute(""" SELECT *
                FROM STUDENT_COURSE
                WHERE STUDENT_COURSE.ID = '%s' and STUDENT_COURSE.CRN ='%s' 
                """%(id, Crn))
                query_result = cursor.fetchall()
                if not query_result:
                    x = 0
                    print("You have entered the wrong info please try again")
                else:
                        cursor.execute(""" DELETE FRO6M
                        STUDENT_COURSE WHERE STUDENT_COURSE.ID = '%s' and STUDENT_COURSE.CRN = '%s'
                        """%(id, Crn))
                        print("You have removed this student from this course ")
                        x = 1

    def linkInstructor(self):
        x = 0
        while x == 0:
            print("What is the crn of the class would you like to change the professor for: ")
            crn = input()
            cursor.execute(""" Select *
            FROM COURSE
            WHERE COURSE.CRN = '%s'
            """%(crn))
            query_result = cursor.fetchall()
            if not query_result:
                print("You have entered invalid info ")
            else:
                print("What is the professor's ID that you want to teach this course")
                newProff = input()
                cursor.execute(""" Select INSTRUCTOR.NAME,INSTRUCTOR.SURNAME
                FROM INSTRUCTOR
                WHERE INSTRUCTOR.ID = '%s'  
                """%(newProff))
                query_result = cursor.fetchall()
                print(query_result)
                c = 0
                for a in query_result:
                    for b in a:
                        if c == 0:
                            name = b
                        if c == 1:
                            last_name = b
                        c += 1
                print(name)
                print(last_name)
                print(crn)
                if not query_result:
                    print("You have entered the wrong data please try again")
                    x = 0
                else:
                    cursor.execute("""
                    UPDATE COURSE
                    SET INSTRUCTOR_FIRST = '%s', INSTRUCTOR_LAST = '%s' 
                    WHERE CRN = '%s' """ %(name, last_name, crn))
                    print("You have succesfully changed the professor for this class")
                    x = 1
    def unLinkInstructor(self):
        x = 0
        while x == 0:
            print("What is the crn of the class would you like unlist the professor from: ")
            crn = input()
            cursor.execute(""" Select *
            FROM COURSE
            WHERE COURSE.CRN = '%s'
            """%(crn))
            query_result = cursor.fetchall()
            if not query_result:
                print("You have entered invalid info ")
            else:
                    cursor.execute("""
                    UPDATE COURSE
                    SET INSTRUCTOR_FIRST = 'empty' , INSTRUCTOR_LAST = 'empty'
                    WHERE CRN = '%s' """ %(crn))
                    print("You have succesfully unlisted the professor for this class")
                    x = 1

def checkInstructorPassword(usernames, passwords): #log in for the instructor
        cursor.execute("""Select NAME,SURNAME,ID
        FROM INSTRUCTOR
        WHERE INSTRUCTOR.EMAIL = '%s' and INSTRUCTOR.ID = '%s'""" %(usernames, passwords))
        query_result = cursor.fetchall()
        z = 0
        print(z)
        for x in query_result:
            print(z)
            for y in x:
                if z == 0:
                    firstName = y
                    print(firstName)
                if z == 1:
                    lastName  = y
                    print(lastName)
                if z == 2:
                    id = y
                    print(id)
                z+=1
        if not query_result:
            return 0,0,0
        else:
            print(query_result)
            print("Welcome Instructor")
            x = 1 
            return firstName,lastName,id

def checkStudentPassword(usernames, passwords): #log in for the student
        cursor.execute("""Select NAME,SURNAME,ID
        FROM STUDENT
        WHERE STUDENT.EMAIL = '%s' and STUDENT.ID = '%s'""" %(usernames, passwords))
        query_result = cursor.fetchall()
        z = 0
        print(z)
        for x in query_result:
            print(z)
            for y in x:
                if z == 0:
                    firstName = y
                    print(firstName)
                if z == 1:
                    lastName  = y
                    print(lastName)
                if z == 2:
                    id = y
                    print(id)
                z+=1
        if not query_result:
            return 0,0,0
        else:
            print(query_result)
            print("Welcome Student")
            x = 1 
            return firstName,lastName,id

def checkAdminPassword(usernames, passwords): #log in for the admin
        cursor.execute("""Select NAME,SURNAME,ID
        FROM ADMIN
        WHERE ADMIN.EMAIL = '%s' and ADMIN.ID = '%s'""" %(usernames, passwords))
        query_result = cursor.fetchall()
        z = 0
        #print(z)
        for x in query_result:
            #print(z)
            for y in x:
                if z == 0:
                    firstName = y
                    print(firstName)
                if z == 1:
                    lastName  = y
                    print(lastName)
                if z == 2:
                    id = y
                    print(id)
                z+=1
        if not query_result:
            return 0,0,0
        else:
            print(query_result)
            print("Welcome ADMIN")
            x = 1 
            return firstName,lastName,id

def login(): # function for the log in
    print("Your username is your email")
    print("Your password is your ID number")
    userName = input("Please Enter your Username: ")
    password = input("Please Enter your Password: ") 
    return userName,password
print("Welcome to the Student Database")
z = 0 # this variable controls if the user goes to the next slide
while(z == 0):
    print(" Look at the options below chose from the number 1 -3")
    print("If you are an instructor enter 1 ")
    print("If you are a student enter 2")
    print("If you are an admin enter 3")
    userInput = input("Please enter your option: ")
    print(userInput)
    if userInput not in ['1','2','3']:
        print("That input does not exist")
        inTheWorks = False
        z = 0
    else:
        z = 1 # goes to the next slide if the user enters a valid number
        inTheWorks = 1
y = 1
while  inTheWorks == 1:
    if userInput == '1': # if user selects instructor
        username, passWord = login() #takes the tuple from the login
        firstName,lastName,id  = checkInstructorPassword(username, passWord) # Gives the attributes needed for the instructor class
        if firstName:
            # print(firstName)
            # print(lastName)
            # print(id)
            i = instructor(firstName,lastName, id) # defines the variable j which shows who the instructor is
            while(y == 1):
                print("These are the options which you have")
                print("1. Print class roster")
                print("2. Search all courses")
                print("3. Search by parameter")
                print("4. Print schedule")
                print("5. Log out")
                choice=input()
                if(choice == "1"):
                    i.printRoster()
                elif(choice == "2"):
                    i.searchCourse()
                elif(choice == "3"):
                    i.searchCourseInput()
                elif(choice == "4"):
                    i.printSchedule()
                elif(choice == "5"):
                    y = None
                    inTheWorks = 0
                else:
                    print("That number isn't valid try again: ")
        else:
            print("Wrong username/Password try again") # if incorrect password/username is entered
            username, passWord = login() #takes the tuple from the login
            result = checkInstructorPassword(username, passWord) # checks again to see if the  the login is incorrect
    elif userInput == '2':
        username, passWord = login() #takes the tuple from the login
        firstName,lastName,id  = checkStudentPassword(username, passWord)
        if firstName:
            s = student(firstName,lastName,id)
            while(y == 1):
                print("These are the options that you have")
                print("-------------------------------------")
                print("1. Add course option")
                print("2. Drop course option")
                print("3. Search all Courses")
                print("4. Search by parameter")
                print("5. Print Schedule")
                print("6. Log out")
                print("Select a number: ")
                choice = input()

                if(choice == "1"):
                    s.addCourse()
                elif(choice == "2"):
                    s.dropCourses()
                elif(choice == "3"):
                    s.searchCourse()
                elif(choice == "4"):
                    s.searchCourseInput()
                elif(choice == "5"):
                    s.printSchedule()
                elif(choice == "6"):
                    y = 0
                    inTheWorks = None
                else:
                    print("Invalid choice, try again: ")
        else:
            print("Wrong username/Password try again")# if incorrect password/username is entered
            username, passWord = login() #takes the tuple from the login
            result = checkInstructorPassword(username, passWord)# checks again to see if the  the login is incorrect
    elif userInput == '3':
        username, passWord = login()
        firstName,lastName,id  = checkAdminPassword(username, passWord) #takes the tuple from the login
        if firstName:
            a = admin(firstName,lastName,id)
            while(y == 1):
                print("These are the options that you have")
                print("1. Add course to the system")
                print("2. Drop course from the system")
                print("3. Search all courses")
                print("4. Search by parameter")
                print("5. Remove student from a course")
                print("6. Add student to a course")
                print("7. Add instructor to course")
                print("8. Remove instructor from a course")
                print("9. Log out")
                choice = input()

                if(choice == "1"):
                    a.addCourseSystem()
                elif(choice == "2"):
                    a.dropCourseSystem()
                elif(choice == "3"):
                    a.searchCourse()
                elif(choice == "4"):
                    a.searchCourseInput()
                elif(choice == "5"):
                    a.unlinkStudent()
                elif(choice == "6"):
                    a.linkStudent()
                elif(choice == "7"):
                    a.linkInstructor()
                elif(choice == "8"):
                    a.unLinkInstructor()
                elif(choice == "9"):
                    y = 0
                    inTheWorks = 0 
                    break

                else:
                    print("That number isn't valid try again")
        else:    
                print("Wrong username/Password try again") # if incorrect password/username is entered
                username, passWord = login() #takes the tuple from the login
                result = checkInstructorPassword(username, passWord) 
    else:
        print("That number is not valid")
            
conn.commit()
conn.close()