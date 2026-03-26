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
        self.geometry("1200x720")
        self.configure(bg=BG_COLOR)

        self.current_user = None

        self.check_files()
        self.current_exercise_widgets = []

# ============================================================
# ADDED IN VERSION 8: protocol("WM_DELETE_WINDOW") intercepts
# the window's X button (the close button in the top-right
# corner on Windows/Linux, or top-left on Mac). Normally
# clicking X instantly destroys the window. By registering
# self.confirm_quit as the handler for this protocol event,
# we redirect that click to our own method instead, which
# shows a confirmation dialog before actually closing.
# This is how the same confirmation shown by EXIT APP buttons
# is also triggered when the user uses the OS close button.
# ============================================================
        self.protocol("WM_DELETE_WINDOW", self.confirm_quit)

#creates main container frame
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)

# ADDED IN VERSION 7: settings_frame added alongside existing frames.
        self.login_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.dashboard_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.workout_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.history_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.analytics_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.settings_frame = tk.Frame(self.container, bg=BG_COLOR)

        self.setup_login_frame()
        self.setup_dashboard_frame()
        self.setup_workout_frame()
        self.setup_history_frame()
        self.setup_analytics_frame()
        self.setup_settings_frame()
#makes the login screen appear as first frame in container when app is run
        self.show_frame(self.login_frame)

#this checks to see if there's a correctly named csv file already in the folder and creates one if not
    def check_files(self):
        if not os.path.exists(LOGIN_FILE):
            with open(LOGIN_FILE, mode='w', newline='') as f:
                csv.writer(f).writerow(["Username", "Password"])

        if not os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, mode='w', newline='') as f:
# ============================================================
# MODIFIED IN VERSION 8: "Notes" column added to the CSV
# header. This column stores the optional session note the
# user can type before saving a workout. Existing CSV files
# without this column will still load and display correctly
# because open_history and save_workout use len(row) checks
# before reading index 6. Only newly created CSV files will
# have the column header present from the start.
# ============================================================
                csv.writer(f).writerow(["Username", "Date", "Exercise", "Set_Number", "Reps", "Weight", "Notes"])

# MODIFIED IN VERSION 7: settings_frame included in the hide loop.
    def show_frame(self, frame):
        for f in [self.login_frame, self.dashboard_frame, self.workout_frame,
                  self.history_frame, self.analytics_frame, self.settings_frame]:
            f.pack_forget()
        frame.pack(fill="both", expand=True)

# ============================================================
# ADDED IN VERSION 8: confirm_quit method.
# This is the single method called by every quit action in
# the app - both the EXIT APP buttons and the OS window X
# button. Centralising the quit logic here means the
# confirmation behaviour is identical everywhere and only
# needs to be changed in one place if requirements change.
#
# How it works:
# - messagebox.askyesno() displays a dialog with Yes and No
#   buttons and returns True if the user clicks Yes.
# - self.destroy() closes the tkinter window and ends the
#   mainloop cleanly. This is the correct way to close a
#   tkinter application programmatically. The old approach
#   of self.quit() was causing issues on Windows because
#   quit() stops the mainloop but does not always destroy
#   the window, which can leave a frozen empty window behind.
#   destroy() tears down the window completely and reliably
#   on all platforms.
# ============================================================
    def confirm_quit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit the app?"):
            self.destroy()

    #login menu frame
    def setup_login_frame(self):#visual labels and boxes
        top_bar = tk.Frame(self.login_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=10, padx=10)
#creating buttons with styling
# ============================================================
# MODIFIED IN VERSION 8: EXIT APP button now calls
# self.confirm_quit instead of self.quit. This applies to
# all EXIT APP buttons across every screen. confirm_quit
# shows a Yes/No dialog and calls self.destroy() on
# confirmation, which is more reliable than self.quit()
# on Windows where quit() can leave a frozen blank window.
# ============================================================
        tk.Button(top_bar, text="EXIT APP", bg=BTN_COLOR, fg="white",
                  relief="solid", bd=BTN_BORDER, font=("Arial", 10, "bold"),
                  command=self.confirm_quit).pack(side=tk.LEFT)

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

