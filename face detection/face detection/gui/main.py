# ============================================================
# FACE RECOGNITION ATTENDANCE SYSTEM
# ============================================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd

import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time


# ============================================================
# PATHS
# ============================================================

HAARCASCADE_PATH = "haarcascade_frontalface_default.xml"
STUDENT_DETAILS_PATH = "StudentDetails/StudentDetails.csv"
TRAINING_IMAGE_PATH = "TrainingImage"
TRAINING_LABEL_PATH = "TrainingImageLabel"
TRAINER_PATH = "TrainingImageLabel/Trainner.yml"
PASSWORD_PATH = "TrainingImageLabel/psd.txt"
ATTENDANCE_PATH = "Attendance"


# ============================================================
# CREATE REQUIRED FOLDERS
# ============================================================

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


assure_path_exists("StudentDetails")
assure_path_exists("TrainingImage")
assure_path_exists("TrainingImageLabel")
assure_path_exists("Attendance")


# ============================================================
# LIVE CLOCK
# ============================================================

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(100, tick)


# ============================================================
# CONTACT
# ============================================================

def contact():
    mess.showinfo(
        "Contact Keerthana AJ",
        "Please contact us on: varunkk317@gmail.com"
    )


# ============================================================
# CHECK HAAR CASCADE
# ============================================================

def check_haarcascadefile():
    if os.path.isfile(HAARCASCADE_PATH):
        return True

    mess.showerror(
        "Some file missing",
        "haarcascade_frontalface_default.xml is missing."
    )
    return False


# ============================================================
# SAVE / CHANGE PASSWORD
# ============================================================

def save_pass():
    assure_path_exists(TRAINING_LABEL_PATH)

    if os.path.isfile(PASSWORD_PATH):

        with open(PASSWORD_PATH, "r") as tf:
            key = tf.read()

    else:

        if 'master' in globals():
            master.destroy()

        new_pas = tsd.askstring(
            "Old Password not found",
            "Please enter a new password below",
            show="*"
        )

        if new_pas is None:
            mess.showwarning(
                "No Password Entered",
                "Password not set!! Please try again"
            )
            return

        with open(PASSWORD_PATH, "w") as tf:
            tf.write(new_pas)

        mess.showinfo(
            "Password Registered",
            "New password was registered successfully!!"
        )
        return

    op = old.get()
    newp = new.get()
    nnewp = nnew.get()

    if op == key:

        if newp == nnewp:

            with open(PASSWORD_PATH, "w") as txf:
                txf.write(newp)

            mess.showinfo(
                "Password Changed",
                "Password changed successfully!!"
            )

            master.destroy()

        else:

            mess.showerror(
                "Error",
                "Confirm new password again!!!"
            )

    else:

        mess.showerror(
            "Wrong Password",
            "Please enter correct old password."
        )


def change_pass():

    global master
    global old
    global new
    global nnew

    master = tk.Toplevel(window)

    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="white")

    lbl4 = tk.Label(
        master,
        text="Enter Old Password",
        bg="white",
        font=("times", 12, "bold")
    )
    lbl4.place(x=10, y=10)

    old = tk.Entry(
        master,
        width=25,
        fg="black",
        relief="solid",
        font=("times", 12, "bold"),
        show="*"
    )
    old.place(x=180, y=10)

    lbl5 = tk.Label(
        master,
        text="Enter New Password",
        bg="white",
        font=("times", 12, "bold")
    )
    lbl5.place(x=10, y=45)

    new = tk.Entry(
        master,
        width=25,
        fg="black",
        relief="solid",
        font=("times", 12, "bold"),
        show="*"
    )
    new.place(x=180, y=45)

    lbl6 = tk.Label(
        master,
        text="Confirm New Password",
        bg="white",
        font=("times", 12, "bold")
    )
    lbl6.place(x=10, y=80)

    nnew = tk.Entry(
        master,
        width=25,
        fg="black",
        relief="solid",
        font=("times", 12, "bold"),
        show="*"
    )
    nnew.place(x=180, y=80)

    cancel = tk.Button(
        master,
        text="Cancel",
        command=master.destroy,
        fg="black",
        bg="red",
        height=1,
        width=25,
        activebackground="white",
        font=("times", 10, "bold")
    )
    cancel.place(x=200, y=120)

    save1 = tk.Button(
        master,
        text="Save",
        command=save_pass,
        fg="black",
        bg="#3ece48",
        height=1,
        width=25,
        activebackground="white",
        font=("times", 10, "bold")
    )
    save1.place(x=10, y=120)


