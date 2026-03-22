#importing libraries
import tkinter as tk
from tkinter import messagebox
import csv
import os
import sys
from datetime import datetime

# ============================================================
# ADDED IN VERSION 7: Counter and defaultdict are imported
# from Python's built-in 'collections' module.
#
# - Counter is a special dictionary that counts how many times
#   each item appears. We use it in the Top Exercises analytics
#   tab to count how many sets each exercise has been logged.
#
# - defaultdict is a dictionary that automatically creates a
#   default value for a key if it doesn't exist yet. We use it
#   in the Volume analytics tab to add up total volume per date
#   without needing to check if the date key exists first.
# ============================================================
from collections import defaultdict, Counter

#global variables defined here

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


#app inherits standard tkinter window properties and class is opened

class FitnessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Workout Planner")
        self.geometry("1200x700")
        self.configure(bg=BG_COLOR)

        self.current_user = None

        self.check_files()
        self.current_exercise_widgets = []

#creates main container frame
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)

# ============================================================
# ADDED IN VERSION 7: settings_frame is added here alongside
# the existing frames. It is created as an empty Frame inside
# the container just like all the others. It only becomes
# visible when show_frame(self.settings_frame) is called.
# ============================================================
        self.login_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.dashboard_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.workout_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.history_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.analytics_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.settings_frame = tk.Frame(self.container, bg=BG_COLOR)  # NEW in v7

        self.setup_login_frame()
        self.setup_dashboard_frame()
        self.setup_workout_frame()
        self.setup_history_frame()
        self.setup_analytics_frame()
        self.setup_settings_frame()  # NEW in v7 - builds the settings screen
#makes the login screen appear as first frame in container when app is run
        self.show_frame(self.login_frame)

#this checks to see if there's a correctly named csv file already in the folder and creates one if not
    def check_files(self):
        if not os.path.exists(LOGIN_FILE):
            with open(LOGIN_FILE, mode='w', newline='') as f:
                csv.writer(f).writerow(["Username", "Password"])

        if not os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, mode='w', newline='') as f:
                csv.writer(f).writerow(["Username", "Date", "Exercise", "Set_Number", "Reps", "Weight"])

# ============================================================
# MODIFIED IN VERSION 7: settings_frame is added to the list
# of frames that show_frame loops through and hides.
# Without this, settings_frame would never be hidden when
# switching to another screen - it would stay visible on top
# of everything else.
# ============================================================
    def show_frame(self, frame):
        for f in [self.login_frame, self.dashboard_frame, self.workout_frame,
                  self.history_frame, self.analytics_frame, self.settings_frame]:
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
            for row in reader:#uses for loop to check the username and password entered match those in the field of the csv file
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

#return stops the process there as no data has been entered into the input boxes

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
        self.show_frame(self.login_frame)#goes back to login menu and clears which user is active when the log out button is pressed

    #dashboard
    def setup_dashboard_frame(self):
        top_bar = tk.Frame(self.dashboard_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=10, padx=10)

        tk.Button(top_bar, text="EXIT APP", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=self.quit).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(top_bar, text="LOG OUT", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=self.logout).pack(side=tk.LEFT)

# ============================================================
# ADDED IN VERSION 7: SETTINGS button in the dashboard top bar.
# It sits next to LOG OUT and calls show_frame(settings_frame)
# when clicked. This is the entry point to the entire settings
# screen. The lambda is used here instead of a direct reference
# because show_frame needs an argument - lambda lets us pass
# that argument when the button is clicked rather than when
# the button is created.
# ============================================================
        tk.Button(top_bar, text="SETTINGS", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=lambda: self.show_frame(self.settings_frame)).pack(side=tk.LEFT, padx=(5, 0))

        tk.Label(top_bar, text="WORKOUT PLANNER", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 24)).pack(side=tk.LEFT, expand=True)

        self.lbl_username = tk.Label(top_bar, text="USER", bg=BTN_COLOR, fg="white",
                                     font=("Arial", 12, "bold"), padx=15, pady=5, relief="solid", bd=BTN_BORDER)
        self.lbl_username.pack(side=tk.RIGHT)

        content_area = tk.Frame(self.dashboard_frame, bg=BG_COLOR)
        content_area.pack(fill="both", expand=True, padx=40, pady=40)

        def create_big_btn(parent, text, cmd):#creates a function for the styling of a button that can be reused for all three buttons instead of having to manually style all of them
            btn = tk.Button(parent, text=text, bg=BTN_COLOR, fg="white",
                            font=("Times New Roman", 24), relief="solid", bd=BTN_BORDER, command=cmd)
            btn.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

        create_big_btn(content_area, "HISTORY", self.open_history)

# ============================================================
# MODIFIED IN VERSION 7: The NEW WORKOUT button now calls
# open_workout instead of directly calling show_frame.
# This is needed because open_workout refreshes the exercise
# dropdown picker with the latest data before opening the
# screen. Without this step the dropdown would always show
# an empty list because it's populated dynamically from
# the CSV at the point the screen is opened, not at startup.
# ============================================================
        create_big_btn(content_area, "NEW\nWORKOUT", self.open_workout)

