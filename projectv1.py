#importing libraries
import tkinter as tk
from tkinter import messagebox
import csv
import os
import sys
from datetime import datetime
#global vairables defined here

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#csv files

# Stores: Username, Password
WORKOUT_FILE = os.path.join(BASE_DIR, "my_workout_data.csv")
LOGIN_FILE = os.path.join(BASE_DIR, "login_info.csv")



#the style
BG_COLOR = "#BFBFBF"
BTN_COLOR = "#6D8AB0"
BTN_BORDER = 3
FONT_HEADER = ("Times New Roman", 28)
FONT_BODY = ("Arial", 12)


#app inherits stamdard tkimter window properties and class is opened

class FitnessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Workout Planner")
        self.geometry("1200x700") # slightly taller for better spacing
        self.configure(bg=BG_COLOR)

        self.current_user = None

        self.check_files()
        self.current_exercise_widgets = []

#creates main container frame
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)
#creates all the sub frames for the screens inside of this container
        self.login_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.dashboard_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.workout_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.history_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.analytics_frame = tk.Frame(self.container, bg=BG_COLOR)

        self.setup_login_frame()
        self.setup_dashboard_frame()
        self.setup_workout_frame()
        self.setup_history_frame()
        self.setup_analytics_frame()
#makes the login screen appear as first frame in container when app is run
        self.show_frame(self.login_frame)

#this checks to see if there;s a correctly name csv file already in the foler and creates one if not
    def check_files(self):
        if not os.path.exists(LOGIN_FILE):
            with open(LOGIN_FILE, mode='w', newline='') as f:
                csv.writer(f).writerow(["Username", "Password"])

        if not os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, mode='w', newline='') as f:
                csv.writer(f).writerow(["Username", "Date", "Exercise", "Set_Number", "Reps", "Weight"])

#The navigation tool. It loops through a list of all frames, uses pack_forget() to hide them all, and then uses pack() to show only the frame which has been requested/clicked on
    def show_frame(self, frame):
        for f in [self.login_frame, self.dashboard_frame, self.workout_frame,
                  self.history_frame, self.analytics_frame]:
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    #login menu frame
    def setup_login_frame(self):#visual labels and boxes
        top_bar = tk.Frame(self.login_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=10, padx=10)
#creating buttons with styling
        tk.Button(top_bar, text="EXIT APP", bg=BTN_COLOR, fg="white",
                  relief="solid", bd=BTN_BORDER, font=("Arial", 10, "bold"),
                  command=self.quit).pack(side=tk.LEFT)

        center_frame = tk.Frame(self.login_frame, bg=BG_COLOR)
        center_frame.pack(expand=True)

        tk.Label(center_frame, text="WORKOUT PLANNER", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 40)).pack(pady=(0, 30))
#input boxes for username and password
        tk.Label(center_frame, text="USERNAME", bg=BG_COLOR, fg="white", font=("Times New Roman", 18)).pack()
        self.entry_user = tk.Entry(center_frame, font=("Arial", 14), width=30, justify="center", bg=BTN_COLOR)
        self.entry_user.pack(pady=5, ipady=5)

        tk.Label(center_frame, text="PASSWORD", bg=BG_COLOR, fg="white", font=("Times New Roman", 18)).pack(pady=(20, 0))
        self.entry_pass = tk.Entry(center_frame, show="*", font=("Arial", 14), width=30, justify="center", bg=BTN_COLOR)
        self.entry_pass.pack(pady=5, ipady=5)

        btn_row = tk.Frame(center_frame, bg=BG_COLOR)
        btn_row.pack(pady=30)