# ============================================================
# MODIFIED IN VERSION 8: perform_signup now validates the
# password before creating the account.
#
# Two rules are enforced:
#
# Rule 1 - Length: len(p) checks how many characters are in
# the password string. The condition (3 <= len(p) <= 12) is
# a Python chained comparison - it checks that the length
# is at least 3 AND at most 12 in a single readable line.
# If this fails, showerror displays the message and return
# stops the function immediately so no account is created.
#
# Rule 2 - Characters: p.isalnum() is a built-in Python
# string method that returns True only if every character
# in the string is either a letter (a-z, A-Z) or a digit
# (0-9). If the password contains a space, symbol, or
# punctuation mark, isalnum() returns False and the error
# message is shown.
#
# Both checks happen before the username duplicate check
# and before anything is written to the CSV, so an invalid
# password is caught immediately without touching the file.
# ============================================================
    def perform_signup(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        if not u or not p:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Rule 1: Password must be between 3 and 12 characters long
        if not (5 <= len(p) <= 12):
            messagebox.showerror("Error", "Password must be between 3 and 12 characters.")
            return

        # Rule 2: Password may only contain letters and numbers
        if not p.isalnum():
            messagebox.showerror("Error", "Password can only contain letters and numbers.")
            return

        if not u.isalnum():
            messagebox.showerror("Error", "Username can only contain letters and numbers.")
            return

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
                  command=self.confirm_quit).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(top_bar, text="LOG OUT", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=self.logout).pack(side=tk.LEFT)

# ADDED IN VERSION 7: SETTINGS button in the dashboard top bar.
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
# MODIFIED IN VERSION 7: NEW WORKOUT calls open_workout to refresh the dropdown first.
        create_big_btn(content_area, "NEW\nWORKOUT", self.open_workout)
# MODIFIED IN VERSION 7: ANALYTICS calls open_analytics to refresh the exercise list first.
        create_big_btn(content_area, "ANALYTICS", self.open_analytics)

    def update_dashboard_username(self):
        if self.current_user:
            self.lbl_username.config(text=self.current_user.upper())

# MODIFIED IN VERSION 8.1: open_workout no longer needs to rebuild a dropdown menu.
# The OptionMenu has been replaced with a scrollable popup picker, so this method
# simply shows the workout frame directly.
    def open_workout(self):
        self.show_frame(self.workout_frame)

# ADDED IN VERSION 7: Opens analytics screen.
    def open_analytics(self):
        self.show_frame(self.analytics_frame)

# ============================================================
# ADDED IN VERSION 7: get_known_exercises reads the CSV and
# returns a sorted, deduplicated list of exercise names for
# the current user. A set is used to remove duplicates
# automatically, then sorted() alphabetises the result.
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

# ============================================================
        # ADDED IN VERSION 8.2 (refactor): Single shared picker method.
        # Previously there were two near-identical methods:
        #   open_workout_exercise_picker  -> wrote to new_exercise_entry
        #   open_exercise_picker          -> wrote to ana_entry
        # The only difference between them was that one line.
        # This version accepts target_entry as a parameter - the caller
        # passes in whichever Entry widget should receive the chosen
        # exercise name. Both the workout Pick button and the analytics
        # Pick button now call this same method via a lambda that
        # supplies the correct entry widget:
        #   command=lambda: self.open_exercise_picker(self.new_exercise_entry)
        #   command=lambda: self.open_exercise_picker(self.ana_entry)
        # Everything else in the popup is identical for both callers.
        # ============================================================

    def open_exercise_picker(self, target_entry):
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
        list_frame = tk.Frame(popup)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(list_frame, font=("Arial", 11), yscrollcommand=scrollbar.set,
                             selectmode=tk.SINGLE, activestyle="dotbox", height=8)
        #this is the link between scrollbar and listbox
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill="both", expand=True)
        for ex in exercises:
            listbox.insert(tk.END, ex)
        def on_select(event=None):
            selection = listbox.curselection()
            if selection:
                chosen = listbox.get(selection[0])
                target_entry.delete(0, tk.END)
                target_entry.insert(0, chosen)
                popup.destroy()
        listbox.bind("<Double-Button-1>", on_select)
        listbox.bind("<Return>", on_select)
        tk.Button(popup, text="Select", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  command=on_select).pack(pady=(0, 5))

