import mysql.connector
from tkinter import *
from tkinter import messagebox
import datetime
import cv2
import os
import numpy as np
import face_recognition
import cv2.face
from calendar import month_name


# connect to the MySQL database and create the attendance table
mydb = mysql.connector.connect(
    host="localhost", user="root", password="", database="python_database")
if mydb.is_connected():
    print('Connection successful')

mycursor = mydb.cursor()
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS attendance (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), present BOOLEAN,date DATE DEFAULT CURRENT_DATE)")


# function to mark attendance manually
def mark_attendance():
    # create a GUI with a dropdown box to select a division
    root = Tk()
    root.title("Mark Attendance Manually")
    root.geometry("500x500")

    division_label = Label(root, text="Select Division:")
    division_label.pack()

    division_var = StringVar()
    division_dropdown = OptionMenu(root, division_var, "IT", "CE")
    division_dropdown.pack()

    # create a list of students based on the selected division
    students_label = Label(root, text="Students:")
    students_label.pack()

    students_frame = Frame(root)
    students_frame.pack()

    students = []

    def create_student_checkbox(name):
        var = IntVar()
        checkbox = Checkbutton(students_frame, text=name, variable=var,
                               command=lambda: update_student_checkbox(name, var))
        checkbox.pack(side=TOP, anchor=W)
        students.append((name, var))

    def update_student_checkbox(name, var):
        for i, student in enumerate(students):
            if student[0] == name:
                students[i] = (name, var)
                var.set(1)
                print(name, var.get())

    def update_students_list(*args):
        # create a new list of students based on the selected division
        division = division_var.get()

        if division == "IT":
            names = ["Prem", "Ram", "Sam"]
        elif division == "CE":
            names = ["Sakun", "Sabin", "Pawan", "Gopal", "Jiwan", "Shyam"]
        # elif division == "CED":
        #     names = ["Haari", "Ram", "Kelzang", "Tashi", "kinley", "Arun"]
        else:
            names = []

        for widget in students_frame.winfo_children():
            widget.destroy()

        students.clear()
        for name in names:
            create_student_checkbox(name)

    division_var.trace_add("write", update_students_list)

    def save_attendance():
        print(students)  # check if the data is being retrieved properly

        # create a table for the attendance data
        mycursor = mydb.cursor()
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS attendance (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), present BOOLEAN, date DATE DEFAULT CURRENT_DATE)")

        # insert or update the attendance data for the selected students
        for name, var in students:
            present = var.get()
            # check if the data is being retrieved properly
            print(name, present)
            if present:
                # check if attendance for the current student and date already exists
                mycursor.execute(
                    "SELECT * FROM attendance WHERE name = %s AND date = %s", (name, datetime.date.today()))
                result = mycursor.fetchone()
                if result:
                    # update the existing record
                    sql = "UPDATE attendance SET present = %s WHERE id = %s"
                    val = (True, result[0])
                    mycursor.execute(sql, val)
                    messagebox.showinfo("Attendance updated", "Attendance records for today updated")

                else:
                    # insert a new record
                    sql = "INSERT INTO attendance (name, present) VALUES (%s, %s)"
                    val = (name, True)
                    mycursor.execute(sql, val)
                    messagebox.showinfo("Attendance Taken", "Today's attendance has been taken")

            root.destroy()

        # commit the changes to the database and close the connection
        mydb.commit()
        mydb.close()

    save_button = Button(root, text="Save Attendance", command=save_attendance)
    save_button.pack()
    root.mainloop()

########### Camera ##########