#buttons to interact with database and perform actions defined below
        tk.Button(btn_row, text="LOGIN", bg=BTN_COLOR, fg="white", width=15,
                  relief="solid", bd=BTN_BORDER, font=("Arial", 12, "bold"),
                  command=self.perform_login).pack(side=tk.LEFT, padx=20)

        tk.Button(btn_row, text="SIGN UP", bg=BTN_COLOR, fg="white", width=15,
                  relief="solid", bd=BTN_BORDER, font=("Arial", 12, "bold"),
                  command=self.perform_signup).pack(side=tk.LEFT, padx=20)

    def perform_login(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()

        if not u or not p:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        found = False
        with open(LOGIN_FILE, 'r') as f:#opens login file in mode read "r"
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:#uses for loop to check the username and password entered match those in the feild of the csv file
                if row and row[0] == u and row[1] == p:
                    found = True
                    break
#break ends the check when the right credentials are entered
        if found:
            self.current_user = u
            self.update_dashboard_username()
            self.entry_user.delete(0, tk.END)
            self.entry_pass.delete(0, tk.END)
            self.show_frame(self.dashboard_frame)
        else:
            messagebox.showerror("Failed", "Invalid Username or Password")

    def perform_signup(self):#add new user and password to the database
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        if not u or not p: return


#return stops the process there as no data has been entered into the input boxs


        with open(LOGIN_FILE, 'r') as f:
            for row in csv.reader(f):
                if row and row[0] == u:
                    messagebox.showerror("Error", "Username taken.")
                    return

        with open(LOGIN_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([u, p])
        messagebox.showinfo("Success", "Account created!")

    def logout(self):
        self.current_user = None
        self.show_frame(self.login_frame)#goes back to login menu and clears whihc user is active when the log out button is pressed

    #dashboard
    def setup_dashboard_frame(self):
        top_bar = tk.Frame(self.dashboard_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=10, padx=10)

        tk.Button(top_bar, text="EXIT APP", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=self.quit).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(top_bar, text="LOG OUT", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=self.logout).pack(side=tk.LEFT)

        tk.Label(top_bar, text="WORKOUT PLANNER", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 24)).pack(side=tk.LEFT, expand=True)

        self.lbl_username = tk.Label(top_bar, text="USER", bg=BTN_COLOR, fg="white",
                                     font=("Arial", 12, "bold"), padx=15, pady=5, relief="solid", bd=BTN_BORDER)
        self.lbl_username.pack(side=tk.RIGHT)

        content_area = tk.Frame(self.dashboard_frame, bg=BG_COLOR)
        content_area.pack(fill="both", expand=True, padx=40, pady=40)

        def create_big_btn(parent, text, cmd):#creates a function for the stylinbg of a button that can be reused for all three buttons instead of having to manually style all of them
            btn = tk.Button(parent, text=text, bg=BTN_COLOR, fg="white",
                            font=("Times New Roman", 24), relief="solid", bd=BTN_BORDER, command=cmd)
            btn.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

        create_big_btn(content_area, "HISTORY", self.open_history)
        create_big_btn(content_area, "NEW\nWORKOUT", lambda: self.show_frame(self.workout_frame))
        create_big_btn(content_area, "ANALYTICS", lambda: self.show_frame(self.analytics_frame))

    def update_dashboard_username(self):
        if self.current_user:
            self.lbl_username.config(text=self.current_user.upper())

#new workout tab
    def setup_workout_frame(self):
        tk.Label(self.workout_frame, text="New Workout", bg=BG_COLOR, font=FONT_HEADER).pack(pady=10)

        control_frame = tk.Frame(self.workout_frame, bg=BG_COLOR)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Exercise Name:", bg=BG_COLOR, font=FONT_BODY).pack(side=tk.LEFT, padx=5)
        self.new_exercise_entry = tk.Entry(control_frame, font=FONT_BODY, width=20)
        self.new_exercise_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="+ Add Exercise", bg="green", fg="white", font=("Arial", 10, "bold"),
                  command=self.add_exercise_row).pack(side=tk.LEFT, padx=10)

        # Container needs to allow children to expand
        self.exercises_container = tk.Frame(self.workout_frame, bg=BG_COLOR)
        self.exercises_container.pack(fill="both", expand=True, padx=20, pady=10)

        btn_frame = tk.Frame(self.workout_frame, bg=BG_COLOR)
        btn_frame.pack(side=tk.BOTTOM, pady=20)

        tk.Button(btn_frame, text="Save Workout", bg="blue", fg="white", font=("Arial", 14),
                  command=self.save_workout).pack(side=tk.LEFT, padx=20)
        tk.Button(btn_frame, text="Back", font=("Arial", 14),
                  command=lambda: self.show_frame(self.dashboard_frame)).pack(side=tk.LEFT, padx=20)

    def add_exercise_row(self):#this creates 5 new tkinter widgets with 5 collumns for data entry
        ex_name = self.new_exercise_entry.get()
        if not ex_name:
            messagebox.showwarning("Input Error", "Please enter an exercise name first.")
            return

        #main row frame
        row_frame = tk.Frame(self.exercises_container, relief=tk.RIDGE, borderwidth=2, pady=10, bg="#E0E0E0")
        row_frame.pack(fill="x", pady=5)

        # Header for the row (Exercise Name)
        tk.Label(row_frame, text=ex_name, font=("Arial", 16, "bold"), bg="#E0E0E0", width=15, anchor="w").pack(side=tk.TOP, fill="x", padx=10)

        # Grid container for the 5 sets
        sets_container = tk.Frame(row_frame, bg="#E0E0E0")
        sets_container.pack(fill="x", expand=True, padx=5, pady=5)

        exercise_data = {'name': ex_name, 'set_inputs': []}


        #5 columns
        for col_index in range(5):
            sets_container.grid_columnconfigure(col_index, weight=1)


        for i in range(5):
            #sub-frame for each set that fills its grid cell
            set_box = tk.Frame(sets_container, bg="#D0D0D0", bd=1, relief="solid")
            set_box.grid(row=0, column=i, sticky="nsew", padx=5)

            tk.Label(set_box, text=f"SET {i+1}", font=("Arial", 10, "bold"), bg="#D0D0D0").pack(pady=(5,2))

            # Reps
            tk.Label(set_box, text="Reps", font=("Arial", 8), bg="#D0D0D0").pack()
            reps_entry = tk.Entry(set_box, width=6, justify='center', font=("Arial", 12))
            reps_entry.pack(pady=2)

            # Weight
            tk.Label(set_box, text="Kg/Lbs", font=("Arial", 8), bg="#D0D0D0").pack()
            weight_entry = tk.Entry(set_box, width=6, justify='center', font=("Arial", 12))
            weight_entry.pack(pady=(2, 10))

            exercise_data['set_inputs'].append({'reps': reps_entry, 'weight': weight_entry})