#new workout tab
    def setup_workout_frame(self):
        tk.Label(self.workout_frame, text="New Workout", bg=BG_COLOR, font=FONT_HEADER).pack(pady=10)

        control_frame = tk.Frame(self.workout_frame, bg=BG_COLOR)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Exercise Name:", bg=BG_COLOR, font=FONT_BODY).pack(side=tk.LEFT, padx=5)
        self.new_exercise_entry = tk.Entry(control_frame, font=FONT_BODY, width=20)
        self.new_exercise_entry.pack(side=tk.LEFT, padx=5)

# MODIFIED IN VERSION 8.1: OptionMenu replaced with scrollable popup picker button.
# Matches the same pattern used on the analytics screen.

        tk.Button(control_frame, text="▾ Pick", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  relief="solid", bd=BTN_BORDER,
                  command=lambda: self.open_exercise_picker(self.new_exercise_entry)).pack(side=tk.LEFT, padx=(10, 5))

        tk.Button(control_frame, text="+ Add Exercise", bg="green", fg="white", font=("Arial", 10, "bold"),
                  command=self.add_exercise_row).pack(side=tk.LEFT, padx=10)

        # Container needs to allow children to expand
        self.exercises_container = tk.Frame(self.workout_frame, bg=BG_COLOR)
        self.exercises_container.pack(fill="both", expand=True, padx=20, pady=5)

# ============================================================
# ADDED IN VERSION 8: Session notes section.
# A label and a Text widget are packed below the exercises
# container. The Text widget (self.session_notes_entry) is
# taller than a standard Entry and allows multi-line input,
# which is more suitable for free-form notes.
#
# Text is used rather than Entry here because Entry is a
# single-line widget. Text supports multiple lines and has
# a slightly different API - content is retrieved with
# .get("1.0", tk.END) where "1.0" means line 1, character 0
# (the very start of the text), and tk.END means the very
# end. This is different from Entry's .get() which takes no
# arguments. The .strip() call removes any trailing newline
# that Text always appends when reading its content.
#
# The notes box is cleared in clear_workout_screen so it
# resets properly after a workout is saved or discarded.
# ============================================================
        notes_frame = tk.Frame(self.workout_frame, bg=BG_COLOR)
        notes_frame.pack(fill="x", padx=20, pady=(0, 5))
        tk.Label(notes_frame, text="Session Notes (optional):", bg=BG_COLOR,
                 font=FONT_BODY).pack(anchor="w")
        self.session_notes_entry = tk.Text(notes_frame, font=("Arial", 11), height=3,
                                           width=60, bg=BTN_COLOR, fg="white",
                                           insertbackground="white")
        self.session_notes_entry.pack(fill="x")

        btn_frame = tk.Frame(self.workout_frame, bg=BG_COLOR)
        btn_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Button(btn_frame, text="Save Workout", bg="blue", fg="white", font=("Arial", 14),
                  command=self.save_workout).pack(side=tk.LEFT, padx=20)
        tk.Button(btn_frame, text="Back", font=("Arial", 14),
                  command=self.confirm_back_from_workout).pack(side=tk.LEFT, padx=20)

# ============================================================
# ADDED IN VERSION 8.2: confirm_back method.
# Called by the Back button on the workout screen.
#
# The method checks whether the user has added any exercise
# rows (self.current_exercise_widgets is non-empty) OR typed
# anything in the notes box before deciding whether to ask.
#
# - If neither condition is true the screen is blank and there
#   is nothing to lose, so the user goes straight back to the
#   dashboard without any dialog.
#
# - If there is data, askyesno shows a Yes/No dialog. If the
#   user clicks Yes, clear_workout_screen() is called first
#   to wipe all exercise rows, set data, and the notes box
#   before navigating away. Without this call the data would
#   persist in the widgets and reappear the next time the
#   user opens the New Workout screen in the same session.
# ============================================================
    def confirm_back_from_workout(self):
                #Only ask if there is something to lose
                if self.current_exercise_widgets:
                    if messagebox.askyesno("Go Back", "You have unsaved exercises. Are you sure you want to go back? Your workout will be lost."):
                        self.clear_workout_screen()
                        self.show_frame(self.dashboard_frame)
                else:
                    self.show_frame(self.dashboard_frame)