# ============================================================
# PASSWORD BEFORE TRAINING
# ============================================================

def psw():

    assure_path_exists(TRAINING_LABEL_PATH)

    if os.path.isfile(PASSWORD_PATH):

        with open(PASSWORD_PATH, "r") as tf:
            key = tf.read()

    else:

        new_pas = tsd.askstring(
            "Old Password not found",
            "Please enter a new password below",
            show="*"
        )

        if new_pas is None:
            mess.showwarning(
                "No Password Entered",
                "Password not set!! Please try again"
            )
            return

        with open(PASSWORD_PATH, "w") as tf:
            tf.write(new_pas)

        mess.showinfo(
            "Password Registered",
            "New password was registered successfully!!"
        )
        return

    password = tsd.askstring(
        "Password",
        "Enter Password",
        show="*"
    )

    if password == key:
        TrainImages()

    elif password is None:
        return

    else:
        mess.showerror(
            "Wrong Password",
            "You have entered wrong password"
        )


# ============================================================
# CLEAR ID
# ============================================================

def clear():
    txt.delete(0, "end")

    res = "1) Take Images  >>>  2) Save Profile"
    message1.configure(text=res)


# ============================================================
# CLEAR NAME
# ============================================================

def clear2():
    txt2.delete(0, "end")

    res = "1) Take Images  >>>  2) Save Profile"
    message1.configure(text=res)


# ============================================================
# TAKE IMAGES
# ============================================================

def TakeImages():

    if not check_haarcascadefile():
        return

    assure_path_exists("StudentDetails")
    assure_path_exists("TrainingImage")

    columns = ["SERIAL NO.", "", "ID", "", "NAME"]

    serial = 0

    if os.path.isfile(STUDENT_DETAILS_PATH):

        with open(STUDENT_DETAILS_PATH, "r", newline="") as csvFile1:

            reader1 = csv.reader(csvFile1)

            for row in reader1:
                serial += 1

        serial = serial // 2

    else:

        with open(
            STUDENT_DETAILS_PATH,
            "a+",
            newline=""
        ) as csvFile1:

            writer = csv.writer(csvFile1)
            writer.writerow(columns)

        serial = 1

    Id = txt.get().strip()
    name = txt2.get().strip()

    if not Id:
        message.configure(text="Enter a valid ID")
        return

    if not name:
        message.configure(text="Enter a valid name")
        return

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():

        mess.showerror(
            "Camera Error",
            "Could not open the camera."
        )
        return

    detector = cv2.CascadeClassifier(HAARCASCADE_PATH)

    sampleNum = 0

    while True:

        ret, img = cam.read()

        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            sampleNum += 1

            filename = (
                f"TrainingImage/"
                f"{name}.{serial}.{Id}.{sampleNum}.jpg"
            )

            cv2.imwrite(
                filename,
                gray[y:y + h, x:x + w]
            )

            cv2.imshow(
                "Taking Images",
                img
            )

        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

        if sampleNum >= 100:
            break

    cam.release()
    cv2.destroyAllWindows()

    res = "Images Taken for ID: " + Id

    row = [
        serial,
        "",
        Id,
        "",
        name
    ]

    with open(
        STUDENT_DETAILS_PATH,
        "a+",
        newline=""
    ) as csvFile:

        writer = csv.writer(csvFile)
        writer.writerow(row)

    message1.configure(text=res)


# ============================================================
# GET IMAGES AND LABELS
# ============================================================

def getImagesAndLabels(path):

    imagePaths = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    faces = []
    Ids = []

    for imagePath in imagePaths:

        try:

            pilImage = Image.open(imagePath).convert("L")

            imageNp = np.array(
                pilImage,
                "uint8"
            )

            ID = int(
                os.path.split(imagePath)[-1].split(".")[1]
            )

            faces.append(imageNp)
            Ids.append(ID)

        except Exception as e:

            print(
                "Skipping image:",
                imagePath,
                e
            )

    return faces, Ids


# ============================================================
# TRAIN IMAGES
# ============================================================

