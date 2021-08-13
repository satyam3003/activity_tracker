from tkinter import *
from tkinter import messagebox
import json
import requests
import datetime

BACKGROUND_COLOR = "#95f2ff"
COLOR = "#3f00a3"
username = None
token = None
task = None
new_type = 'int'
new_color = 'sora'
option = None


def run_app():
    def create_account(user, tok):
        pixela_post = 'https://pixe.la/v1/users'
        pixela_get_parameters = {
            "token": tok,
            "username": user,
            "agreeTermsOfService": "yes",
            "notMinor": "yes",
        }

        response = requests.post(url=pixela_post, json=pixela_get_parameters)
        print(response.status_code)
        if response.status_code == 200:
            return True
        else:
            return False

    def button_create():
        global username, token
        if len(username_entry.get()) <= 1 or len(token_entry.get()) <= 7:
            messagebox.showinfo(title="Invalid",
                                message=f"Please fill all the details")
        else:
            popup_ok = messagebox.askokcancel(title="Save?",
                                              message=f'You have entered:\nusername: {username_entry.get()}\ntoken:{token_entry.get()}\nDo you want to save this info?')
            if popup_ok:
                is_user_ready = create_account(user=username_entry.get(), tok=token_entry.get())
                if is_user_ready:
                    username = username_entry.get()
                    token = token_entry.get()
                    new_data = {
                        'token': token,
                        'username': username,
                    }
                    with open('secret.json', mode='w') as save_new_file:
                        json.dump(new_data, save_new_file, indent=4)

                    messagebox.showinfo(title="Saving details!",
                                        message=f"Your details are saved as:\nusername: {username}\ntoken: {token}")
                    create_button.config(state='disabled')
                    window.destroy()
                    selection_window()
                else:
                    messagebox.showinfo(title="OOPS!",
                                        message="Account creation failed.. please try different username, token")

    window = Tk()
    window.title("Activity Tracker")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    app_name_lable = Label(text="Goal Tracker", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 25, ['italic', 'bold']),
                           pady=20)
    app_name_lable.grid(row=0, column=0, columnspan=2)

    goal_img = PhotoImage(file='goal.png')
    goal_image_label = Label(image=goal_img, bg=BACKGROUND_COLOR, highlightthickness=0)
    goal_image_label.grid(row=1, column=0, columnspan=2)

    start_label = Label(text="Let's get started!", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 15), pady=20)
    start_label.grid(row=2, column=0, columnspan=2)

    username_label = Label(text="Create username", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 13), pady=5, padx=10)
    username_label.grid(row=3, column=0)

    username_entry = Entry(width=30)
    username_entry.insert(END, string="rule: [a-z][a-z0-9-]{1,32}")
    username_entry.grid(row=3, column=1)

    token_label = Label(text="Create Token", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 13), pady=5, padx=10)
    token_label.grid(row=4, column=0)

    token_entry = Entry(width=30)
    token_entry.insert(END, string="rule: [ -~]{8,128}")
    token_entry.grid(row=4, column=1)

    create_button = Button(text="Create", bg=COLOR, fg='white', font=('Arial', 15), width=15, command=button_create)
    create_button.grid(row=5, column=0, columnspan=2, pady=15)

    window.mainloop()


def selection_window():
    def add_new_entry():
        new_table.destroy()
        try:
            with open('graph_dict.json', mode='r') as save_file:
                dt = json.load(save_file)
                select_graph_main()
        except FileNotFoundError:
            messagebox.showinfo(title="Please make a graph first.",
                                message="To open graphs you must first create a graph.")

    def new_graph():
        new_table.destroy()
        new_graph_setup()

    new_table = Tk()
    new_table.title("Activity Tracker")
    new_table.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    app_name_label = Label(text="Goal Tracker", bg=BACKGROUND_COLOR, fg=COLOR,
                           font=('Arial', 25, ['italic', 'bold']),
                           pady=20)
    app_name_label.grid(row=0, column=0, columnspan=2)

    goal_img = PhotoImage(file='goal.png')
    goal_image_label = Label(image=goal_img, bg=BACKGROUND_COLOR, highlightthickness=0)
    goal_image_label.grid(row=1, column=0, columnspan=2)

    new_entry = Button(text="Create new Entry", bg=COLOR, fg=BACKGROUND_COLOR, font=('Arial', 15),
                       command=add_new_entry)
    new_entry.grid(row=2, column=0, columnspan=2, pady=20)

    or_label = Label(text="OR", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 15))
    or_label.grid(row=3, column=0, columnspan=2)

    create_graph = Button(text="Create new Graph", bg=COLOR, fg=BACKGROUND_COLOR, font=('Arial', 15),
                          command=new_graph)
    create_graph.grid(row=4, column=0, columnspan=2, pady=20)

    new_table.mainloop()


