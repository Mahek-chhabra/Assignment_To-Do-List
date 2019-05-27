from tkinter import *
import pymysql


# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
    register_screen.configure(bg="white")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="black",fg="white").pack()
    Label(register_screen, bg="white" ,text="").pack()
    username_lable = Label(register_screen, bg="white",text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen,bg="white", text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, bg="white" , text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="black",fg="white", command=register_user).pack()


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    login_screen.configure(bg="white")
    Label(login_screen,bg="white" , text="Please enter details below to login").pack()
    Label(login_screen,bg="white" , text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen,bg="white" , text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen,bg="white" , text="").pack()
    Label(login_screen,bg="white" , text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen,bg="white" , text="").pack()
    Button(login_screen, text="Login", width=10, height=1,bg="white" , command=login_verify).pack()


# Implementing event on register button

def register_user():
    username_info = username.get()
    password_info = password.get()

    cursor.execute("INSERT INTO users (username,password) VALUES  ('%s','%s')" % (username_info,password_info))
    cursor.execute("UPDATE users SET userid=CONCAT(username,'',Personalid)")
    conn.commit()

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()


# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    global iddetails
    iddetails=StringVar()

    if username1 == "" or password1 == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT userid FROM users WHERE username = '%s'" % (username1))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT userid FROM users WHERE username = '%s' AND password = '%s' " % (username1, password1))
            if cursor.fetchone() is not None:
                Label(login_screen, text="Login Success", fg="green", font=("calibri", 11)).pack()
                cursor.execute("SELECT userid FROM users WHERE username = '%s' AND password = '%s' " % (username1, password1))
                idd = cursor.fetchone()
                iddetails = idd[0]
                todo_list()
            else:
                password_not_recognised()
        else:
            user_not_found()



# Designing popup for login success

def todo_list():
    global todo_list
    todo_list = Toplevel(login_screen)
    todo_list.title("To-Do List")
    todo_list.geometry("300x400")
    todo_list.configure(bg="white")
    Label(todo_list, text="To-Do List",bg="white", fg="black").pack()
    Label(todo_list, text="", bg="white", fg="black").pack()
    Button(todo_list, text="Add task", width=15, height=1, bg="white", fg="black", command=add_task).pack()
    Button(todo_list, text="Display all task", width=15, height=1, bg="white", fg="black", command=display_task).pack()
    Button(todo_list, text="Modify task", width=15, height=1, bg="white", fg="black", command=modify_task).pack()
    Button(todo_list, text="Deleta All Task", width=15, height=1, bg="white", fg="black", command=delete_all).pack()
    Button(todo_list, text="Delect One Task", width=15, height=1, bg="white", fg="black", command=delete_one).pack()
    Button(todo_list, text="Sort Ascending", width=15, height=1, bg="white", fg="black", command=sort_asc).pack()
    Button(todo_list, text="Sort Descending", width=15, height=1, bg="white", fg="black", command=sort_desc).pack()
    Button(todo_list, text="Number of Tasks", width=15, height=1, bg="white", fg="black", command=numberoftasks).pack()
    Button(todo_list, text="Exit", width=15, height=1, bg="white", fg="black", command=exit).pack()



# Adding task to-do list

def add_task():
    global add_task
    add_task = Toplevel(todo_list)
    add_task.title("Add task")
    add_task.geometry("300x250")
    add_task.configure(bg="white")
    Label(add_task, text="Add task", bg="white", fg="black").pack()

    global taskentered
    taskentered=StringVar()

    global task_entered

    task_entered = Entry(add_task, textvariable=taskentered)
    task_entered.pack()
    Button(add_task, text="Submit", width=15, height=1, bg="white", fg="black", command=add_tasktolist).pack()


def add_tasktolist():
    taskdetails=taskentered.get()
    cursor.execute("CREATE TABLE IF NOT EXISTS todolist (userid TEXT,task TEXT,taskvalue INT)")
    cursor.execute("INSERT INTO todolist(userid,task,taskvalue) VALUES('%s', '%s',%d) "%(iddetails, taskdetails,0))
    conn.commit()
    updated_task()