def TrainImages():

    if not check_haarcascadefile():
        return

    assure_path_exists(TRAINING_LABEL_PATH)

    try:

        recognizer = cv2.face.LBPHFaceRecognizer_create()

    except AttributeError:

        mess.showerror(
            "OpenCV Error",
            "cv2.face is not available.\n\n"
            "Install opencv-contrib-python."
        )
        return

    faces, IDs = getImagesAndLabels(
        TRAINING_IMAGE_PATH
    )

    if len(faces) == 0:

        mess.showwarning(
            "No Registrations",
            "Please click Take Images first."
        )
        return

    try:

        recognizer.train(
            faces,
            np.array(IDs)
        )

    except Exception as e:

        mess.showerror(
            "Training Error",
            str(e)
        )
        return

    recognizer.save(TRAINER_PATH)

    res = "Profile Saved Successfully"

    message1.configure(text=res)

    message.configure(
        text="Total Registrations till now: "
        + str(len(set(IDs)))
    )

    mess.showinfo(
        "Training Complete",
        "Profile Saved Successfully"
    )


# ============================================================
# TAKE ATTENDANCE
# ============================================================

def TrackImages():

    if not check_haarcascadefile():
        return

    assure_path_exists("Attendance")
    assure_path_exists("StudentDetails")

    for item in tv.get_children():
        tv.delete(item)

    if not os.path.isfile(TRAINER_PATH):

        mess.showerror(
            "Data Missing",
            "Please register a student and save the profile first."
        )
        return

    if not os.path.isfile(STUDENT_DETAILS_PATH):

        mess.showerror(
            "Details Missing",
            "Student details are missing."
        )
        return

    try:

        recognizer = cv2.face.LBPHFaceRecognizer_create()

    except AttributeError:

        mess.showerror(
            "OpenCV Error",
            "cv2.face is not available.\n\n"
            "Install opencv-contrib-python."
        )
        return

    recognizer.read(TRAINER_PATH)

    faceCascade = cv2.CascadeClassifier(
        HAARCASCADE_PATH
    )

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():

        mess.showerror(
            "Camera Error",
            "Could not open the camera."
        )
        return

    font = cv2.FONT_HERSHEY_SIMPLEX

    df = pd.read_csv(
        STUDENT_DETAILS_PATH
    )

    attendance = None

    while True:

        ret, im = cam.read()

        if not ret:
            break

        gray = cv2.cvtColor(
            im,
            cv2.COLOR_BGR2GRAY
        )

        faces = faceCascade.detectMultiScale(
            gray,
            1.2,
            5
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                im,
                (x, y),
                (x + w, y + h),
                (225, 0, 0),
                2
            )

            serial, conf = recognizer.predict(
                gray[y:y + h, x:x + w]
            )

            if conf < 50:

                name_values = df.loc[
                    df["SERIAL NO."] == serial,
                    "NAME"
                ].values

                id_values = df.loc[
                    df["SERIAL NO."] == serial,
                    "ID"
                ].values

                if len(name_values) > 0:

                    name = str(
                        name_values[0]
                    )

                else:

                    name = "Unknown"

                if len(id_values) > 0:

                    student_id = str(
                        id_values[0]
                    )

                else:

                    student_id = "Unknown"

                ts = time.time()

                date = datetime.datetime.fromtimestamp(
                    ts
                ).strftime("%d-%m-%Y")

                timeStamp = datetime.datetime.fromtimestamp(
                    ts
                ).strftime("%H:%M:%S")

                attendance = [
                    student_id,
                    "",
                    name,
                    "",
                    date,
                    "",
                    timeStamp
                ]

                display_name = name

            else:

                display_name = "Unknown"

            # Display ONLY the name
            cv2.putText(
                im,
                display_name,
                (x, y + h),
                font,
                1,
                (255, 255, 255),
                2
            )

        cv2.imshow(
            "Taking Attendance",
            im
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

    # Save attendance only when a student was recognized
    if attendance is not None:

        student_id = attendance[0]
        name = attendance[2]
        date = attendance[4]
        timeStamp = attendance[6]

        attendance_file = (
            f"Attendance/Attendance_{date}.csv"
        )

        file_exists = os.path.isfile(
            attendance_file
        )

        with open(
            attendance_file,
            "a+",
            newline=""
        ) as csvFile:

            writer = csv.writer(csvFile)

            if not file_exists:

                writer.writerow([
                    "Id",
                    "",
                    "Name",
                    "",
                    "Date",
                    "",
                    "Time"
                ])

            writer.writerow(
                attendance
            )

        message.configure(
            text=f"Attendance marked for {name}"
        )

    # Refresh table
    load_attendance()


# ============================================================
# LOAD ATTENDANCE TABLE
# ============================================================

def load_attendance():

    for item in tv.get_children():
        tv.delete(item)

    today = datetime.datetime.now().strftime(
        "%d-%m-%Y"
    )

    attendance_file = (
        f"Attendance/Attendance_{today}.csv"
    )

    if not os.path.isfile(attendance_file):
        return

    try:

        with open(
            attendance_file,
            "r",
            newline=""
        ) as csvFile:

            reader = csv.reader(csvFile)

            next(reader, None)

            for row in reader:

                if len(row) >= 7:

                    tv.insert(
                        "",
                        0,
                        text=str(row[0]),
                        values=(
                            str(row[2]),
                            str(row[4]),
                            str(row[6])
                        )
                    )

    except Exception as e:

        print(
            "Attendance table error:",
            e
        )


# ============================================================
# DATE
# ============================================================

ts = time.time()

date = datetime.datetime.fromtimestamp(
    ts
).strftime("%d-%m-%Y")

day, month, year = date.split("-")

mont = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}