def new_graph_setup():
    def backspace_function():
        window2.destroy()
        selection_window()

    def make_new_graph(graph_parameters):
        graph_endpoint = f"https://pixe.la/v1/users/{data['username']}/graphs"
        headers = {
            "X-USER-TOKEN": data['token'],
        }
        response = requests.post(url=graph_endpoint, json=graph_parameters, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            return True
        else:
            return False

    def graph_new_function():
        new_id = id_entry.get().lower()
        new_name = name_entry.get()
        new_unit = unit_entry.get()
        if len(new_id) == 0 or len(new_name) == 0 or len(new_unit) == 0:
            messagebox.showinfo(title='oops!', message='Please rill all inputs correctly')
        else:
            new_graph_dict = {
                "id": new_id,
                "name": new_name,
                "unit": new_unit,
                "type": new_type,
                "color": new_color
            }
            if make_new_graph(new_graph_dict):
                new_graph_send = {
                    new_id: {
                        "name": new_name,
                        "unit": new_unit,
                    }
                }

                try:
                    with open('graph_dict.json', mode='r') as file:
                        graph_data = json.load(file)  # read the data from file
                        # print(graph_data)
                        graph_data.update(new_graph_send)  # update the data from file with new_entry
                    with open('graph_dict.json', mode='w') as file:
                        json.dump(graph_data, file, indent=4)
                except FileNotFoundError:
                    with open('graph_dict.json', mode='w') as file:
                        json.dump(new_graph_send, file, indent=4)
                messagebox.showinfo(title="Success!", message="Yey!! Graph Generated!")
                window2.destroy()
                select_graph_main()

            else:
                messagebox.showinfo(title="Error!",
                                    message="Please recheck your inputs.. Seems like you made some error")

    def type_float():
        global new_type
        new_type = "float"

    def color_blue():
        global new_color
        new_color = "sora"

    def color_red():
        global new_color
        new_color = "momiji"

    def color_green():
        global new_color
        new_color = "shibafu"

    def color_yellow():
        global new_color
        new_color = "ichou"

    def color_purple():
        global new_color
        new_color = "ajisai"

    def color_black():
        global new_color
        new_color = "kuro"

    window2 = Tk()
    window2.title("Activity Tracker")
    window2.config(padx=50, bg=BACKGROUND_COLOR)

    app_name_label = Label(text="Goal Tracker", bg=BACKGROUND_COLOR, fg=COLOR,
                           font=('Arial', 25, ['italic', 'bold']),
                           pady=20)
    app_name_label.grid(row=0, column=0, columnspan=3)

    goal_img = PhotoImage(file='goal.png')
    goal_image_label = Label(image=goal_img, bg=BACKGROUND_COLOR, highlightthickness=0)
    goal_image_label.grid(row=1, column=0, columnspan=3)

    # -------------------- New graph heading ----------------------
    create_graph = Label(text="Let's Create a new graph", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 15),
                         pady=20)
    create_graph.grid(row=2, column=0, columnspan=3)

    # ---------------- ID -------------------------
    id_label = Label(text="ID", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 13), pady=5, padx=10)
    id_label.grid(row=3, column=0)

    id_entry = Entry(width=30)
    id_entry.insert(0, string="")
    id_entry.grid(row=3, column=1, columnspan=2)

    # --------------- name ----------------------
    name_label = Label(text="Graph Name", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 13), pady=5, padx=10)
    name_label.grid(row=4, column=0)

    name_entry = Entry(width=30)
    name_entry.insert(0, string="")
    name_entry.grid(row=4, column=1, columnspan=2)

    # --------------- Unit ----------------------
    unit_label = Label(text="Unit", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 13), pady=5, padx=10)
    unit_label.grid(row=5, column=0)

    unit_entry = Entry(width=30)
    unit_entry.insert(END, string=" ")
    unit_entry.grid(row=5, column=1, columnspan=2)

    # --------------int or float ---------------------
    type_label = Label(text="Type", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 13), pady=5, padx=10)
    type_label.grid(row=6, column=0)

    int_entry = Button(text='Int', bg=COLOR, fg='white', width=8)
    int_entry.grid(row=6, column=1)
    float_entry = Button(text="Float", bg=COLOR, fg='white', width=8, command=type_float)
    float_entry.grid(row=6, column=2)

    # ----------------- Color ------------------------
    color_label = Label(text="Choose Color", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 13), pady=15)
    color_label.grid(row=7, column=0, columnspan=3)

    blue_color = Button(bg='blue', padx=15, pady=5, command=color_blue)
    blue_color.grid(row=8, column=0, pady=2)

    red_color = Button(bg='red', padx=15, pady=5, command=color_red)
    red_color.grid(row=8, column=1, pady=2)

    green_color = Button(bg='green', padx=15, pady=5, command=color_green)
    green_color.grid(row=8, column=2, pady=2)

    yellow_color = Button(bg='yellow', padx=15, pady=5, command=color_yellow)
    yellow_color.grid(row=9, column=0, pady=2)

    purple_color = Button(bg='purple', padx=15, pady=5, command=color_purple)
    purple_color.grid(row=9, column=1, pady=2)

    black_color = Button(bg='black', padx=15, pady=5, command=color_black)
    black_color.grid(row=9, column=2, pady=2)

    # --------------- Add graph -------------------

    create_grp = Button(text="Create Graph", bg=COLOR, fg='white', font=('Arial', 15), width=15,
                        command=graph_new_function)
    create_grp.grid(row=10, column=0, columnspan=3, pady=25)

    backspace = Button(text="Go Back", bg=COLOR, fg=BACKGROUND_COLOR, font=('Arial', 15),
                       command=backspace_function)
    backspace.grid(row=11, column=0, columnspan=3, pady=20)
    window2.mainloop()


