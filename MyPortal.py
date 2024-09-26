# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 12:43:30 2024

@author: ssvai
"""
import mysql.connector as sqltor

def HomePg():
    while True:
        usertype= int(input("Enter 1 for student and 2 for admin. "))
        if usertype==1:
            print ("\n\nStudent Login")
            StudentLogin()
        elif usertype==2:
            print("\n\nAdmin login")
            AdminLogin()


def EstablishConnection():
    mycon= sqltor.connect(user='admin',
                           password='admin',
                           host='127.0.0.1',
                           database= 'TechSok')
    if mycon.is_connected()== False:
        print ("Error Connection failed")
        return None
    else:
        return mycon
    
    
            
def AdminLogin():
    mycon= EstablishConnection()
    
    if mycon!=None:
        backtohomepg= False
        while backtohomepg==False:
            A_ID= int(input("Enter ID: "))
            Password= input("Enter Password: ")
            
            cursor= mycon.cursor()
            st= "SELECT * FROM aidnp;"
            cursor.execute(st)
            
            while True:
                row= cursor.fetchone()
                
                if row==None:
                    print("Invalid user Id or Password@")
                    x= int( input("To return to home pg type 10, otherwise type 20"))
                    if x==10:
                        backtohomepg=True
                    break
                elif row[0]==A_ID and row[1]==Password:
                    print ("You have logged in.")
                    #Next pg
                    while True:
                        x= int(input("Enter 1 to add courses, 2 to add marks, anything else to exit"))
                        if x==1:
                            AddCourse()
                        elif x==2:
                            AddMarks()
                        else:
                            print('Exited')
                            break
                    backtohomepg= True
                    break
    mycon.close()


def AddCourse():
    mycon= EstablishConnection()
    if mycon!= None:
        branch= str( input("Enter branch: "))
        sem= str(input("Enter semester: "))
        batch= input("Enter batch in the format 2024_2028: ")
        cursor= mycon.cursor()
                
        st1= "CREATE TABLE {}_{}_{} (StudentID int);".format(batch, branch, sem)
        cursor. execute(st1)
        mycon.commit()
        
        st2= "SELECT StudentID FROM studentinfo WHERE Branch='{}' AND Batch='{}'; ".format(branch, batch)
        cursor.execute(st2)
        
        #input students
        data= cursor.fetchall()
        for i in data:
            s_id= i[0]
            st3= "INSERT INTO {}_{}_{} VALUES({});".format(batch,branch,sem,s_id)
            cursor.execute(st3)
        mycon.commit()
        
        #input courses
        num= int(input("number of courses: "))
        for i in range(1, (num+1)):
            c= input("Enter course name: ")
            st= ("ALTER TABLE {}_{}_{} ADD {} INT;").format(batch,branch,sem,c)
            cursor.execute(st)
        
        mycon.commit()
        mycon.close()

def AddMarks():
    mycon= EstablishConnection()
    if mycon!= None:
        branch= input("Enter branch: ")
        sem= input("Enter semester: ")
        batch= input("Enter batch in the format 2024-2028: ")
        course= input('Enter course: ')
        cursor= mycon.cursor()
        st1= "SELECT StudentID FROM {}_{}_{};".format(batch,branch,sem)
        cursor.execute(st1)
        StudentsList= cursor.fetchall()
        print ("The ID's of the students taking this course are \n", StudentsList)
        another=1
        Found= False
        
        #Checks if student id id there for the course 
        # and enters marks if its there
        while another==1:
            s_id= int(input("Enter studentid: "))
            Found=False
            for i in StudentsList:
                if s_id==i[0]:
                    marks= int(input("Enter marks: "))
                    
                    st= "UPDATE {}_{}_{} SET {}={} WHERE StudentID= {};".format(batch,branch,sem,course,marks,s_id)
                    cursor.execute(st)
                    mycon.commit()
                    
                    another=int(input("To enter another students marks (of the same batch and branch) type 1 else type 0. "))
                    Found=True
                    break 
            
            if Found==False:
                print ("Invalid Student ID")
                another=int(input("To enter another students marks (of the same batch and branch) type 1 else type 0. "))
            
        mycon.close()

def StudentLogin():
    mycon= EstablishConnection()
    
    if mycon!=None:
        backtohomepg= False
        while backtohomepg==False:
            S_ID= int( input("Enter ID: "))
            Password= input("Enter Password: ")
            
            cursor= mycon.cursor()
            st= "SELECT * FROM sidnp;"
            cursor.execute(st)
            
            while True:
                row= cursor.fetchone()
                if row==None:
                    print("Invalid user Id or Password!")
                    x= int( input("To return to home pg type 10, otherwise type 20. "))
                    if x==10:
                        backtohomepg=True
                    break
                elif row[0]==S_ID and row[1]==Password:
                    print ("You have logged in.\n \n \n Veiw Marks")
                    CheckAnotherSem= True
                    while CheckAnotherSem== True:
                        ViewMarks(S_ID)
                        x= int( input("To return to home pg type 10, to check another semesters marks type 20: "))
                        if x==10:
                            backtohomepg=True
                            CheckAnotherSem=False
                    break
                    
        mycon.close()


def CalcSPI(ID, batch, branch, sem):
    mycon= EstablishConnection()
    cursor=mycon.cursor()
    st= "SELECT * FROM {}_{}_{} WHERE StudentID={};".format(batch,branch,sem,ID)
    cursor.execute(st)
    marks= cursor.fetchone()
    
    st2= "DESC {}_{}_{};".format(batch, branch, sem)
    cursor.execute(st2)
    data= cursor.fetchall()
    
    Sum=0
    for i in range (1, len(marks)):
        if marks[i]==None:
            print("U have a backlog in ",data[i][0], "in sem ", sem)
        else:
            Sum +=marks[i]
    SPI= Sum/ (len(marks)-1)
    mycon.close()
    return SPI

def CalcCPI(ID, CurrentSem, batch, branch):
    mycon= EstablishConnection()
    cursor=mycon.cursor()
    
    st2= "SELECT CurrentSem from studentinfo WHERE StudentID= {};". format(ID)
    cursor.execute(st2)
    CS= cursor.fetchone()
    CurrentSem= CS[0]
    if CurrentSem==1:
        return -1
    sum=0
    for i in range (1, CurrentSem):
        SPI= CalcSPI(ID, batch, branch, i)
        sum+= SPI
    CPI= sum/ (CurrentSem-1 )
    mycon.close()
    return CPI
    

def ViewMarks(ID):
    mycon= EstablishConnection()
    cursor=mycon.cursor()
    st1= "SELECT * FROM studentinfo WHERE StudentID= {}".format(ID)
    cursor.execute(st1)
    s_info= cursor.fetchone()
    studID= s_info[0]
    name= s_info[1]
    branch= s_info[2]
    batch= s_info[3]
    CurrentSem= s_info[4]
    #print details
    print ("ID- ", ID)
    print ("Name- ", name)
    print ("Branch- ", branch)
    print ("Batch- ", batch)
    print ("Current sem- ", CurrentSem)
    
    sem= input("Which SEM'S marks do you want to check. Enter NUMBER: ")
    
    st= "SELECT * FROM {}_{}_{} WHERE StudentID={};".format(batch,branch,sem,ID)
    cursor.execute(st)
    marks= cursor.fetchone()
    
    st2= "DESC {}_{}_{};".format(batch, branch, sem)
    cursor.execute(st2)
    data= cursor.fetchall()
    
    for i in range (1, len(marks)):
        print (data[i][0], ":", marks[i])
        
    print( "SPI : ", CalcSPI(ID, batch, branch, sem))
    print ("-------\t--------\t--------\t--------\t-------")
    CPI= CalcCPI(ID, CurrentSem, batch, branch)
    if CPI==-1:
        print ("No CPI assigned yet as you are still in your first sem")
    else:
        print ("CPI: ", CPI)
    mycon.close()
            
#Create student sign up, UPDATE password for both admins an students   

HomePg()

        
    
        
        
            

    
    
                
        