# ============================================================
# GUI FRONT END
# ============================================================

window = tk.Tk()

window.geometry("1280x720")
window.resizable(True, False)
window.title("Attendance System")
window.configure(
    background="#262523"
)


# ============================================================
# FRAMES
# ============================================================

frame1 = tk.Frame(
    window,
    bg="#00aeff"
)

frame1.place(
    relx=0.11,
    rely=0.17,
    relwidth=0.39,
    relheight=0.80
)


frame2 = tk.Frame(
    window,
    bg="#00aeff"
)

frame2.place(
    relx=0.51,
    rely=0.17,
    relwidth=0.38,
    relheight=0.80
)


# ============================================================
# TITLE
# ============================================================

message3 = tk.Label(
    window,
    text="BMSIT&M Attendance System",
    fg="white",
    bg="#262523",
    width=55,
    height=1,
    font=("times", 29, "bold")
)

message3.place(
    x=10,
    y=10
)


# ============================================================
# DATE AND CLOCK
# ============================================================

frame3 = tk.Frame(
    window,
    bg="#c4c6ce"
)

frame3.place(
    relx=0.52,
    rely=0.09,
    relwidth=0.09,
    relheight=0.07
)


frame4 = tk.Frame(
    window,
    bg="#c4c6ce"
)

frame4.place(
    relx=0.36,
    rely=0.09,
    relwidth=0.16,
    relheight=0.07
)


datef = tk.Label(
    frame4,
    text=day + "-" + mont[month] + "-" + year + "  |  ",
    fg="orange",
    bg="#262523",
    width=55,
    height=1,
    font=("times", 22, "bold")
)

datef.pack(
    fill="both",
    expand=1
)


clock = tk.Label(
    frame3,
    fg="orange",
    bg="#262523",
    width=55,
    height=1,
    font=("times", 22, "bold")
)

clock.pack(
    fill="both",
    expand=1
)

tick()


# ============================================================
# HEADINGS
# ============================================================

head2 = tk.Label(
    frame2,
    text="For New Registrations",
    fg="black",
    bg="#3ece48",
    font=("times", 17, "bold")
)

head2.grid(
    row=0,
    column=0
)


head1 = tk.Label(
    frame1,
    text="For Already Registered",
    fg="black",
    bg="#3ece48",
    font=("times", 17, "bold")
)

head1.place(
    x=0,
    y=0
)


# ============================================================
# ID
# ============================================================

lbl = tk.Label(
    frame2,
    text="Enter ID",
    width=20,
    height=1,
    fg="black",
    bg="#00aeff",
    font=("times", 17, "bold")
)

lbl.place(
    x=80,
    y=55
)


txt = tk.Entry(
    frame2,
    width=32,
    fg="black",
    font=("times", 15, "bold")
)

txt.place(
    x=30,
    y=88
)


# ============================================================
# NAME
# ============================================================

lbl2 = tk.Label(
    frame2,
    text="Enter Name",
    width=20,
    fg="black",
    bg="#00aeff",
    font=("times", 17, "bold")
)

lbl2.place(
    x=80,
    y=140
)


txt2 = tk.Entry(
    frame2,
    width=32,
    fg="black",
    font=("times", 15, "bold")
)

txt2.place(
    x=30,
    y=173
)


# ============================================================
# MESSAGES
# ============================================================

message1 = tk.Label(
    frame2,
    text="1) Take Images  >>>  2) Save Profile",
    bg="#00aeff",
    fg="black",
    width=39,
    height=1,
    font=("times", 15, "bold")
)

message1.place(
    x=7,
    y=230
)