def camera_attendance():

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer1 = cv2.face.LBPHFaceRecognizer_create()
    recognizer1.read("trainer1.yml")
    recognizer2 = cv2.face.LBPHFaceRecognizer_create()
    recognizer2.read("trainer2.yml")
    recognizer3 = cv2.face.LBPHFaceRecognizer_create()
    recognizer3.read("trainer3.yml")
    cap = cv2.VideoCapture(0)

    # Increase the brightness of the video
    brightness = 50
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness / 100)

    # Create a CLAHE object (Arguments are optional).
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    while True:
        ret, frame = cap.read()

        # Apply contrast-limited adaptive histogram equalization to the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = clahe.apply(gray)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            id_1, conf_1 = recognizer1.predict(roi_gray)
            id_2, conf_2 = recognizer2.predict(roi_gray)
            id_3, conf_3 = recognizer3.predict(roi_gray)

            if conf_1 >= 45 and conf_1 <= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = "Sakun"
                color = (0, 255, 0)

                # Insert the student's name into the attendance table
                mycursor.execute(
                    "SELECT * FROM attendance WHERE name = %s AND date = %s", (name, datetime.date.today()))
                result = mycursor.fetchall()
                if result:
                    messagebox.showinfo("Attendance already taken", "Attendance for Sakun has already been taken for today.")
                    cap.release()
                    cv2.destroyAllWindows()

                elif not result:
                    sql = "INSERT INTO attendance (name, present) VALUES (%s, %s)"
                    val = (name, True)
                    mycursor.execute(sql, val)
                    mydb.commit()  # commit the changes to the database
                    messagebox.showinfo("Attendance taken", "Attendance for Sakun has been taken.")
                    cap.release()
                    cv2.destroyAllWindows()

                # Draw a rectangle around the detected face and display the name
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, name, (x, y-10), font, 1, color, 2)

            elif conf_2 >= 45 and conf_2 <= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = "Pawan"
                color = (0, 255, 0)

                # Insert the student's name into the attendance table
                mycursor.execute(
                    "SELECT * FROM attendance WHERE name = %s AND date = %s", (name, datetime.date.today()))
                result = mycursor.fetchall()
                if result == 1:
                    messagebox.showinfo("Attendance already taken", "Attendance for Pawan has already been taken for today.")
                    cap.release()
                    cv2.destroyAllWindows()

                elif not result:
                    sql = "INSERT INTO attendance (name, present) VALUES (%s, %s)"
                    val = (name, True)
                    mycursor.execute(sql, val)
                    mydb.commit()  # commit the changes to the database
                    messagebox.showinfo("Attendance taken", "Attendance for Pawan has been taken.")
                    cap.release()
                    cv2.destroyAllWindows()
                
            elif conf_3 >= 45 and conf_3 <= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = "Prem"
                color = (0, 255, 0)

                # Insert the student's name into the attendance table
                mycursor.execute(
                    "SELECT * FROM attendance WHERE name = %s AND date = %s", (name, datetime.date.today()))
                result = mycursor.fetchall()
                if result == 1:
                    messagebox.showinfo("Attendance already taken", "Attendance for Pawan has already been taken for today.")
                    cap.release()
                    cv2.destroyAllWindows()

                elif not result:
                    sql = "INSERT INTO attendance (name, present) VALUES (%s, %s)"
                    val = (name, True)
                    mycursor.execute(sql, val)
                    mydb.commit()  # commit the changes to the database
                    messagebox.showinfo("Attendance taken", "Attendance for Prem has been taken.")
                    cap.release()
                    cv2.destroyAllWindows()

                # Draw a rectangle around the detected face and display the name
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, name, (x, y-10), font, 1, color, 2)

            else:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = "Unknown"
                color = (0, 0, 255)

                # Draw a rectangle around the detected face and display the name
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, name, (x, y-10), font, 1, color, 2)

        # Display the video
        cv2.imshow('video', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.imshow("Attendance", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def show_attendance():
    # retrieve the attendance data from the MySQL database
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT name, MONTHNAME(date), COUNT(*) FROM attendance GROUP BY name, MONTH(date)")
    rows = mycursor.fetchall()

    # display the attendance data in a GUI
    root = Tk()
    root.title("Attendance Report")
    root.geometry("500x500")

    attendance_label = Label(root, text="Attendance:")
    attendance_label.pack()

    attendance_frame = Frame(root)
    attendance_frame.pack()

    for row in rows:
        name_label = Label(attendance_frame, text=row[0])
        name_label.grid(row=rows.index(row), column=0)

        month_label = Label(attendance_frame, text=row[1])
        month_label.grid(row=rows.index(row), column=1)

        total_label = Label(attendance_frame, text=row[2])
        total_label.grid(row=rows.index(row), column=2)

    root.mainloop()


# create a main GUI that has buttons to mark attendance manually, mark attendance with camera, and show attendance
root = Tk()
root.title("Attendance System")
root.geometry("500x500")

attendance_label = Label(root, text="Attendance System With Three Options:")
attendance_label.pack()

manual_button = Button(
    root, text="Mark Attendance Manually", command=mark_attendance)
manual_button.pack()

camera_button = Button(
    root, text="Mark Attendance with Camera", command=camera_attendance)
camera_button.pack()

show_button = Button(root, text="Show Attendance", command=show_attendance)
show_button.pack()

root.mainloop()
