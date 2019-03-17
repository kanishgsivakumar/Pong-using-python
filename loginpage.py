import libs.login_module as lm
import tkinter as tk
from PIL import Image,ImageTk


def display(msg):
    label_info['text']= msg

def log():
    logged_in = lm.login(text_userid.get(1.0,"end-1c"),text_password.get(1.0,"end-1c"))
    if(logged_in):
        display("you are logged in as\t" + text_userid.get(1.0,"end-1c"))
    else:
        display("incorrect crediantials. please try again")
def reg():
    
    reg_state = lm.register(text_userid.get(1.0,"end-1c"),text_password.get(1.0,"end-1c"))
    if reg_state:
        log()
    else:
        display("oops! Error 404 ")
def asGuest():
    display("Logged in as Guest")

pad = (5,5)
root = tk.Tk()
root.geometry()
root.minsize(width=200,height=200)
frame = tk.Frame(root )
button_frame1 = tk.Frame(frame)
button_frame2 = tk.Frame(frame)
user_frame = tk.Frame(frame)
password_frame = tk.Frame(frame)
label_info = tk.Label(root)
label_userid = tk.Label(user_frame,text = "User ID",width = 10)
label_password = tk.Label(password_frame,text = "Password",width = 10)
text_userid = tk.Text(user_frame,height = 1,width = 10)
text_password = tk.Text(password_frame,height = 1,width = 10)
button_login = tk.Button(button_frame1 ,text = "Login",width = 8,command= log)
button_register = tk.Button(button_frame1,text = "Register",width = 8,command = reg )
button_guest = tk.Button(button_frame2,text = "Login as Guest",width = 20,command = asGuest)

frame.place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)
user_frame.pack(side = tk.TOP,padx = pad,pady = pad)
password_frame.pack(side = tk.TOP,padx = pad,pady = pad)
button_frame2.pack(side = tk.BOTTOM,padx = pad,pady = pad)
button_frame1.pack(side = tk.BOTTOM,padx = pad,pady = pad)
label_userid.pack(side = tk.LEFT,padx = pad,pady = pad)
text_userid.pack(side = tk.RIGHT,padx = pad,pady = pad)
label_password.pack(side = tk.LEFT,padx = pad,pady = pad)
text_password.pack(side = tk.RIGHT,padx = pad,pady = pad)
button_login.pack(side = tk.RIGHT ,padx = pad,pady = pad)
button_register.pack(side = tk.LEFT,padx = pad,pady = pad)
button_guest.pack(padx = pad,pady = pad)
label_info.place(x= 0,y = 0)
root.mainloop()