# MODIFIED IN VERSION 7: One set shown at start, + Add Set button adds more dynamically.
# See version 7 comments for full explanation of the nested add_set function and
# the default argument trick used to lock in each exercise's container reference.
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
        if not self.current_exercise_widgets:
# ============================================================
# MODIFIED IN VERSION 8: Blank workout error message.
# In version 7, if Save Workout was pressed with no exercises
# added, the method silently returned with no feedback using:
#   if not self.current_exercise_widgets: return
# The user had no way to know why nothing happened.
#
# In version 8, a showerror messagebox is shown before the
# return so the user gets a clear explanation. showerror is
# used rather than showwarning because attempting to save
# empty data is a more significant mistake - the red icon
# communicates this better than the yellow warning icon.
# ============================================================
            messagebox.showerror("Nothing to Save",
                                 "You haven't added any exercises yet.\nUse '+ Add Exercise' to add exercises before saving.")
            return

# ============================================================
# ADDED IN VERSION 8.2: Save confirmation dialog.
# askyesno returns True if the user clicks Yes and False if
# they click No or close the dialog. The not (...) means the
# function returns early (cancelling the save) if the user
# does not confirm. The actual save logic only runs if they
# click Yes.
# ============================================================
        if not messagebox.askyesno("Save Workout",
                                   "Ready to save this workout?"):
            return

        today = datetime.now().strftime("%d/%m/%Y")
        data_to_save = []

# ============================================================
# ADDED IN VERSION 8: Reading the session notes.
# self.session_notes_entry.get("1.0", tk.END) retrieves all
# text from the Text widget. "1.0" is the start position
# (line 1, character 0) and tk.END is the end. .strip()
# removes the trailing newline character that tkinter's Text
# widget automatically appends. If the user left the notes
# box empty, notes will be an empty string "".
# ============================================================
        notes = self.session_notes_entry.get("1.0", tk.END).strip()

        for ex_item in self.current_exercise_widgets:
            name = ex_item['name']
            for i, inputs in enumerate(ex_item['set_inputs']):
                r_txt = inputs['reps'].get()
                w_txt = inputs['weight'].get()
                if r_txt and w_txt:
                    try:
# MODIFIED IN VERSION 8: notes variable appended to each row.
# The same note applies to the whole session so it is saved
# on every set row for that save. This keeps the CSV structure
# flat (one row per set) without needing a separate notes file.
                        data_to_save.append([self.current_user, today, name, i+1, int(r_txt), float(w_txt), notes])
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
# ADDED IN VERSION 8: Clear the notes box when the screen resets so old notes
# don't persist into the next workout session.
        self.session_notes_entry.delete("1.0", tk.END)

    # history
    def setup_history_frame(self):
        tk.Label(self.history_frame, text="Workout History", bg=BG_COLOR, font=FONT_HEADER).pack(pady=10)
        self.history_text = tk.Text(self.history_frame, width=90, height=20, font=("Courier", 12))
        self.history_text.pack(pady=10)
        tk.Button(self.history_frame, text="Back", font=("Arial", 14),
                  command=lambda: self.show_frame(self.dashboard_frame)).pack(pady=10)

# MODIFIED IN VERSION 7: Rows reversed so newest entries appear at the top.
# MODIFIED IN VERSION 8: Notes column now displayed in the history view.
    def open_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)

        if os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, mode='r') as file:
                reader = csv.reader(file)
                data = list(reader)

# ============================================================
# MODIFIED IN VERSION 8: History header updated to include
# the Notes column. The column widths in the f-string use
# Python's format spec :<N to left-align text in a field of
# N characters. Notes gets 25 characters of space so short
# notes display cleanly alongside the numeric columns.
# The divider line is extended to 85 dashes to match.
# ============================================================
                header = f"{'Date':<12} {'Exercise':<15} {'Set':<5} {'Reps':<5} {'Weight':<8} {'Notes':<25}\n"
                self.history_text.insert(tk.END, header + "-"*85 + "\n")

                # Filter to this user's rows first, then reverse so newest is at the top
                user_rows = [row for row in data[1:] if row and row[0] == self.current_user]
                for row in reversed(user_rows):