def updated_task():
    global updated_task
    updated_task = Toplevel(add_task)
    updated_task.title(" Updated To-Do Task")
    updated_task.geometry("300x250")
    updated_task.configure(bg="white")

    Label(updated_task, text="Incomplete Tasks", bg="white", fg="black").pack()

    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=0" % iddetails)
    data = cursor.fetchall()
    check_boxes_task={row : IntVar() for row in data}


    for row in data:
        c = Checkbutton(updated_task, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()

    Label(updated_task, text="Completed Tasks", bg="white", fg="black").pack()

    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=1" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(updated_task, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()

    Button(updated_task, text="OK",bg="white" , command=delete_updated_task).pack()



def modify_task():
    global modify_task
    modify_task = Toplevel(todo_list)
    modify_task.title(" Modify Task")
    modify_task.geometry("300x250")
    modify_task.configure(bg="white")

    Label(modify_task , text="Mark Completed Task" , bg="white" , fg="black"). pack()

    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=0" % iddetails)
    global incompletetask
    incompletetask = cursor.fetchall()
    global check_boxes_task
    check_boxes_task= {row: IntVar() for row in incompletetask}

    for row in incompletetask:
        c = Checkbutton(modify_task, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()

    Button(modify_task, text="OK",bg="white" , command=state).pack()


def state():
    for row in incompletetask:
        statevalue=check_boxes_task[row].get()
        if statevalue == 1:
            cursor.execute("UPDATE todolist set taskvalue =1 WHERE userid='%s' and task='%s'" % (iddetails,row[0]))
            conn.commit()
    delete_modify_task()

def display_task():
    global display_task
    display_task = Toplevel(todo_list)
    display_task.title("To-Do Task")
    display_task.geometry("300x250")
    display_task.configure(bg="white")
    usernamedetails = username_verify.get()

    Label(display_task, text="Incomplete Tasks", bg="white", fg="black").pack()

    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=0" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(display_task, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()

    Label(display_task, text="Completed Tasks", bg="white", fg="black").pack()

    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=1" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(display_task, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()

    Button(display_task, text="OK", bg="white" ,command=delete_display_task).pack()


def delete_all():
    usernamedetails= username_verify.get()
    cursor.execute("DELETE FROM todolist where userid ='%s' " % iddetails)
    conn.commit()
    post_delete_all()

def post_delete_all():
    global post_delete_all
    post_delete_all=Toplevel(todo_list)
    post_delete_all.title("Deleted")
    post_delete_all.geometry("300x250")
    post_delete_all.configure(bg="white")
    Label(post_delete_all, bg="white", fg="black", text="All tasks successfully deleted ").pack()
    Button(post_delete_all, text="OK",bg="white" , command=delete_post_delete_all).pack()


def delete_one():
    global delete_one
    delete_one = Toplevel(todo_list)
    delete_one.title("Delete Task")
    delete_one.geometry("300x250")
    delete_one.configure(bg="white")
    Label(delete_one, text="write task to delete", bg="white", fg="black").pack()

    global taskdeleted
    taskdeleted = StringVar()

    global task_deleted

    task_deleted = Entry(delete_one, textvariable=taskdeleted)
    task_deleted.pack()
    Button(delete_one, text="Submit", width=15, height=1, bg="white", fg="black", command=deletetaskfromlist).pack()

    Label(delete_one, text="Incomplete Tasks List", bg="white", fg="black").pack()

    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=0" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(delete_one, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()

    Label(delete_one, text="Completed Tasks List", bg="white", fg="black").pack()

    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=1" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(delete_one, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()



def deletetaskfromlist():
    taskdetails=taskdeleted.get()
    cursor.execute("DELETE FROM todolist where userid ='%s' and task='%s'" % (iddetails,taskdetails))
    conn.commit()
    updatedafterdelete()



def updatedafterdelete():
    global updatedafterdelete
    updatedafterdelete=Toplevel(delete_one)
    updatedafterdelete.title("Updated task list after deletion")
    updatedafterdelete.geometry("300x250")
    updatedafterdelete.configure(bg="white")

    Label(updatedafterdelete, text="Incomplete Tasks ", bg="white", fg="black").pack()
    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=0" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(updatedafterdelete, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()

    Label(updatedafterdelete, text="Completed Tasks ", bg="white", fg="black").pack()

    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=1" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(updatedafterdelete, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()


    Button(updatedafterdelete, text="OK", bg="white" ,command=delete_updatedafterdelete).pack()



def sort_asc():
    global sort_asc
    sort_asc = Toplevel(todo_list)
    sort_asc.title("Ascending ordered list")
    sort_asc.geometry("300x250")
    sort_asc.configure(bg="white")

    Label(sort_asc, text="Incomplete Tasks ", bg="white", fg="black").pack()
    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=0 ORDER BY task ASC" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(sort_asc, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()
    Button(sort_asc, text="OK", bg="white" ,command=delete_asc_order).pack()


def sort_desc():
    global sort_desc
    sort_desc = Toplevel(todo_list)
    sort_desc.title("Descending ordered list")
    sort_desc.geometry("300x250")
    sort_desc.configure(bg="white")
    Label(sort_desc, text="Incomplete Tasks ", bg="white", fg="black").pack()
    cursor.execute("SELECT task FROM todolist WHERE userid='%s' and taskvalue=0 ORDER BY task ASC" % iddetails)
    data = cursor.fetchall()
    check_boxes_task = {row: IntVar() for row in data}

    for row in data:
        c = Checkbutton(sort_desc, text=row, bg="white", fg="black", variable=check_boxes_task[row])
        c.pack()

    Button(sort_desc, text="OK", bg="white" ,command=delete_desc_order).pack()

def numberoftasks():
    global numberoftasks
    numberoftasks = Toplevel(todo_list)
    numberoftasks.title("Total number of tasks pending")
    numberoftasks.geometry("300x250")
    numberoftasks.configure(bg="white")

    usernamedetails = username_verify.get()
    Lb = Listbox(numberoftasks)

    cursor.execute("SELECT task FROM todolist WHERE userid ='%s' and taskvalue=0" % (iddetails))
    data = cursor.fetchall()
    count = cursor.rowcount
    Lb.insert(1,count)
    Lb.pack()
    Button(numberoftasks, text="OK", bg="white" ,command=delete_numberoftasks).pack()




# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, bg="white" ,text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", bg="white" ,command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen,bg="white" , text="User Not Found").pack()
    Button(user_not_found_screen, text="OK",bg="white" , command=delete_user_not_found_screen).pack()


# Deleting popups

def delete_login_success():
    login_success_screen.destroy()


def delete_asc_order():
    sort_asc.destroy()

def delete_desc_order():
    sort_desc.destroy()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()

def delete_post_delete_all():
    post_delete_all.destroy()


def delete_updated_task():
    updated_task.destroy()
    add_task.destroy()

def delete_display_task():
    display_task.destroy()

def delete_modify_task():
    modify_task.destroy()


def delete_updatedafterdelete():
    updatedafterdelete.destroy()
    delete_one.destroy()

def delete_numberoftasks():
    numberoftasks.destroy()



# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    main_screen.configure(bg="white")
    Label(text="Select Your Choice", bg="black", fg="white" , width="300", height="2", font=("Calibri", 13)).pack()
    Label(bg="white" ,text="").pack()
    Button(text="Login", height="2", width="30",bg="white" , command=login).pack()
    Label(bg="white" ,text="").pack()
    Button(text="Register", height="2", width="30", bg="white" ,command=register).pack()
    global conn, cursor
    conn = pymysql.connect("localhost", "root", "mahek", "to-do list")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT,Personalid int AUTO_INCREMENT PRIMARY KEY,userid TEXT)")
    cursor.execute("SELECT * FROM users WHERE username = 'admin' AND password = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES('admin', 'admin')")
        conn.commit()

    main_screen.mainloop()


main_account_screen()