# ============================================================
# MODIFIED IN VERSION 7: ANALYTICS now calls open_analytics
# instead of show_frame directly, for the same reason as above
# - it refreshes the exercise list for the analytics picker
# before showing the screen.
# ============================================================
        create_big_btn(content_area, "ANALYTICS", self.open_analytics)

    def update_dashboard_username(self):
        if self.current_user:
            self.lbl_username.config(text=self.current_user.upper())

# ============================================================
# ADDED IN VERSION 7: open_workout method.
# This is called instead of going directly to workout_frame.
# It reads the CSV to find every exercise this user has ever
# saved, then rebuilds the OptionMenu (dropdown) with those
# exercise names before showing the workout screen.
#
# How the dropdown rebuild works:
# - self.exercise_dropdown["menu"] gets the actual Menu object
#   that lives inside the OptionMenu widget.
# - menu.delete(0, "end") clears all existing items from it.
# - menu.add_command() adds each exercise as a clickable item.
#   The command uses a lambda with e=ex to capture the current
#   value of ex. Without e=ex, all items would refer to the
#   last value of ex in the loop (a common Python loop bug).
# - Finally the StringVar is reset to the placeholder text.
# ============================================================
    def open_workout(self):
        known = self.get_known_exercises()
        menu = self.exercise_dropdown["menu"]
        menu.delete(0, "end")
        menu.add_command(label="-- Previous --",
                         command=lambda: self.exercise_dropdown_var.set("-- Previous --"))
        for ex in known:
            menu.add_command(label=ex, command=lambda e=ex: self.exercise_dropdown_var.set(e))
        self.exercise_dropdown_var.set("-- Previous --")
        self.show_frame(self.workout_frame)

# ============================================================
# ADDED IN VERSION 7: open_analytics method.
# Same pattern as open_workout. Calling this before showing
# the analytics frame ensures the scrollable exercise picker
# popup will have fresh data whenever the user opens analytics.
# ============================================================
    def open_analytics(self):
        self.show_frame(self.analytics_frame)

# ============================================================
# ADDED IN VERSION 7: get_known_exercises method.
# This is a helper method used by both the workout dropdown
# and the analytics picker. It opens the workout CSV, reads
# every row that belongs to the current user, and collects
# the exercise names (column index 2) into a Python set.
#
# A set is used instead of a list because sets automatically
# ignore duplicates - if the user has logged "Bench Press"
# 50 times, it still only appears once. sorted() then turns
# the set into an alphabetically ordered list.
# ============================================================
    def get_known_exercises(self):
        exercises = set()
        if os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header row
                for row in reader:
                    if row and row[0] == self.current_user and len(row) > 2:
                        exercises.add(row[2].strip())
        return sorted(exercises)

#new workout tab
    def setup_workout_frame(self):
        tk.Label(self.workout_frame, text="New Workout", bg=BG_COLOR, font=FONT_HEADER).pack(pady=10)

        control_frame = tk.Frame(self.workout_frame, bg=BG_COLOR)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Exercise Name:", bg=BG_COLOR, font=FONT_BODY).pack(side=tk.LEFT, padx=5)
        self.new_exercise_entry = tk.Entry(control_frame, font=FONT_BODY, width=20)
        self.new_exercise_entry.pack(side=tk.LEFT, padx=5)

# ============================================================
# ADDED IN VERSION 7: Exercise dropdown picker for the workout
# screen. This uses tkinter's built-in OptionMenu widget.
#
# How it works:
# - exercise_dropdown_var is a StringVar - a special tkinter
#   variable that widgets can read and watch for changes.
# - The OptionMenu is linked to this StringVar. When the user
#   clicks a menu item, the StringVar's value changes to that
#   item's label automatically.
# - .trace("w", on_dropdown_select) sets up a "watcher" on
#   the StringVar. Every time its value is written ("w") to,
#   on_dropdown_select fires automatically.
# - on_dropdown_select reads the current value, and if it is
#   not the placeholder, it clears the text entry box and
#   inserts the chosen exercise name into it. This means the
#   user can either type a name or pick from the dropdown -
#   both end up in the same entry box and work identically
#   when + Add Exercise is clicked.
# - The dropdown starts with only "-- Previous --" because
#   the real list is populated by open_workout at runtime.
# ============================================================
        tk.Label(control_frame, text="or pick:", bg=BG_COLOR, font=FONT_BODY).pack(side=tk.LEFT, padx=(10, 2))
        self.exercise_dropdown_var = tk.StringVar(value="-- Previous --")
        self.exercise_dropdown = tk.OptionMenu(control_frame, self.exercise_dropdown_var, "-- Previous --")
        self.exercise_dropdown.config(bg=BTN_COLOR, fg="white", font=("Arial", 10))
        self.exercise_dropdown.pack(side=tk.LEFT, padx=5)

        def on_dropdown_select(*args):
            val = self.exercise_dropdown_var.get()
            if val != "-- Previous --":
                self.new_exercise_entry.delete(0, tk.END)
                self.new_exercise_entry.insert(0, val)
        self.exercise_dropdown_var.trace("w", on_dropdown_select)

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