# ============================================================
# MODIFIED IN VERSION 8: Each row now reads index 6 for notes.
# len(row) > 6 guards against rows saved before this version
# which only have 6 columns (indices 0-5). If index 6 does
# not exist, notes_col defaults to an empty string so old
# data still displays correctly without crashing.
# ============================================================
                    notes_col = row[6] if len(row) > 6 else ""
                    self.history_text.insert(tk.END,
                        f"{row[1]:<12} {row[2]:<15} {row[3]:<5} {row[4]:<5} {row[5]:<8} {notes_col:<25}\n")

        self.history_text.config(state=tk.DISABLED)#this line puts the data in from the csv file and locks the text box so users aren't able to enter other things in
        self.show_frame(self.history_frame)

# REPLACED IN VERSION 7: Analytics now has 3 tabs - 1RM Progress, Volume Per Session,
# Top Exercises. See version 7 comments for full explanation.
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

        # Control row: text entry + Pick button + Graph button
        ctrl_frame = tk.Frame(self.analytics_frame, bg=BG_COLOR)
        ctrl_frame.pack(pady=10)
        tk.Label(ctrl_frame, text="Exercise Name:", bg=BG_COLOR).pack(side=tk.LEFT)
        self.ana_entry = tk.Entry(ctrl_frame)
        self.ana_entry.pack(side=tk.LEFT, padx=10)

# ADDED IN VERSION 7: Scrollable picker popup for analytics exercise selection.

        tk.Button(ctrl_frame, text="▾ Pick", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  relief="solid", bd=BTN_BORDER,
                  command=lambda: self.open_exercise_picker(self.ana_entry)).pack(side=tk.LEFT, padx=(0, 10))

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

# ADDED IN VERSION 7: Switches active analytics tab. Draws Top Exercises immediately
# since it needs no user input.
    def show_analytics_tab(self, tab):
        self.current_analytics_tab = tab
        self.canvas.delete("all")
        self.stats_label.config(text="")
        if tab == "top":
            self.generate_top_exercises()

# ============================================================
# ADDED IN VERSION 7: Scrollable exercise picker popup.
# Opens a Toplevel window with a Listbox + Scrollbar so the
# user can select an exercise from a scrollable list instead
# of typing. grab_set() makes it modal. The two-way link
# between Listbox and Scrollbar (yscrollcommand + yview)
# keeps both in sync. Double-click, Enter, or the Select
# button all confirm the selection and close the popup.
# See version 7 comments for the full step-by-step breakdown.
# ============================================================


# MODIFIED IN VERSION 7: Routes to the correct graph method based on active tab.
    def generate_graph(self):
        if self.current_analytics_tab == "1rm":
            self._graph_1rm()
        elif self.current_analytics_tab == "volume":
            self._graph_volume()

# ADDED IN VERSION 7: 1RM line graph. Plots Epley estimated 1 rep max for every
# logged set of the chosen exercise. See version 7 comments for full explanation.
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

# ADDED IN VERSION 7: Volume line graph. Plots total reps x weight per day for the
# chosen exercise. Uses defaultdict to sum volume without needing key existence checks.
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

# ADDED IN VERSION 7: Top Exercises bar chart. Uses Counter to tally set rows per
# exercise, then draws proportional bars for the top 5. No exercise name needed.
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

# ADDED IN VERSION 7: Shared line graph drawing helper. Both _graph_1rm and
# _graph_volume call this with their data and a colour string.
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

# ADDED IN VERSION 7: Settings screen with change username, change password,
# workout count, and delete account. Uses grid geometry for column alignment.
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

# ============================================================
# MODIFIED IN VERSION 8: change_password in Settings now also
# applies the same password validation rules as perform_signup.
# This ensures the rules are consistently enforced whether a
# user sets their password during sign-up or changes it later.
# The same two checks (length 3-12 and isalnum()) are used
# so the rules are identical in both places.
# ============================================================
    def change_password(self):
        new_p = self.new_password_entry.get().strip()
        if not new_p:
            messagebox.showerror("Error", "Please enter a new password.")
            return

        # Enforce the same rules as sign-up
        if not (5 <= len(new_p) <= 12):
            messagebox.showerror("Error", "Password must be between 5 and 12 characters.")
            return
        if not new_p.isalnum():
            messagebox.showerror("Error", "Password can only contain letters and numbers.")
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