message = tk.Label(
    frame2,
    text="",
    bg="#00aeff",
    fg="black",
    width=39,
    height=1,
    font=("times", 16, "bold")
)

message.place(
    x=7,
    y=450
)


# ============================================================
# ATTENDANCE LABEL
# ============================================================

lbl3 = tk.Label(
    frame1,
    text="Attendance",
    width=20,
    fg="black",
    bg="#00aeff",
    height=1,
    font=("times", 17, "bold")
)

lbl3.place(
    x=100,
    y=115
)


# ============================================================
# TOTAL REGISTRATIONS
# ============================================================

res = 0

if os.path.isfile(STUDENT_DETAILS_PATH):

    try:

        with open(
            STUDENT_DETAILS_PATH,
            "r",
            newline=""
        ) as csvFile1:

            reader1 = csv.reader(csvFile1)

            rows = list(reader1)

            if len(rows) > 1:
                res = len(rows) - 1

    except Exception:
        res = 0


message.configure(
    text="Total Registrations till now: " + str(res)
)


# ============================================================
# MENU BAR
# ============================================================

menubar = tk.Menu(
    window,
    relief="ridge"
)

filemenu = tk.Menu(
    menubar,
    tearoff=0
)

filemenu.add_command(
    label="Change Password",
    command=change_pass
)

filemenu.add_command(
    label="Contact Us",
    command=contact
)

filemenu.add_command(
    label="Exit",
    command=window.destroy
)

menubar.add_cascade(
    label="Help",
    menu=filemenu
)


# ============================================================
# TREEVIEW ATTENDANCE TABLE
# ============================================================

tv = ttk.Treeview(
    frame1,
    height=13,
    columns=("name", "date", "time")
)

tv.column(
    "#0",
    width=82
)

tv.column(
    "name",
    width=130
)

tv.column(
    "date",
    width=133
)

tv.column(
    "time",
    width=133
)

tv.grid(
    row=2,
    column=0,
    padx=(0, 0),
    pady=(150, 0),
    columnspan=4
)

tv.heading(
    "#0",
    text="ID"
)

tv.heading(
    "name",
    text="NAME"
)

tv.heading(
    "date",
    text="DATE"
)

tv.heading(
    "time",
    text="TIME"
)


# ============================================================
# SCROLLBAR
# ============================================================

scroll = ttk.Scrollbar(
    frame1,
    orient="vertical",
    command=tv.yview
)

scroll.grid(
    row=2,
    column=4,
    padx=(0, 100),
    pady=(150, 0),
    sticky="ns"
)

tv.configure(
    yscrollcommand=scroll.set
)


# ============================================================
# BUTTONS
# ============================================================

clearButton = tk.Button(
    frame2,
    text="Clear",
    command=clear,
    fg="black",
    bg="#ea2a2a",
    width=11,
    activebackground="white",
    font=("times", 11, "bold")
)

clearButton.place(
    x=335,
    y=86
)


clearButton2 = tk.Button(
    frame2,
    text="Clear",
    command=clear2,
    fg="black",
    bg="#ea2a2a",
    width=11,
    activebackground="white",
    font=("times", 11, "bold")
)

clearButton2.place(
    x=335,
    y=172
)


takeImg = tk.Button(
    frame2,
    text="Take Images",
    command=TakeImages,
    fg="white",
    bg="blue",
    width=34,
    height=1,
    activebackground="white",
    font=("times", 15, "bold")
)

takeImg.place(
    x=30,
    y=300
)


trainImg = tk.Button(
    frame2,
    text="Save Profile",
    command=psw,
    fg="white",
    bg="blue",
    width=34,
    height=1,
    activebackground="white",
    font=("times", 15, "bold")
)

trainImg.place(
    x=30,
    y=380
)


trackImg = tk.Button(
    frame1,
    text="Take Attendance",
    command=TrackImages,
    fg="black",
    bg="yellow",
    width=35,
    height=1,
    activebackground="white",
    font=("times", 15, "bold")
)

trackImg.place(
    x=30,
    y=50
)


quitWindow = tk.Button(
    frame1,
    text="Quit",
    command=window.destroy,
    fg="black",
    bg="red",
    width=35,
    height=1,
    activebackground="white",
    font=("times", 15, "bold")
)

quitWindow.place(
    x=30,
    y=450
)


# ============================================================
# LOAD TODAY'S ATTENDANCE
# ============================================================

load_attendance()


# ============================================================
# START GUI
# ============================================================

window.configure(
    menu=menubar
)

window.mainloop()