# ============================================================
# MODIFIED IN VERSION 7: add_exercise_row - one set to start,
# with an "+ Add Set" button to add more.
#
# In version 5 this method used a simple for loop:
#   for i in range(5):
# which always created all 5 set boxes immediately.
#
# In version 7, the loop is replaced with a nested function
# called add_set. Here is how that works:
#
# - exercise_data now stores 'set_count': 0 alongside the
#   existing 'name' and 'set_inputs' keys. set_count tracks
#   how many set columns currently exist for this exercise.
#
# - add_set is defined inside add_exercise_row so it has
#   access to that specific exercise's row_frame, sets_container,
#   and exercise_data via closure (Python automatically
#   captures the local variables from the outer function).
#
# - The default argument trick (ex_data=exercise_data,
#   container=sets_container) is used to "lock in" the values
#   at the time add_set is defined. Without this, if the user
#   adds two exercises, both Add Set buttons would refer to
#   whichever variables were last assigned - causing both
#   buttons to add sets to the second exercise only.
#
# - Each time add_set runs, it reads the current set_count to
#   know which column to place the new set box in, then
#   increments set_count by 1 ready for the next call.
#
# - grid_columnconfigure(i, weight=1) is called for each new
#   column so that all set columns share the available width
#   equally and expand to fill the exercise row.
#
# - add_set() is called once immediately after being defined
#   so that the user always starts with exactly one set
#   already visible instead of a blank exercise row.
#
# - The "+ Add Set" button is placed below the sets_container
#   and has add_set as its command, so every click adds one
#   more set column to that exercise's row.
# ============================================================
    def add_exercise_row(self):
        ex_name = self.new_exercise_entry.get()
        if not ex_name:
            messagebox.showwarning("Input Error", "Please enter an exercise name first.")
            return

        #main row frame
        row_frame = tk.Frame(self.exercises_container, relief=tk.RIDGE, borderwidth=2, pady=10, bg="#E0E0E0")
        row_frame.pack(fill="x", pady=5)

        # Header for the row (Exercise Name)
        tk.Label(row_frame, text=ex_name, font=("Arial", 16, "bold"), bg="#E0E0E0", width=15, anchor="w").pack(side=tk.TOP, fill="x", padx=10)

        # Grid container for sets - starts empty, sets are added dynamically
        sets_container = tk.Frame(row_frame, bg="#E0E0E0")
        sets_container.pack(fill="x", expand=True, padx=5, pady=5)

        # set_count tracks how many set columns exist so add_set knows which column to use next
        exercise_data = {'name': ex_name, 'set_inputs': [], 'set_count': 0}

        def add_set(ex_data=exercise_data, container=sets_container):
            i = ex_data['set_count']
            # Make this new column share width equally with all others
            container.grid_columnconfigure(i, weight=1)

            set_box = tk.Frame(container, bg="#D0D0D0", bd=1, relief="solid")
            set_box.grid(row=0, column=i, sticky="nsew", padx=5)

            tk.Label(set_box, text=f"SET {i+1}", font=("Arial", 10, "bold"), bg="#D0D0D0").pack(pady=(5, 2))

            # Reps
            tk.Label(set_box, text="Reps", font=("Arial", 8), bg="#D0D0D0").pack()
            reps_entry = tk.Entry(set_box, width=6, justify='center', font=("Arial", 12))
            reps_entry.pack(pady=2)

            # Weight
            tk.Label(set_box, text="Kg/Lbs", font=("Arial", 8), bg="#D0D0D0").pack()
            weight_entry = tk.Entry(set_box, width=6, justify='center', font=("Arial", 12))
            weight_entry.pack(pady=(2, 10))

            ex_data['set_inputs'].append({'reps': reps_entry, 'weight': weight_entry})
            ex_data['set_count'] += 1

        # Show one set immediately so the row isn't blank
        add_set()

        # Button that adds one more set column each time it is clicked
        tk.Button(row_frame, text="+ Add Set", bg="green", fg="white", font=("Arial", 9, "bold"),
                  command=add_set).pack(pady=(5, 0))

#saves a volatile version of the data entered from that column while workout is continued until user presses save workout
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

#executes functions that have been defined, deleting current data and going back to dashboard frame
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