#saves a volitile version of the data entered from that collumn while workout is continued until user presses save workout

        self.current_exercise_widgets.append(exercise_data)
        self.new_exercise_entry.delete(0, tk.END)




#Loops through those saved widgets, grabs the text (.get()), converts them to integers/floats, and appends them to WORKOUT_FILE

    def save_workout(self):
        if not self.current_exercise_widgets: return
        today = datetime.now().strftime("%Y-%m-%d")
        data_to_save = []





        for ex_item in self.current_exercise_widgets:
            name = ex_item['name']
            for i, inputs in enumerate(ex_item['set_inputs']):
                r_txt = inputs['reps'].get()
                w_txt = inputs['weight'].get()
                if r_txt and w_txt:
                    try:
                        # Save User, Date, Name, Set, Reps, Weight
                        data_to_save.append([self.current_user, today, name, i+1, int(r_txt), float(w_txt)])
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid number in {name}")
                        return

        with open(WORKOUT_FILE, mode='a', newline='') as file:
            csv.writer(file).writerows(data_to_save)



#executes functions that have been defined ,delteiing current data and going back to dashboard frame
        messagebox.showinfo("Success", "Workout Saved!")
        self.clear_workout_screen()
        self.show_frame(self.dashboard_frame)





#Uses .winfo_children().destroy() to delete the dynamically generated widgets from the screen after saving

    def clear_workout_screen(self):
        for widget in self.exercises_container.winfo_children():
            widget.destroy()
        self.current_exercise_widgets = []




    # history
    def setup_history_frame(self):
        tk.Label(self.history_frame, text="Workout History", bg=BG_COLOR, font=FONT_HEADER).pack(pady=10)
        self.history_text = tk.Text(self.history_frame, width=80, height=20, font=("Courier", 12))
        self.history_text.pack(pady=10)
        tk.Button(self.history_frame, text="Back", font=("Arial", 14),
                  command=lambda: self.show_frame(self.dashboard_frame)).pack(pady=10)

    def open_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)

        if os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, mode='r') as file:
                reader = csv.reader(file)
                data = list(reader)

                header = f"{'Date':<12} {'Exercise':<15} {'Set':<5} {'Reps':<5} {'Weight':<8}\n"
                self.history_text.insert(tk.END, header + "-"*60 + "\n")

                for row in data[1:]:
                    if row and row[0] == self.current_user:
                        self.history_text.insert(tk.END, f"{row[1]:<12} {row[2]:<15} {row[3]:<5} {row[4]:<5} {row[5]:<8}\n")



        self.history_text.config(state=tk.DISABLED)#this line puts the data in from the csv file and locks the text box so users arent able to enter other things in
        self.show_frame(self.history_frame)








    #analyitics
    def setup_analytics_frame(self):
        tk.Label(self.analytics_frame, text="Analytics", bg=BG_COLOR, font=FONT_HEADER).pack(pady=10)

        ctrl_frame = tk.Frame(self.analytics_frame, bg=BG_COLOR)
        ctrl_frame.pack(pady=10)
        tk.Label(ctrl_frame, text="Exercise Name:", bg=BG_COLOR).pack(side=tk.LEFT)
        self.ana_entry = tk.Entry(ctrl_frame)
        self.ana_entry.pack(side=tk.LEFT, padx=10)
        tk.Button(ctrl_frame, text="Graph", command=self.generate_graph).pack(side=tk.LEFT)


