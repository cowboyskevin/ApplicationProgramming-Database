#!/usr/bin/python
import sqlite3
import unittest
from unittest.mock import patch


conn = sqlite3.connect('assignment3.db')
print("Opened database successfully")
cursor = conn.cursor()

sql_command = """CREATE TABLE IF NOT EXISTSCOURSE(
CRN INTEGER PRIMARY KEY NOT NULL,
TITLE TEXT NOT NULL,
department TEXT NOT NULL,
time TEXT NOT NULL,
days of week TEXT NOT NULL,
semester TEXT NOT NULL,
year INT NOT NULL,
 credits  INT NOT NULL);"""

sql_command = """CREATE TABLE IF NOT EXISTS STUDENT_COURSE (  
INCREMENT INTEGER PRIMARY KEY,
CRN TEXT NOT NULL,
ID TEXT NOT NULL)
;"""
cursor.execute(sql_command) 

sql_command = """CREATE TABLE IF NOT EXISTS INSTRUCTOR_COURSE (  
INCREMENT INTEGER PRIMARY KEY,
CRN TEXT NOT NULL,
ID TEXT NOT NULL)
;"""
cursor.execute(sql_command)

# #cursor.execute("DROP TABLE COURSE")

sql_command = """CREATE TABLE IF NOT EXISTS COURSE (  
CRN TEXT UNIQUE NOT NULL,
TITLE TEXT NOT NULL,
DEPARTMENT TEXT NOT NULL,
INSTRUCTOR_FIRST TEXT NOT NULL,
INSTRUCTOR_LAST TEXT NOT NULL,
TIME TEXT NOT NULL,
DAYS TEXT NOT NULL,
SEMESTER TEXT NOT NULL,
YEAR TEXT NOT NULL,
CREDITS TEXT NOT NULL)
;"""

cursor.execute(sql_command)



#sql_command = """INSERT OR IGNORE INTO COURSE VALUES('1000', 'APPLIED PROGRAMMING CONCEPTS', 'ELEC', 'Joseph', 'Forier', '8:00-9:50', 'MWF', 'SUMMER', 2022, 4);"""
#cursor.execute(sql_command) 

# sql_command = """INSERT OR IGNORE INTO COURSE VALUES('1001', 'SENIOR DESIGN', 'ELEC', 'Patrick', 'Nelson', '10:00-12:50', 'TR', 'SUMMER', 2022, 4);"""
# cursor.execute(sql_command) 
# sql_command = """INSERT OR IGNORE INTO COURSE VALUES('1002', 'Chemistry', 'SCIN', 'Galilei', 'Galileo', '8:00-9:20', 'TR', 'SUMMER', 2022, 4);"""
# cursor.execute(sql_command) 
# sql_command = """INSERT OR IGNORE INTO COURSE VALUES('1003', 'Computer Networks', 'ELEC', 'Alan', 'Turing', '10:00-10:50', 'MWF', 'SUMMER', 2022, 3);"""
# cursor.execute(sql_command) 
# sql_command = """INSERT OR IGNORE INTO COURSE VALUES('1004', 'Youth Development', 'HUS', 'Katie', 'Bouman', '3:00-4:50', 'TR', 'SUMMER', 2022, 4);"""
# cursor.execute(sql_command)

#sql_command = """DELETE FROM STUDENT_COURSE WHERE INCREMENT = 9 """
cursor.execute(sql_command)

def get_input(text):
    return input(text)

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
    
    #print names of all students in a course
    def printRoster(self):
        z = False
        print(self.firstname)
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
                print(j)

    #print list of all courses
    def searchCourse(self):
        print("\nCourse List: ")
        cursor.execute("""SELECT * FROM COURSE""")
        course_result = cursor.fetchall()
        for i in course_result:
            print(i)
    
    #print list of courses found for any user input
    def searchCourseInput(self):
        print("Enter Search Parameter: ")
        x = input()
        cursor.execute("""SELECT * 
        FROM COURSE 
        WHERE CRN='%s' OR TITLE='%s' OR DEPARTMENT='%s' OR INSTRUCTOR_FIRST='%s' OR INSTRUCTOR_LAST='%s' OR TIME='%s' OR DAYS='%s' OR SEMESTER='%s' OR YEAR='%s' OR CREDITS='%s' """% (x, x, x, x, x, x, x, x, x, x))
        courseInput_result = cursor.fetchall()
        for i in courseInput_result:
             print(i)
 