# ============================================================
# MODIFIED IN VERSION 7: open_history - newest entries first.
#
# In version 5, the rows were inserted into the text box in
# the order they came out of the CSV file - which is oldest
# first because rows are always appended to the bottom.
#
# The fix is two lines:
#   user_rows = [row for row in data[1:] if row and row[0] == self.current_user]
#   for row in reversed(user_rows):
#
# First, a list comprehension filters the CSV data down to
# only the rows belonging to the current user, skipping the
# header (data[1:]).
#
# Then reversed() iterates through that list from the last
# item to the first - which means the most recently saved
# workout row is inserted into the text box first, and
# therefore appears at the top when the user reads it.
#
# reversed() does not change or copy the list, it just reads
# it backwards, so this is efficient even with large files.
# ============================================================
    def open_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)

        if os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, mode='r') as file:
                reader = csv.reader(file)
                data = list(reader)

                header = f"{'Date':<12} {'Exercise':<15} {'Set':<5} {'Reps':<5} {'Weight':<8}\n"
                self.history_text.insert(tk.END, header + "-"*60 + "\n")

                # Filter to this user's rows first, then iterate in reverse so newest is at the top
                user_rows = [row for row in data[1:] if row and row[0] == self.current_user]
                for row in reversed(user_rows):
                    self.history_text.insert(tk.END, f"{row[1]:<12} {row[2]:<15} {row[3]:<5} {row[4]:<5} {row[5]:<8}\n")

        self.history_text.config(state=tk.DISABLED)#this line puts the data in from the csv file and locks the text box so users aren't able to enter other things in
        self.show_frame(self.history_frame)

# ============================================================
# REPLACED IN VERSION 7: setup_analytics_frame.
#
# Version 5 had a single analytics view with one text entry
# and one graph type (estimated 1RM line graph). Version 7
# replaces this with three separate analytics tabs selectable
# via buttons at the top of the screen.
#
# Layout overview:
# - A row of three tab buttons: "1RM Progress", "Volume Per
#   Session", "Top Exercises". Each calls show_analytics_tab()
#   with a different tab identifier string.
# - A control row with a text entry and two buttons:
#   "▾ Pick" opens the scrollable exercise picker popup.
#   "Generate" runs whichever tab is currently active.
# - A Canvas widget where the graphs are drawn.
# - A stats_label below the canvas for summary text.
# - A Back button.
#
# self.current_analytics_tab stores which tab is active as a
# plain string ("1rm", "volume", or "top"). generate_graph()
# reads this string to decide which drawing method to call.
# ============================================================
    def setup_analytics_frame(self):
        tk.Label(self.analytics_frame, text="Analytics", bg=BG_COLOR, font=FONT_HEADER).pack(pady=10)

        # Three tab selector buttons at the top
        tab_row = tk.Frame(self.analytics_frame, bg=BG_COLOR)
        tab_row.pack(pady=(0, 10))
        for label, tab_id in [("1RM Progress", "1rm"),
                               ("Volume Per Session", "volume"),
                               ("Top Exercises", "top")]:
            tk.Button(tab_row, text=label, bg=BTN_COLOR, fg="white", font=("Arial", 11, "bold"),
                      relief="solid", bd=BTN_BORDER,
                      command=lambda t=tab_id: self.show_analytics_tab(t)).pack(side=tk.LEFT, padx=8)

        # Control row: text entry + Pick button + Generate button
        ctrl_frame = tk.Frame(self.analytics_frame, bg=BG_COLOR)
        ctrl_frame.pack(pady=10)
        tk.Label(ctrl_frame, text="Exercise Name:", bg=BG_COLOR).pack(side=tk.LEFT)
        self.ana_entry = tk.Entry(ctrl_frame)
        self.ana_entry.pack(side=tk.LEFT, padx=10)

# ============================================================
# ADDED IN VERSION 7: "▾ Pick" button for analytics.
# tkinter's OptionMenu does not scroll. If a user has logged
# 30 different exercises the menu would extend off the screen
# and become unusable. The solution used here is a popup
# window (Toplevel) containing a Listbox with a Scrollbar.
# The Pick button opens this popup by calling
# open_exercise_picker(). See that method for full details.
# ============================================================
        tk.Button(ctrl_frame, text="▾ Pick", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  relief="solid", bd=BTN_BORDER,
                  command=self.open_exercise_picker).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(ctrl_frame, text="Graph", command=self.generate_graph).pack(side=tk.LEFT)

        # Canvas for drawing graphs - same size as version 5
        self.canvas = tk.Canvas(self.analytics_frame, width=800, height=400, bg="white",
                                highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=20)
        self.stats_label = tk.Label(self.analytics_frame, text="", bg=BG_COLOR,
                                    font=("Times New Roman", 12, "bold"))
        self.stats_label.pack(pady=5)
        tk.Button(self.analytics_frame, text="Back", font=("Arial", 14),
                  command=lambda: self.show_frame(self.dashboard_frame)).pack(pady=10)

        # Track which tab is currently active
        self.current_analytics_tab = "1rm"