def select_graph_main():
    with open('graph_dict.json', mode='r') as save_file:
        data = json.load(save_file)
        # print(data)
    graph_id = [key for (key, value) in data.items()]

    def backspace_function():
        select_graph.destroy()
        selection_window()

    def grp_select():
        global option
        for i in listbox.curselection():
            option = listbox.get(i).split(" ")[0]
            # print(option)
            select_graph.destroy()
            add_pixel_main()

    select_graph = Tk()
    select_graph.title("Activity Tracker")
    select_graph.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    app_name_label = Label(text="Goal Tracker", bg=BACKGROUND_COLOR, fg=COLOR,
                           font=('Arial', 25, ['italic', 'bold']),
                           pady=20)
    app_name_label.grid(row=0, column=0, columnspan=3)

    goal_img = PhotoImage(file='goal.png')
    goal_image_label = Label(image=goal_img, bg=BACKGROUND_COLOR, highlightthickness=0)
    goal_image_label.grid(row=1, column=0, columnspan=3)

    # -------------------- New graph heading ----------------------
    create_graph = Label(text="Choose a graph", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 15),
                         pady=20)
    create_graph.grid(row=2, column=0, columnspan=3)

    listbox = Listbox(select_graph, height=len(graph_id), bg=COLOR, activestyle='dotbox', font=("Helvetica", 13),
                      fg=BACKGROUND_COLOR)

    for graph_options in graph_id:
        listbox.insert('end', f"{graph_options} {data[graph_options]['name']} ")

    listbox.grid(row=3, column=0, columnspan=3)

    select_grp = Button(text="Select", bg=COLOR, fg='white', font=('Arial', 15), width=15, command=grp_select)
    select_grp.grid(row=4, column=0, columnspan=3, pady=25)

    backspace = Button(text="Go Back", bg=COLOR, fg=BACKGROUND_COLOR, font=('Arial', 15),
                       command=backspace_function)
    backspace.grid(row=11, column=0, columnspan=3, pady=20)

    select_graph.mainloop()