class student(User):
    def __init__(self, FirstName, LastName, ID):
        super(student, self).__init__(FirstName, LastName, ID)

    #add course to student schedule (student_course table)
    def addCourse(self):
        print("CRN: ")
        x = input()
        # print("ID Number: ")
        # y = input()
        cursor.execute("""SELECT CRN 
        FROM STUDENT_COURSE
        WHERE CRN = '%s' and ID = '%s' """% (x,self.ID))
        result = cursor.fetchall()
        if result:
            print("You have already added this course")
            return 0
        else:
            cursor.execute("""INSERT OR IGNORE INTO STUDENT_COURSE VALUES(NULL, ?, ?)""", (x, self.ID))
            print("\nCourse Added To Schedule")
            return 1

    #remove course from student schedule (student_course table)
    def dropCourse(self):
        print("CRN: ")
        x = input()

        cursor.execute("""SELECT CRN 
        FROM STUDENT_COURSE
        WHERE CRN = '%s' and ID = '%s' """% (x,self.ID))
        result = cursor.fetchall()
        if result:
            cursor.execute("DELETE from STUDENT_COURSE where CRN=? AND ID =?", (x, self.ID))
            print("\n Course Deleted From Schedule")
            return 1
        else:
            print("\nYou are not enrolled in this course")
            return 0
        

    #print list of all courses
    def searchCourse(self):
        print("\nCourse List: ")
        cursor.execute("""SELECT * FROM COURSE""")
        course_result = cursor.fetchall()
        for i in course_result:
            print(i)

    #print list of courses found for any user input
    def searchCourseInput(self):
        print("Enter Search Parameter: ")
        x = input()
        cursor.execute("""SELECT * 
        FROM COURSE 
        WHERE CRN='%s' OR TITLE='%s' OR DEPARTMENT='%s' OR INSTRUCTOR_FIRST='%s' OR INSTRUCTOR_LAST='%s' OR TIME='%s' OR DAYS='%s' OR SEMESTER='%s' OR YEAR='%s' OR CREDITS='%s' """% (x, x, x, x, x, x, x, x, x, x))
        courseInput_result = cursor.fetchall()
        for i in courseInput_result:
             print(i)