# ============================================================
# ADDED IN VERSION 7: show_analytics_tab method.
# Called by each tab button. It updates current_analytics_tab,
# clears the canvas and stats text, and if the user switches
# to the Top Exercises tab it draws the bar chart immediately
# because that tab doesn't need the user to type an exercise
# name - it works on all of the user's data at once.
# ============================================================
    def show_analytics_tab(self, tab):
        self.current_analytics_tab = tab
        self.canvas.delete("all")
        self.stats_label.config(text="")
        if tab == "top":
            self.generate_top_exercises()

# ============================================================
# ADDED IN VERSION 7: open_exercise_picker method.
# This creates a small floating popup window to let the user
# select an exercise from a scrollable list. Here is exactly
# how it works step by step:
#
# 1. get_known_exercises() is called to get the sorted list
#    of exercises from the CSV for the current user.
#
# 2. tk.Toplevel(self) creates a new independent window that
#    floats on top of the main app. Unlike a regular Frame,
#    a Toplevel is its own OS window with its own title bar.
#    We call popup.title("") to give it a minimal title bar.
#
# 3. popup.grab_set() makes the popup "modal" - it captures
#    all keyboard and mouse input so the user cannot click
#    anything in the main app until the popup is closed.
#    This prevents confusion from clicking Generate while
#    the popup is still open.
#
# 4. popup.geometry("220x200+X+Y") positions the popup.
#    winfo_rootx() and winfo_rooty() return the pixel position
#    of the main window on the screen. Adding fixed offsets
#    places the popup roughly below the control row.
#
# 5. Inside the popup, a Frame (list_frame) holds both the
#    Listbox and the Scrollbar side by side. The Scrollbar is
#    packed to the RIGHT first, then the Listbox fills the
#    rest. yscrollcommand=scrollbar.set links the Listbox's
#    scroll position to the Scrollbar, and
#    scrollbar.config(command=listbox.yview) links the
#    Scrollbar's drag back to the Listbox. Together these two
#    lines create a two-way connection so both stay in sync.
#
# 6. A for loop inserts each exercise name into the Listbox
#    using listbox.insert(tk.END, ex).
#
# 7. on_select reads the currently highlighted item with
#    listbox.curselection(), which returns a tuple of selected
#    index positions. If something is selected, listbox.get()
#    fetches the text at that index, inserts it into the
#    ana_entry box, and calls popup.destroy() to close the
#    window and release the grab_set lock.
#
# 8. Two bindings are added:
#    <Double-Button-1> fires on_select when the user
#    double-clicks a list item.
#    <Return> fires on_select when the user presses Enter.
#    A Select button also calls on_select for mouse users
#    who prefer single-click then button.
# ============================================================
    def open_exercise_picker(self):
        exercises = self.get_known_exercises()
        if not exercises:
            messagebox.showinfo("No Exercises", "No exercises found. Save a workout first.")
            return

        popup = tk.Toplevel(self)
        popup.title("")
        popup.resizable(False, False)
        popup.grab_set()

        popup.geometry(f"220x200+{self.winfo_rootx() + 380}+{self.winfo_rooty() + 220}")

        tk.Label(popup, text="Select an exercise:", font=("Arial", 10, "bold"),
                 bg=BTN_COLOR, fg="white").pack(fill="x")

        # Frame holds Listbox and Scrollbar side by side
        list_frame = tk.Frame(popup)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(list_frame, font=("Arial", 11), yscrollcommand=scrollbar.set,
                             selectmode=tk.SINGLE, activestyle="dotbox", height=8)
        # Two-way link between scrollbar and listbox
        scrollbar.config(command=listbox.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill="both", expand=True)

        for ex in exercises:
            listbox.insert(tk.END, ex)

        def on_select(event=None):
            selection = listbox.curselection()
            if selection:
                chosen = listbox.get(selection[0])
                self.ana_entry.delete(0, tk.END)
                self.ana_entry.insert(0, chosen)
                popup.destroy()

        listbox.bind("<Double-Button-1>", on_select)
        listbox.bind("<Return>", on_select)

        tk.Button(popup, text="Select", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  command=on_select).pack(pady=(0, 5))

# ============================================================
# MODIFIED IN VERSION 7: generate_graph now routes to the
# correct drawing method based on current_analytics_tab.
# In version 5 it always drew the 1RM graph. Now it checks
# which tab is active and calls the matching method.
# ============================================================
    def generate_graph(self):
        if self.current_analytics_tab == "1rm":
            self._graph_1rm()
        elif self.current_analytics_tab == "volume":
            self._graph_volume()