def add_pixel_main():
    with open('graph_dict.json', mode='r') as save_file:
        dt = json.load(save_file)
    graph_id = [key for (key, value) in dt.items()]
    if option in graph_id:
        add_pixel_url = f"https://pixe.la/v1/users/{data['username']}/graphs/{option}"
        # print(add_pixel_url)
        headers = {
            "X-USER-TOKEN": data['token'],
        }

        def send_pixel_info(param):
            response = requests.post(url=add_pixel_url, json=param, headers=headers)
            print(response.status_code)
            # print(response.text)
            if response.status_code == 200:
                return True
            else:
                return False

        def add_pixel_function():
            if len(date_entry.get()) != 8 or len(quantity_entry.get()) == 0:
                messagebox.showinfo(title="You missed something?",
                                    message="Fill date and quantity attributes correctly!!")
            else:
                pixel_parameters = {
                    'date': date_entry.get(),
                    'quantity': quantity_entry.get()
                }
                print(pixel_parameters)
                resp_pixel = send_pixel_info(pixel_parameters)
                if resp_pixel:
                    messagebox.showinfo(title="Yu Hu! Entry added successfully",
                                        message=f"Entry added successfully\ndate: {date_entry.get()}\nquantity: {quantity_entry.get()}")
                    add_entry_button.config(text='Add Another entry..')
                    date_entry.delete(0, END)
                    date_entry.insert(END, string=f"{date_std}")
                    quantity_entry.delete(0, END)

                else:
                    messagebox.showinfo(title="You made an error!",
                                        message="You made and error while inputting info:\nFollow the following steps and try again\n1. Check date format, Dont rewrite a date if already entered\n2. Check int/float in quantities.\n3. Go to the graph and check if you are missing on something\n4. Contact admin.")
                    add_entry_button.config(text='Retry entry.')

        def back_to_graphs():
            new_pixel.destroy()
            select_graph_main()

        new_pixel = Tk()
        new_pixel.title("Activity Tracker")
        new_pixel.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        app_name_label = Label(text="Goal Tracker", bg=BACKGROUND_COLOR, fg=COLOR,
                               font=('Arial', 25, ['italic', 'bold']),
                               pady=20)
        app_name_label.grid(row=0, column=0, columnspan=3)

        goal_img = PhotoImage(file='goal.png')
        goal_image_label = Label(image=goal_img, bg=BACKGROUND_COLOR, highlightthickness=0)
        goal_image_label.grid(row=1, column=0, columnspan=3)

        new_entry_header = Label(text="New Entry", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 15),
                                 pady=20)
        new_entry_header.grid(row=2, column=0, columnspan=3)

        # -------------- Graph name ----------------------
        graph_name = Label(text=f"{dt[option]['name']}", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 18, 'bold'),
                           pady=12,
                           padx=10)
        graph_name.grid(row=3, column=0, columnspan=3)

        # ---------------- Date -----------------------------
        date_label = Label(text="Date [yyyymmdd]", bg=BACKGROUND_COLOR, fg=COLOR, font=('Arial', 13), pady=10,
                           padx=10)
        date_label.grid(row=4, column=0)

        now = datetime.datetime.now()
        date_std = now.strftime("%Y%m%d")
        date_entry = Entry()
        date_entry.insert(END, string=f"{date_std}")
        date_entry.grid(row=4, column=1, columnspan=2)

        # ------------------- Quantity -------------------------
        quantity_label = Label(text=f"Quantity ({dt[option]['unit']})", bg=BACKGROUND_COLOR, fg=COLOR,
                               font=('Arial', 13),
                               pady=10, padx=10)
        quantity_label.grid(row=5, column=0)

        quantity_entry = Entry()
        quantity_entry.insert(END, string=f"")
        quantity_entry.grid(row=5, column=1, columnspan=2)

        # -------------------------- Add button --------------------
        add_entry_button = Button(text="Add Entry!", bg=COLOR, fg=BACKGROUND_COLOR, font=('Arial', 15),
                                  command=add_pixel_function)
        add_entry_button.grid(row=6, column=0, columnspan=3, pady=20)

        # ------------------ Graph address ---------------------
        activity_graph_label = Label(text=f"{dt[option]['name']} Activity Graph(paste internet):",
                                     bg=BACKGROUND_COLOR, fg=COLOR).grid(
            row=7, column=0, columnspan=3)
        activity_graph_address = Entry(width=50)
        activity_graph_address.insert(END, string=f"{add_pixel_url}.html")
        activity_graph_address.grid(row=8, column=0, columnspan=3)

        # ------------------- Profile address ----------------------
        profile_label = Label(text=f"View Profile", bg=BACKGROUND_COLOR,
                              fg=COLOR).grid(row=9, column=0, columnspan=3)
        profile_address = Entry(width=50)
        profile_address.insert(END, string=f"https://pixe.la/@{data['username']}")
        profile_address.grid(row=10, column=0, columnspan=3)

        # ------------------- Get back to selection ------------------
        back_to_all_graphs = Button(text="Go Back to Graphs", bg=COLOR, fg=BACKGROUND_COLOR, font=('Arial', 15),
                                    command=back_to_graphs)
        back_to_all_graphs.grid(row=11, column=0, columnspan=3, pady=20)

        new_pixel.mainloop()

    else:
        messagebox.showinfo(title='Oops', message='Something went wrong!!!')

try:
    with open('secret.json', mode='r') as save_file:
        data = json.load(save_file)
        print(data)
        selection_window()


except FileNotFoundError:
    run_app()
