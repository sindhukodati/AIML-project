import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2
import os
import csv
import subprocess
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
        
def close_window(event):
    if event.keysym == "space":
        window.destroy()

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

def contact():
    mess._show(title='About Application', message='''
               AN AIML COURSE PROJECT DEVELOPED BY
               
               JAYANTH BOTTU           -   2303A51LA7
               SINDHU KODATI           -   2303A51LA0
               MAHENDRA GADDAM       -   2303A51LA9
               SATHVIKA MUGITHE        -   2303A51LA3
               MARUTHI RAO DAGGU     -   2303A51L98
               ''')

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Error Occured On Your End', message='Please contact us for help !')
        window.destroy()

def how_to():
    mess._show(title='About Application', message='''
                    1) Enter the Application
                    2) Give Input Of ID And Name 
                    3) Take images (wait for 30 seconds, machine will load your image)
                    4) Save Profile 
                    5) Now Click on Take Attendance
                    6) When the Camera pops and identify you, click Space to take attendance
                    ''')

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read() 
    TrainImages()

def clear():
    txt.delete(0, 'end')
    res = "1) Take Images  >>>  2) Save Profile"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1) Take Images  >>>  2) Save Profile"
    message1.configure(text=res)

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                sampleNum = sampleNum + 1

                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])

                cv2.imshow('Taking Images', img)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register First !')
        return
    recognizer.save("TrainingImageLabel\Trainer.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

def getImagesAndLabels(path):

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []

    Ids = []

    for imagePath in imagePaths:

        pilImage = Image.open(imagePath).convert('L')

        imageNp = np.array(pilImage, 'uint8')

        ID = int(os.path.split(imagePath)[-1].split(".")[1])

        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  
    exists3 = os.path.isfile("TrainingImageLabel\Trainer.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainer.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == 32):
            break
    ts = time.time()
    today = datetime.datetime.now().strftime("%d_%m_%Y")
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance.csv")
    if exists:
        with open("Attendance\Attendance.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance.csv", 'r') as csvFile2:
        reader1 = csv.reader(csvFile2)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile2.close()
    cam.release()
cv2.destroyAllWindows()

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

window = tk.Tk()
window.iconbitmap('favicon.ico')
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")

image = Image.open("background.jpg")
width, height = window.winfo_screenwidth(), window.winfo_screenheight()
canvas = tk.Canvas(window, width=width, height=height)
canvas.pack(fill=tk.BOTH, expand=True)
tk_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, image=tk_image, anchor=tk.NW)

frame1 = tk.Frame(window, bg="#BDBAC2")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#BDBAC2")
frame2.place(relx=0.51, rely=0.17, relwidth=0.39, relheight=0.80)
message3 = tk.Label(window, text="Face Recognition And Auto Attendance System" ,fg="black",width=57 ,height=1,font=('Trebuchet MS', 29, ' bold '))

message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.11, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+" ", fg="black",bg="#FFFFFF" ,width=55 ,height=1,font=('comic', 22, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="black",bg="#FFFFFF" ,width=60 ,height=1,font=('comic', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                      For New Registrations                       ", fg="#FFFFFF",bg="#994753" ,font=('Trebuchet MS', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                     For Already Registered                       ", fg="#FFFFFF",bg="#994753" ,font=('Trebuchet MS', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg="#BDBAC2" ,font=('Trebuchet MS', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=32,font=('Trebuchet MS', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="#BDBAC2" ,font=('Trebuchet MS', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32,font=('Trebuchet MS', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1) Take Images  >>>  2) Save Profile" ,bg="#BDBAC2" ,fg="black"  ,width=39 ,height=1, activebackground = "#3ffc00" ,font=('Trebuchet MS', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#BDBAC2" ,fg="black"  ,width=39,height=1, activebackground = "#3ffc00" ,font=('Trebuchet MS', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg="#BDBAC2"  ,height=1 ,font=('Trebuchet MS', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='How to Use ? ', command = how_to)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Options',font=('Trebuchet MS', 29, ' bold '),menu=filemenu)

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

button_background = "#47476b"  
button_text_color = "white"  
active_button_background = "#363656"  
font_family = "Trebuchet MS"  

clear_button1 = tk.Button(
    frame2,
    text="Clear",
    command=clear,
    fg="black",
    bg="#9F8900",
    width=11,
    font=(font_family, 11, "bold"),
)
clear_button1.place(x=335, y=86)

clear_button2 = tk.Button(
    frame2,
    text="Clear",
    command=clear2,
    fg="black",
    bg="#9F8900",
    width=11,
    font=(font_family, 11, "bold"),
)
clear_button2.place(x=335, y=172)

take_image_button = tk.Button(
    frame2,
    text="Take Images",
    command=TakeImages,
    fg=button_text_color,
    bg="#2962ff",  
    width=34,
    height=1,
    activebackground=active_button_background,
    font=(font_family, 15, "bold"),
)
take_image_button.place(x=30, y=300)

train_image_button = tk.Button(
    frame2,
    text="Save Profile",
    command=psw,
    fg=button_text_color,
    bg="#2962ff",
    width=34,
    height=1,
    activebackground=active_button_background,
    font=(font_family, 15, "bold"),
)   
train_image_button.place(x=30, y=380)

track_image_button = tk.Button(
    frame1,
    text="Take Attendance",
    command=TrackImages,
    fg="#000000",
    bg="#00ef00", 
    width=35,
    height=1,

    font=("Trebuchet MS", 15, "bold"),
)
track_image_button.place(x=30, y=50)

quit_button = tk.Button(
    frame1,
    text="Quit",
    command=window.destroy,
    fg=button_text_color,
    bg="#cc0000",  
    width=35,
    height=1,
    activebackground=active_button_background,
    font=(font_family, 15, "bold"),
)
quit_button.place(x=30, y=450)

window.configure(menu=menubar)

window.bind("<KeyPress>", close_window)
window.mainloop()