class admin(User):
    def __init__(self, FirstName, LastName, ID):
        super(admin, self).__init__(FirstName, LastName, ID)

    #add course to system (course table)
    def addCourseSystem():
        print("CRN: ")
        q = input()
        print("Course Title: ")
        r = input()
        print("Department: ")
        s = input()
        print("Instructor First Name: ")
        t = input()
        print("Instructor Last Name: ")
        u = input()
        print("Time: ")
        v = input()
        print("Days: ")
        w = input()
        print("Semester: ")
        x = input()
        print("Year: ")
        y = input()
        print("Credits: ")
        z = input()
        cursor.execute("""INSERT OR IGNORE INTO COURSE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (r, s, t, u, v, w, x, y, z))

        print("\n Course Added To System")

    #remove course from system (course table)
    def dropCourseSystem():
        print("CRN: ")
        x = input()
        
        cursor.execute("""SELECT CRN 
        FROM COURSE
        WHERE CRN = '%s' """% (x))
        result = cursor.fetchall()
        if result:
            cursor.execute("DELETE FROM COURSE WHERE CRN=%s" ""% (x))

            print("\n Course Removed From System")
            return 1
        else:
            print("\nIncorrect CRN")
            return 0

        

    #print list of all courses
    def searchCourse():
        print("\nCourse List: ")
        cursor.execute("""SELECT * FROM COURSE""")
        course_result = cursor.fetchall()
        for i in course_result:
            print(i)

    #print list of courses found for any user input
    def searchCourseInput():
        print("Enter Search Parameter: ")
        x = input()
        cursor.execute("""SELECT * 
        FROM COURSE 
        WHERE CRN='%s' OR TITLE='%s' OR DEPARTMENT='%s' OR INSTRUCTOR_FIRST='%s' OR INSTRUCTOR_LAST='%s' OR TIME='%s' OR DAYS='%s' OR SEMESTER='%s' OR YEAR='%s' OR CREDITS='%s' """% (x, x, x, x, x, x, x, x, x, x))
        courseInput_result = cursor.fetchall()
        for i in courseInput_result:
             print(i)
class Test_Database(unittest.TestCase):
    #@patch (get_input, return_value = 'yes')
    #@patch('builtins.input', lambda _: '1000') # <- value to be returned by input method

    # def test_studentAddCourseWrong(self):
    #     s1 = student("Isaac","Newton",10001)
    #     actual =s1.addCourse() #test with 1000
    #     expected = 0
    #     self.assertEqual(actual, expected)

    # def test_studentAddCourseRight(self):
    #     s1 = student("Isaac","Newton",10001)
    #     inp = '1000'
    #     actual =s1.addCourse() #test with 1004
    #     expected = 1
    #     self.assertEqual(actual, expected)

    # def test_studentDropCourseWrong(self):
    #     s1 = student("Isaac","Newton",10001)
    #     actual =s1.dropCourse() #test with 1003
    #     expected = 0
    #     self.assertEqual(actual, expected)

    # def test_studentDropCourseRight(self):
    #     s1 = student("Isaac","Newton",10001)
    #     actual =s1.dropCourse() #test with 1000
    #     expected = 1
    #     self.assertEqual(actual, expected)

    # def test_adminAddCourseWrong(self):
    #     a1 = admin("Margaret","Hamilton",30001)
    #     actual =a1.addCourseSystem() #test with 1005, Object Oriented Programming, ELEC, Alan, Turing, 12:30-1:50, WF, FALL, 2022, 4
    #     expected = 0
    #     self.assertEqual(actual, expected)

    # def test_adminAddCourseRight(self):
    #     a1 = admin("Margaret","Hamilton",30001)
    #     actual =a1.addCourseSystem() #test with 1005, Object Oriented Programming, ELEC, Alan, Turing, 12:30-1:50, WF, FALL, 2022, 4
    #     expected = 1
    #     self.assertEqual(actual, expected)

    # def test_adminDropCourseWrong(self):
    #     a1 = admin("Margaret","Hamilton",30001)
    #     actual =a1.dropCourseSystem() #test with 1008
    #     expected = 0
    #     self.assertEqual(actual, expected)

    # def test_adminDropCourseRight(self):
    #     a1 = admin("Margaret","Hamilton",30001)
    #     actual =a1.dropCourseSystem() #test with 1004
    #     expected = 1
    #     self.assertEqual(actual, expected)

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
                    lastName = y
                    print(lastName)
                if z == 1:
                    firstName  = y
                    print(firstName)
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

def checkStudentPassword(usernames, passwords): #log in for the instructor
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
                    lastName = y
                    print(lastName)
                if z == 1:
                    firstName  = y
                    print(firstName)
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

def checkAdminPassword(usernames, passwords): #log in for the instructor
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
                    lastName = y
                    print(lastName)
                if z == 1:
                    firstName  = y
                    print(firstName)
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
z = 0
while(z == 0):
    unittest.main()
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
        z = 1
        inTheWorks = True
y = 1
while inTheWorks:
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
                print("If you want to print class  press 1")
                print(" If you want to search all Courses press 2")
                print("If you want to search courses based on parameters press 3")
                print("If you want to log out press 4")
                choice=input()
                if(choice == "1"):
                    i.printRoster()
                elif(choice == "2"):
                    i.searchCourse()
                elif(choice == "3"):
                    i.searchCourseInput()
                elif(choice == "4"):
                    y = None
                    inTheWorks = None
                else:
                    print("That number isn't valid try again")
        else:
            print("Wrong username/Password try again")
            username, passWord = login() #takes the tuple from the login
            result = checkInstructorPassword(username, passWord)
    elif userInput == '2':
        username, passWord = login() #takes the tuple from the login
        firstName,lastName,id  = checkStudentPassword(username, passWord)
        if firstName:
            s = student(firstName,lastName,id)
            while(y == 1):
                print("These are the options that you have")
                print("Add course option press 1")
                print("Drop course option press 2")
                print("Search all Courses press 3")
                print("Search by parameter press 4")
                print("Log out press 5")
                choice = input()
                if(choice == "1"):
                    s.addCourse()
                elif(choice == "2"):
                    s.dropCourses()
                elif(choice == "3"):
                    s.searchCourse()
                elif(choice == "4"):
                    s.searchCourseInput()
                    print("I have been called")
                elif(choice == "5"):
                    y = None
                    inTheWorks = None
                else:
                    print("That number isn't valid try again")
        else:
            print("Wrong username/Password try again")
            username, passWord = login() #takes the tuple from the login
            result = checkInstructorPassword(username, passWord)

    elif userInput == '3':
        username, passWord = login() #takes the tuple from the login
        firstName,lastName,id  = checkAdminPassword(username, passWord)
        if firstName:
            a = admin(firstName,lastName,id)
            while(y == 1):
                print("These are the options that you have")
                print("Add course option press 1")
                print("Drop course option press 2")
                print("Search all Courses press 3")
                print("Search by parameter press 4")
                print("Log out press 5")
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
                    y = None
                    inTheWorks = None
                else:
                    print("That number isn't valid try again")
        else:
            print("Wrong username/Password try again")
            username, passWord = login() #takes the tuple from the login
            result = checkInstructorPassword(username, passWord)
else:
        print("input doesnt exist")

conn.commit()
conn.close()

# python 