# ============================================================
# ADDED IN VERSION 7: _graph_1rm method.
# This is the original version 5 graph logic extracted into
# its own method so generate_graph can call it cleanly.
# The graph plots estimated 1 Rep Max (e1RM) for every set
# the user has logged for the chosen exercise.
#
# e1RM formula: weight x (1 + reps / 30)
# This is the Epley formula, a widely used sports science
# equation that estimates what a lifter's maximum single rep
# would be based on a submaximal set.
#
# The drawing works by:
# - Finding the min and max e1RM values to define the Y range.
# - Dividing the canvas width evenly by the number of data
#   points to find the X spacing (x_step).
# - For each point, normalising the Y value as a percentage
#   between min and max, then scaling that to canvas height.
# - Drawing a red oval at each point and a blue line between
#   consecutive points using prev_x, prev_y tracking.
# ============================================================
    def _graph_1rm(self):
        target_ex = self.ana_entry.get().strip()
        self.canvas.delete("all")
        if not target_ex or not os.path.exists(WORKOUT_FILE): return

        y_values = []
        with open(WORKOUT_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if row[0] == self.current_user and row[2].lower() == target_ex.lower():
                    try:
                        reps = int(row[4])
                        weight = float(row[5])
                        e1rm = weight * (1 + reps / 30)  # Epley 1RM formula
                        y_values.append(e1rm)
                    except ValueError:
                        continue

        if not y_values:
            self.canvas.create_text(400, 200, text="No data found for this user/exercise", font=("Arial", 16))
            return

        w, h, margin = 800, 400, 50
        max_v, min_v = max(y_values), min(y_values)
        if max_v == min_v: max_v += 10
        if min_v > 0: min_v -= 10

        num_points = len(y_values)
        x_step = (w - 2 * margin) / max(1, num_points - 1)
        prev_x, prev_y = None, None

        for i, val in enumerate(y_values):
            x = margin + (i * x_step)
            norm_h = (val - min_v) / (max_v - min_v)
            y = h - margin - (norm_h * (h - 2 * margin))
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="red")
            self.canvas.create_text(x, h-margin+20, text=f"{i+1}", font=("Arial", 8))
            if prev_x is not None:
                self.canvas.create_line(prev_x, prev_y, x, y, fill="blue", width=2)
            prev_x, prev_y = x, y

        self.stats_label.config(text=f"Last 1RM: {int(y_values[-1])} kg  |  Best: {int(max(y_values))} kg")