#setting up frames and sizes with styles

        self.canvas = tk.Canvas(self.analytics_frame, width=800, height=400, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=20)
        self.stats_label = tk.Label(self.analytics_frame, text="", bg=BG_COLOR, font=("Times New Roman", 12, "bold"))
        self.stats_label.pack(pady=5)
        tk.Button(self.analytics_frame, text="Back", font=("Arial", 14),
                  command=lambda: self.show_frame(self.dashboard_frame)).pack(pady=10)


#making the graph

    def generate_graph(self):
        target_ex = self.ana_entry.get().strip()
        self.canvas.delete("all")
        if not target_ex or not os.path.exists(WORKOUT_FILE): return

        #collect ALL entries for this user in order creating list
        y_values = []

        with open(WORKOUT_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader) # skip header

            # We track the 'best' lift per saved session/row to avoid duplicate dots for Set 1, Set 2 etc
            # But the user might save multiple sets at once.
            # Strategy: Every row in CSV is a set. We want to graph "strength".
            # To avoid a messy graph with 5 dots per day, let's group by "unique date+time" or just row order.
            # SIMPLEST FOR TESTING: Graph every single set that is a Personal Best?
            # OR: Graph every entry (might be messy).
            # BETTER: Group by Date, but allow duplicates if dates repeat?
            # REVISED STRATEGY: Graph the MAX of every "save batch".
            # Since CSV doesn't track batches easily, we will just graph EVERY valid set's 1RM in order.

            for row in reader:
                # 1. SECURITY CHECK: Only current user
                if row[0] == self.current_user and row[2].lower() == target_ex.lower():
                    try:
                        reps = int(row[4])
                        weight = float(row[5])
                        e1rm = weight * (1 + reps / 30)#equation for 1 rep max
                        y_values.append(e1rm)
                    except ValueError:
                        continue

        if not y_values:
            self.canvas.create_text(400, 200, text="No data found for this user/exercise", font=("Arial", 16))
            return

#this is the drawing
        w, h, margin = 800, 400, 50
        max_v, min_v = max(y_values), min(y_values)
        if max_v == min_v: max_v += 10
        if min_v > 0: min_v -= 10 # Give a little room at bottom

        num_points = len(y_values)

# Automatic Spacing Divides width by how many points we have

    #Divides the width of the canvas by the number of workouts to space the dots evenly.
        x_step = (w - 2 * margin) / max(1, num_points - 1)

        prev_x, prev_y = None, None

        for i, val in enumerate(y_values):
            # X Calculation: Purely based on order (Session 1, Session 2...)
            x = margin + (i * x_step)

            # Y Calculation
            norm_h = (val - min_v) / (max_v - min_v) #This normalizes the Y-axis. It finds out where the weight sits purely as a percentage between the user's minimum and maximum lifts, scaling it perfectly to the height of the canvas
            y = h - margin - (norm_h * (h - 2 * margin))

            # Draw Point
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="red")

            # Draw Label (Session #)
            self.canvas.create_text(x, h-margin+20, text=f"{i+1}", font=("Arial", 8))

            #Connects the calculated coordinates to actually draw the graph.
            if prev_x is not None:
                self.canvas.create_line(prev_x, prev_y, x, y, fill="blue", width=2)

            prev_x, prev_y = x, y

        self.stats_label.config(text=f"Last 1RM: {int(y_values[-1])} kg")



#simply runs the programme and everything definied in it
if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