# ============================================================
# ADDED IN VERSION 7: _graph_volume method - new analytics tab.
# This graph shows total training volume per session for the
# chosen exercise. Volume = reps x weight for each set, all
# sets summed per day.
#
# How it works:
# - defaultdict(float) creates a dictionary where any new key
#   automatically starts at 0.0. This means we can write
#   daily[row[1]] += ... without first checking if that date
#   key exists - it is created with 0.0 on first access.
# - The CSV is read and for every matching row, the set's
#   volume (reps x weight) is added to the total for that date.
# - sorted(daily) returns the date keys in chronological order
#   (works because the dates are stored as YYYY-MM-DD strings,
#   which sort alphabetically in the correct date order).
# - The resulting list of daily totals is passed to the shared
#   _draw_line_graph helper which handles all the canvas drawing.
# ============================================================
    def _graph_volume(self):
        target_ex = self.ana_entry.get().strip()
        self.canvas.delete("all")
        if not target_ex or not os.path.exists(WORKOUT_FILE): return

        daily = defaultdict(float)
        with open(WORKOUT_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == self.current_user and row[2].lower() == target_ex.lower():
                    try:
                        daily[row[1]] += int(row[4]) * float(row[5])
                    except ValueError:
                        continue

        if not daily:
            self.canvas.create_text(400, 200, text="No data found for this user/exercise", font=("Arial", 16))
            return

        # Sort by date so the graph goes left to right chronologically
        y_values = [daily[d] for d in sorted(daily)]
        self._draw_line_graph(y_values, "green")
        self.stats_label.config(
            text=f"Total sessions: {len(y_values)}  |  Best volume day: {int(max(y_values))} kg")

# ============================================================
# ADDED IN VERSION 7: generate_top_exercises - new analytics tab.
# This draws a bar chart of the user's top 5 most-logged
# exercises. It does not need an exercise name typed in -
# it scans the entire workout history for the current user.
#
# How it works:
# - Counter() from the collections module is used. Counter
#   works like a dictionary but has a built-in tallying
#   system. Each time counts[row[2]] += 1 runs, the exercise
#   name is used as the key and its count goes up by 1.
# - counts.most_common(5) returns a list of up to 5 tuples
#   in the format [(exercise_name, count), ...], ordered from
#   most to least logged.
# - The bar chart is drawn using canvas rectangles. The height
#   of each bar is calculated as a proportion of max_val so
#   the tallest bar always fills the available space and
#   shorter bars scale proportionally below it.
# - spacing divides the canvas width evenly between bars.
#   x is the centre point of each bar, so bar_width is split
#   equally either side of x using x - bar_width//2 and
#   x + bar_width//2.
# ============================================================
    def generate_top_exercises(self):
        self.canvas.delete("all")
        if not os.path.exists(WORKOUT_FILE): return

        counts = Counter()
        with open(WORKOUT_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row and row[0] == self.current_user:
                    counts[row[2]] += 1

        if not counts:
            self.canvas.create_text(400, 200, text="No workout data yet.", font=("Arial", 16))
            return

        top = counts.most_common(5)
        w, h, margin = 800, 400, 50
        bar_width = 80
        max_val = top[0][1]
        spacing = (w - 2 * margin) // len(top)

        for i, (ex, count) in enumerate(top):
            x = margin + i * spacing + spacing // 2
            bar_h = int((count / max_val) * (h - 2 * margin))
            y_top = h - margin - bar_h
            self.canvas.create_rectangle(x - bar_width // 2, y_top,
                                         x + bar_width // 2, h - margin, fill=BTN_COLOR)
            self.canvas.create_text(x, y_top - 10, text=str(count), font=("Arial", 10, "bold"))
            self.canvas.create_text(x, h - margin + 15, text=ex[:20], font=("Arial", 9))

        self.stats_label.config(text=f"Your most-trained exercise: {top[0][0]}")

# ============================================================
# ADDED IN VERSION 7: _draw_line_graph helper method.
# Both _graph_1rm and _graph_volume need to draw a line graph
# on the canvas using the same logic. Rather than duplicating
# that code in both methods, it lives here once and both
# methods call it with their data and a chosen line colour.
#
# Parameters:
# - y_values: a list of numeric values to plot (one per point)
# - color: the colour string for the connecting line
#
# The normalisation formula (val - min_v) / (max_v - min_v)
# converts any value in the data range to a 0.0-1.0 scale.
# Multiplying by the drawable height and inverting with
# (h - margin - ...) converts that into a canvas Y coordinate
# where higher values appear higher on screen.
# ============================================================
    def _draw_line_graph(self, y_values, color):
        w, h, margin = 800, 400, 50
        max_v, min_v = max(y_values), min(y_values)
        if max_v == min_v: max_v += 10
        if min_v > 0: min_v -= 10

        x_step = (w - 2 * margin) / max(1, len(y_values) - 1)
        prev_x, prev_y = None, None

        for i, val in enumerate(y_values):
            x = margin + i * x_step
            norm_h = (val - min_v) / (max_v - min_v)
            y = h - margin - (norm_h * (h - 2 * margin))
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="red")
            self.canvas.create_text(x, h - margin + 20, text=f"{i+1}", font=("Arial", 8))
            if prev_x is not None:
                self.canvas.create_line(prev_x, prev_y, x, y, fill=color, width=2)
            prev_x, prev_y = x, y

# ============================================================
# ADDED IN VERSION 7: setup_settings_frame and its action
# methods. The settings screen is a new frame laid out with
# tkinter's grid geometry manager (instead of pack) so that
# labels and entry boxes can be aligned in neat columns.
#
# It provides three sections:
#
# 1. CHANGE USERNAME
#    Reads all rows from login_info.csv, rewrites the file
#    with the matching row updated to the new username. It
#    also rewrites my_workout_data.csv to update the username
#    column there too, otherwise the user's history would
#    become invisible (it's filtered by username).
#
# 2. CHANGE PASSWORD
#    Same pattern - reads, rewrites with the changed row.
#    Does not apply any validation here since version 7 does
#    not include the password rules feature.
#
# 3. VIEW WORKOUT COUNT
#    Reads the workout CSV and collects unique dates for this
#    user into a set. The length of that set is the number of
#    distinct days a workout was saved. This is more meaningful
#    than counting raw rows (which would count every set).
#
# 4. DELETE ACCOUNT
#    Shows a confirmation dialog first. If confirmed, rewrites
#    both CSV files keeping only rows that do NOT belong to
#    the current user. Then resets current_user and returns
#    to the login screen.
# ============================================================
    def setup_settings_frame(self):
        top_bar = tk.Frame(self.settings_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=10, padx=10)
        tk.Button(top_bar, text="Back", font=("Arial", 12), bg=BTN_COLOR, fg="white",
                  relief="solid", bd=BTN_BORDER,
                  command=lambda: self.show_frame(self.dashboard_frame)).pack(side=tk.LEFT)
        tk.Label(top_bar, text="SETTINGS", bg=BG_COLOR, fg="white",
                 font=FONT_HEADER).pack(side=tk.LEFT, expand=True)

        content = tk.Frame(self.settings_frame, bg=BG_COLOR)
        content.pack(expand=True, pady=20)

        # --- Change Username ---
        tk.Label(content, text="Change Username", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 16, "bold")).grid(row=0, column=0, columnspan=2,
                                                             pady=(10, 2), sticky="w")
        tk.Label(content, text="New Username:", bg=BG_COLOR, fg="white",
                 font=FONT_BODY).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.new_username_entry = tk.Entry(content, font=FONT_BODY, width=20,
                                           bg=BTN_COLOR, fg="white")
        self.new_username_entry.grid(row=1, column=1, pady=5)
        tk.Button(content, text="Update Username", bg=BTN_COLOR, fg="white",
                  font=("Arial", 10, "bold"), relief="solid", bd=BTN_BORDER,
                  command=self.change_username).grid(row=2, column=0, columnspan=2, pady=5)

        # --- Change Password ---
        tk.Label(content, text="Change Password", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 16, "bold")).grid(row=3, column=0, columnspan=2,
                                                             pady=(20, 2), sticky="w")
        tk.Label(content, text="New Password:", bg=BG_COLOR, fg="white",
                 font=FONT_BODY).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.new_password_entry = tk.Entry(content, show="*", font=FONT_BODY, width=20,
                                           bg=BTN_COLOR, fg="white")
        self.new_password_entry.grid(row=4, column=1, pady=5)
        tk.Button(content, text="Update Password", bg=BTN_COLOR, fg="white",
                  font=("Arial", 10, "bold"), relief="solid", bd=BTN_BORDER,
                  command=self.change_password).grid(row=5, column=0, columnspan=2, pady=5)

        # --- Account Info ---
        tk.Label(content, text="Account Info", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 16, "bold")).grid(row=6, column=0, columnspan=2,
                                                             pady=(20, 2), sticky="w")
        tk.Button(content, text="View Workout Count", bg=BTN_COLOR, fg="white",
                  font=("Arial", 10, "bold"), relief="solid", bd=BTN_BORDER,
                  command=self.view_workout_count).grid(row=7, column=0, columnspan=2, pady=5)
        self.workout_count_label = tk.Label(content, text="", bg=BG_COLOR, fg="white",
                                            font=FONT_BODY)
        self.workout_count_label.grid(row=8, column=0, columnspan=2)

        # --- Delete Account ---
        tk.Button(content, text="DELETE ACCOUNT", bg="red", fg="white",
                  font=("Arial", 11, "bold"), relief="solid", bd=BTN_BORDER,
                  command=self.delete_account).grid(row=9, column=0, columnspan=2, pady=(30, 5))

    def change_username(self):
        new_u = self.new_username_entry.get().strip()
        if not new_u:
            messagebox.showerror("Error", "Please enter a new username.")
            return
        rows = []
        with open(LOGIN_FILE, 'r') as f:
            rows = list(csv.reader(f))
        for row in rows[1:]:
            if row and row[0] == new_u:
                messagebox.showerror("Error", "Username already taken.")
                return
        # Rewrite login file with updated username
        with open(LOGIN_FILE, 'w', newline='') as f:
            for row in rows:
                if row and row[0] == self.current_user:
                    csv.writer(f).writerow([new_u, row[1]])
                else:
                    csv.writer(f).writerow(row)
        # Rewrite workout file so history stays linked to the new username
        if os.path.exists(WORKOUT_FILE):
            wrows = []
            with open(WORKOUT_FILE, 'r') as f:
                wrows = list(csv.reader(f))
            with open(WORKOUT_FILE, 'w', newline='') as f:
                for row in wrows:
                    if row and row[0] == self.current_user:
                        row[0] = new_u
                    csv.writer(f).writerow(row)
        self.current_user = new_u
        self.update_dashboard_username()
        self.new_username_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Username updated to '{new_u}'.")

    def change_password(self):
        new_p = self.new_password_entry.get().strip()
        if not new_p:
            messagebox.showerror("Error", "Please enter a new password.")
            return
        rows = []
        with open(LOGIN_FILE, 'r') as f:
            rows = list(csv.reader(f))
        with open(LOGIN_FILE, 'w', newline='') as f:
            for row in rows:
                if row and row[0] == self.current_user:
                    csv.writer(f).writerow([row[0], new_p])
                else:
                    csv.writer(f).writerow(row)
        self.new_password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Password updated.")

    def view_workout_count(self):
        # Count unique dates to get number of distinct workout sessions
        dates = set()
        if os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row and row[0] == self.current_user:
                        dates.add(row[1])
        self.workout_count_label.config(text=f"Total workout sessions: {len(dates)}")

    def delete_account(self):
        confirm = messagebox.askyesno("Delete Account",
                                      "Are you sure? This will permanently delete your account and all workout data.")
        if not confirm: return
        # Remove from login file
        rows = []
        with open(LOGIN_FILE, 'r') as f:
            rows = list(csv.reader(f))
        with open(LOGIN_FILE, 'w', newline='') as f:
            for row in rows:
                if row and row[0] != self.current_user:
                    csv.writer(f).writerow(row)
        # Remove from workout file
        if os.path.exists(WORKOUT_FILE):
            rows = []
            with open(WORKOUT_FILE, 'r') as f:
                rows = list(csv.reader(f))
            with open(WORKOUT_FILE, 'w', newline='') as f:
                for row in rows:
                    if row and row[0] != self.current_user:
                        csv.writer(f).writerow(row)
        self.current_user = None
        messagebox.showinfo("Deleted", "Your account has been deleted.")
        self.show_frame(self.login_frame)


#simply runs the programme and everything defined in it
if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
