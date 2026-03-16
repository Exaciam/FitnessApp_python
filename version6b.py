#importing libraries
import tkinter as tk
from tkinter import messagebox
import csv
import os
import sys
from datetime import datetime
from collections import defaultdict, Counter
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
        self.geometry("1200x750")
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
        # --- ADDED: Settings frame ---
        self.settings_frame = tk.Frame(self.container, bg=BG_COLOR)

        self.setup_login_frame()
        self.setup_dashboard_frame()
        self.setup_workout_frame()
        self.setup_history_frame()
        self.setup_analytics_frame()
        # --- ADDED: Settings frame setup ---
        self.setup_settings_frame()
#makes the login screen appear as first frame in container when app is run
        self.show_frame(self.login_frame)

#this checks to see if there;s a correctly name csv file already in the foler and creates one if not
    def check_files(self):
        if not os.path.exists(LOGIN_FILE):
            with open(LOGIN_FILE, mode='w', newline='') as f:
                csv.writer(f).writerow(["Username", "Password"])

        if not os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, mode='w', newline='') as f:
                # --- MODIFIED: Added Notes column ---
                csv.writer(f).writerow(["Username", "Date", "Exercise", "Set_Number", "Reps", "Weight", "Notes"])

#The navigation tool. It loops through a list of all frames, uses pack_forget() to hide them all, and then uses pack() to show only the frame which has been requested/clicked on
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

    # --- ADDED: Password validation on signup ---
    def perform_signup(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        if not u or not p:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Password length check (3-12 characters)
        if not (3 <= len(p) <= 12):
            messagebox.showerror("Error", "Password must be between 3 and 12 characters.")
            return

        # Only letters and numbers allowed
        if not p.isalnum():
            messagebox.showerror("Error", "Password can only contain letters and numbers.")
            return

        with open(LOGIN_FILE, 'r') as f:
            for row in csv.reader(f):
                if row and row[0] == u:
                    messagebox.showerror("Error", "Username taken.")
                    return

        with open(LOGIN_FILE, 'a', newline='') as f:
            csv.writer(f).writerow([u, p])
        messagebox.showinfo("Success", "Account created!")

    # --- ADDED: Logout confirmation ---
    def logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.current_user = None
            self.show_frame(self.login_frame)

    #dashboard
    def setup_dashboard_frame(self):
        top_bar = tk.Frame(self.dashboard_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=10, padx=10)

        tk.Button(top_bar, text="EXIT APP", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=self.quit).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(top_bar, text="LOG OUT", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=self.logout).pack(side=tk.LEFT)
        # --- ADDED: Settings button in top bar ---
        tk.Button(top_bar, text="SETTINGS", bg=BTN_COLOR, fg="white", relief="solid", bd=BTN_BORDER,
                  command=lambda: self.show_frame(self.settings_frame)).pack(side=tk.LEFT, padx=(5, 0))

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
        # --- MODIFIED: Opens open_workout to refresh exercise dropdown ---
        create_big_btn(content_area, "NEW\nWORKOUT", self.open_workout)
        create_big_btn(content_area, "ANALYTICS", lambda: self.show_frame(self.analytics_frame))

    def update_dashboard_username(self):
        if self.current_user:
            self.lbl_username.config(text=self.current_user.upper())

    # --- ADDED: Refreshes exercise dropdown then opens workout screen ---
    def open_workout(self):
        known = self.get_known_exercises()
        menu = self.exercise_dropdown["menu"]
        menu.delete(0, "end")
        menu.add_command(label="-- Previous --", command=lambda: self.exercise_dropdown_var.set("-- Previous --"))
        for ex in known:
            menu.add_command(label=ex, command=lambda e=ex: self.exercise_dropdown_var.set(e))
        self.exercise_dropdown_var.set("-- Previous --")
        self.show_frame(self.workout_frame)

    # --- ADDED: Reads CSV and returns sorted list of exercises this user has done before ---
    def get_known_exercises(self):
        exercises = set()
        if os.path.exists(WORKOUT_FILE):
            with open(WORKOUT_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)
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

        # --- ADDED: Dropdown for previously entered exercises ---
        tk.Label(control_frame, text="or pick:", bg=BG_COLOR, font=FONT_BODY).pack(side=tk.LEFT, padx=(10, 2))
        self.exercise_dropdown_var = tk.StringVar(value="-- Previous --")
        self.exercise_dropdown = tk.OptionMenu(control_frame, self.exercise_dropdown_var, "-- Previous --")
        self.exercise_dropdown.config(bg=BTN_COLOR, fg="white", font=("Arial", 10))
        self.exercise_dropdown.pack(side=tk.LEFT, padx=5)

        # When a dropdown option is selected, fill the text entry automatically
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
        self.exercises_container.pack(fill="both", expand=True, padx=20, pady=5)

        # --- ADDED: Notes section for each workout ---
        notes_frame = tk.Frame(self.workout_frame, bg=BG_COLOR)
        notes_frame.pack(fill="x", padx=20, pady=(0, 5))
        tk.Label(notes_frame, text="Workout Notes:", bg=BG_COLOR, font=FONT_BODY).pack(anchor="w")
        self.workout_notes_entry = tk.Text(notes_frame, font=("Arial", 11), height=3, width=60,
                                           bg=BTN_COLOR, fg="white")
        self.workout_notes_entry.pack(fill="x")

        btn_frame = tk.Frame(self.workout_frame, bg=BG_COLOR)
        btn_frame.pack(side=tk.BOTTOM, pady=15)

        tk.Button(btn_frame, text="Save Workout", bg="blue", fg="white", font=("Arial", 14),
                  command=self.save_workout).pack(side=tk.LEFT, padx=20)
        # --- MODIFIED: Back button now asks confirmation ---
        tk.Button(btn_frame, text="Back", font=("Arial", 14),
                  command=self.confirm_back_from_workout).pack(side=tk.LEFT, padx=20)

    # --- ADDED: One set to start, with an Add Set button per exercise ---
    def add_exercise_row(self):
        ex_name = self.new_exercise_entry.get()
        if not ex_name:
            messagebox.showwarning("Input Error", "Please enter an exercise name first.")
            return

        row_frame = tk.Frame(self.exercises_container, relief=tk.RIDGE, borderwidth=2, pady=10, bg="#E0E0E0")
        row_frame.pack(fill="x", pady=5)

        tk.Label(row_frame, text=ex_name, font=("Arial", 16, "bold"), bg="#E0E0E0", width=15, anchor="w").pack(side=tk.TOP, fill="x", padx=10)

        sets_container = tk.Frame(row_frame, bg="#E0E0E0")
        sets_container.pack(fill="x", expand=True, padx=5, pady=5)

        exercise_data = {'name': ex_name, 'set_inputs': [], 'sets_container': sets_container, 'set_count': 0}

        def add_set(ex_data=exercise_data, container=sets_container):
            i = ex_data['set_count']
            container.grid_columnconfigure(i, weight=1)

            set_box = tk.Frame(container, bg="#D0D0D0", bd=1, relief="solid")
            set_box.grid(row=0, column=i, sticky="nsew", padx=5)

            tk.Label(set_box, text=f"SET {i+1}", font=("Arial", 10, "bold"), bg="#D0D0D0").pack(pady=(5, 2))

            tk.Label(set_box, text="Reps", font=("Arial", 8), bg="#D0D0D0").pack()
            reps_entry = tk.Entry(set_box, width=6, justify='center', font=("Arial", 12))
            reps_entry.pack(pady=2)

            tk.Label(set_box, text="Kg/Lbs", font=("Arial", 8), bg="#D0D0D0").pack()
            weight_entry = tk.Entry(set_box, width=6, justify='center', font=("Arial", 12))
            weight_entry.pack(pady=(2, 10))

            ex_data['set_inputs'].append({'reps': reps_entry, 'weight': weight_entry})
            ex_data['set_count'] += 1

        # Start with one set shown
        add_set()

        # Add Set button for this exercise
        tk.Button(row_frame, text="+ Add Set", bg="green", fg="white", font=("Arial", 9, "bold"),
                  command=add_set).pack(pady=(5, 0))

        self.current_exercise_widgets.append(exercise_data)
        self.new_exercise_entry.delete(0, tk.END)

    # --- ADDED: Confirmation before going back from workout screen ---
    def confirm_back_from_workout(self):
        if self.current_exercise_widgets:
            if messagebox.askyesno("Go Back", "You have unsaved exercises. Are you sure you want to go back? Your workout will be lost."):
                self.clear_workout_screen()
                self.show_frame(self.dashboard_frame)
        else:
            self.show_frame(self.dashboard_frame)

#Loops through those saved widgets, grabs the text (.get()), converts them to integers/floats, and appends them to WORKOUT_FILE

    def save_workout(self):
        if not self.current_exercise_widgets: return
        today = datetime.now().strftime("%Y-%m-%d")
        data_to_save = []

        # --- ADDED: Confirmation before saving ---
        if not messagebox.askyesno("Save Workout", "Are you ready to save this workout?"):
            return

        for ex_item in self.current_exercise_widgets:
            name = ex_item['name']
            for i, inputs in enumerate(ex_item['set_inputs']):
                r_txt = inputs['reps'].get()
                w_txt = inputs['weight'].get()
                if r_txt and w_txt:
                    try:
                        # --- MODIFIED: Includes notes in saved data ---
                        notes = self.workout_notes_entry.get("1.0", tk.END).strip()
                        data_to_save.append([self.current_user, today, name, i+1, int(r_txt), float(w_txt), notes])
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid number in {name}")
                        return

        with open(WORKOUT_FILE, mode='a', newline='') as file:
            csv.writer(file).writerows(data_to_save)

        messagebox.showinfo("Success", "Workout Saved!")
        self.clear_workout_screen()
        self.show_frame(self.dashboard_frame)

#Uses .winfo_children().destroy() to delete the dynamically generated widgets from the screen after saving

    def clear_workout_screen(self):
        for widget in self.exercises_container.winfo_children():
            widget.destroy()
        self.current_exercise_widgets = []
        # --- ADDED: Clear notes box when workout is cleared ---
        self.workout_notes_entry.delete("1.0", tk.END)

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

                header = f"{'Date':<12} {'Exercise':<15} {'Set':<5} {'Reps':<5} {'Weight':<8} {'Notes':<20}\n"
                self.history_text.insert(tk.END, header + "-"*70 + "\n")

                for row in data[1:]:
                    if row and row[0] == self.current_user:
                        notes_col = row[6] if len(row) > 6 else ""
                        self.history_text.insert(tk.END,
                            f"{row[1]:<12} {row[2]:<15} {row[3]:<5} {row[4]:<5} {row[5]:<8} {notes_col:<20}\n")

        self.history_text.config(state=tk.DISABLED)
        self.show_frame(self.history_frame)

    # --- REPLACED: Analytics now has 3 tabs instead of 1 ---
    def setup_analytics_frame(self):
        top_bar = tk.Frame(self.analytics_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=10, padx=10)
        tk.Button(top_bar, text="Back", font=("Arial", 14),
                  command=lambda: self.show_frame(self.dashboard_frame)).pack(side=tk.LEFT)
        tk.Label(top_bar, text="Analytics", bg=BG_COLOR, fg="white", font=FONT_HEADER).pack(side=tk.LEFT, expand=True)

        # Tab buttons to switch between the 3 analytics views
        tab_row = tk.Frame(self.analytics_frame, bg=BG_COLOR)
        tab_row.pack(pady=(0, 10))
        for label, tab_id in [("1RM Progress", "1rm"), ("Volume Per Session", "volume"), ("Top Exercises", "top")]:
            tk.Button(tab_row, text=label, bg=BTN_COLOR, fg="white", font=("Arial", 11, "bold"),
                      relief="solid", bd=BTN_BORDER,
                      command=lambda t=tab_id: self.show_analytics_tab(t)).pack(side=tk.LEFT, padx=8)

        # Search row used by 1RM and Volume tabs
        ctrl_frame = tk.Frame(self.analytics_frame, bg=BG_COLOR)
        ctrl_frame.pack(pady=5)
        tk.Label(ctrl_frame, text="Exercise:", bg=BG_COLOR, font=FONT_BODY).pack(side=tk.LEFT)
        self.ana_entry = tk.Entry(ctrl_frame, font=FONT_BODY)
        self.ana_entry.pack(side=tk.LEFT, padx=10)
        tk.Button(ctrl_frame, text="Generate", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  relief="solid", bd=BTN_BORDER, command=self.generate_graph).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.analytics_frame, width=800, height=350, bg="white",
                                highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=10)
        self.stats_label = tk.Label(self.analytics_frame, text="", bg=BG_COLOR, font=("Times New Roman", 12, "bold"))
        self.stats_label.pack(pady=5)

        self.current_analytics_tab = "1rm"

    # Switches which tab is active and auto-generates Top Exercises (no search needed)
    def show_analytics_tab(self, tab):
        self.current_analytics_tab = tab
        self.canvas.delete("all")
        self.stats_label.config(text="")
        if tab == "top":
            self.generate_top_exercises()

    # Routes the Generate button to whichever tab is currently active
    def generate_graph(self):
        if self.current_analytics_tab == "1rm":
            self._graph_1rm()
        elif self.current_analytics_tab == "volume":
            self._graph_volume()

    # Tab 1: Estimated 1 Rep Max progress line graph
    def _graph_1rm(self):
        target_ex = self.ana_entry.get().strip()
        self.canvas.delete("all")
        if not target_ex or not os.path.exists(WORKOUT_FILE): return

        y_values = []
        with open(WORKOUT_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == self.current_user and row[2].lower() == target_ex.lower():
                    try:
                        e1rm = float(row[5]) * (1 + int(row[4]) / 30) #equation for 1 rep max
                        y_values.append(e1rm)
                    except ValueError:
                        continue

        if not y_values:
            self.canvas.create_text(400, 175, text="No data found for this exercise.", font=("Arial", 16))
            return

        self._draw_line_graph(y_values, "blue")
        self.stats_label.config(text=f"Latest 1RM: {int(y_values[-1])} kg  |  Best: {int(max(y_values))} kg")

    # Tab 2: Total volume (reps x weight) per date, grouped by day
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
            self.canvas.create_text(400, 175, text="No data found for this exercise.", font=("Arial", 16))
            return

        y_values = [daily[d] for d in sorted(daily)]
        self._draw_line_graph(y_values, "green")
        self.stats_label.config(text=f"Total sessions: {len(y_values)}  |  Best volume day: {int(max(y_values))} kg")

    # Tab 3: Bar chart of top 5 most-logged exercises for this user
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
            self.canvas.create_text(400, 175, text="No workout data yet.", font=("Arial", 16))
            return

        top = counts.most_common(5)
        w, h, margin = 800, 350, 50
        bar_width = 80
        max_val = top[0][1]
        spacing = (w - 2 * margin) // len(top)

        for i, (ex, count) in enumerate(top):
            x = margin + i * spacing + spacing // 2
            bar_h = int((count / max_val) * (h - 2 * margin))
            y_top = h - margin - bar_h
            self.canvas.create_rectangle(x - bar_width // 2, y_top, x + bar_width // 2, h - margin, fill=BTN_COLOR)
            self.canvas.create_text(x, y_top - 10, text=str(count), font=("Arial", 10, "bold"))
            self.canvas.create_text(x, h - margin + 15, text=ex[:10], font=("Arial", 9))

        self.stats_label.config(text=f"Your most-trained exercise: {top[0][0]}")

    # Shared line graph drawing used by both 1RM and Volume tabs
    def _draw_line_graph(self, y_values, color):
        w, h, margin = 800, 350, 50
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
            self.canvas.create_text(x, h - margin + 18, text=f"{i+1}", font=("Arial", 8))
            if prev_x is not None:
                self.canvas.create_line(prev_x, prev_y, x, y, fill=color, width=2)
            prev_x, prev_y = x, y

    # --- ADDED: Settings screen ---
    def setup_settings_frame(self):
        top_bar = tk.Frame(self.settings_frame, bg=BG_COLOR)
        top_bar.pack(fill="x", pady=10, padx=10)
        tk.Button(top_bar, text="Back", font=("Arial", 12), bg=BTN_COLOR, fg="white",
                  relief="solid", bd=BTN_BORDER,
                  command=lambda: self.show_frame(self.dashboard_frame)).pack(side=tk.LEFT)
        tk.Label(top_bar, text="SETTINGS", bg=BG_COLOR, fg="white", font=FONT_HEADER).pack(side=tk.LEFT, expand=True)

        content = tk.Frame(self.settings_frame, bg=BG_COLOR)
        content.pack(expand=True, pady=20)

        # Change Username section
        tk.Label(content, text="Change Username", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 2), sticky="w")
        tk.Label(content, text="New Username:", bg=BG_COLOR, fg="white", font=FONT_BODY).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.new_username_entry = tk.Entry(content, font=FONT_BODY, width=20, bg=BTN_COLOR, fg="white")
        self.new_username_entry.grid(row=1, column=1, pady=5)
        tk.Button(content, text="Update Username", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  relief="solid", bd=BTN_BORDER,
                  command=self.change_username).grid(row=2, column=0, columnspan=2, pady=5)

        # Change Password section
        tk.Label(content, text="Change Password", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 16, "bold")).grid(row=3, column=0, columnspan=2, pady=(20, 2), sticky="w")
        tk.Label(content, text="New Password:", bg=BG_COLOR, fg="white", font=FONT_BODY).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.new_password_entry = tk.Entry(content, show="*", font=FONT_BODY, width=20, bg=BTN_COLOR, fg="white")
        self.new_password_entry.grid(row=4, column=1, pady=5)
        tk.Button(content, text="Update Password", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  relief="solid", bd=BTN_BORDER,
                  command=self.change_password).grid(row=5, column=0, columnspan=2, pady=5)

        # Workout count section
        tk.Label(content, text="Account Info", bg=BG_COLOR, fg="white",
                 font=("Times New Roman", 16, "bold")).grid(row=6, column=0, columnspan=2, pady=(20, 2), sticky="w")
        tk.Button(content, text="View Workout Count", bg=BTN_COLOR, fg="white", font=("Arial", 10, "bold"),
                  relief="solid", bd=BTN_BORDER,
                  command=self.view_workout_count).grid(row=7, column=0, columnspan=2, pady=5)
        self.workout_count_label = tk.Label(content, text="", bg=BG_COLOR, fg="white", font=FONT_BODY)
        self.workout_count_label.grid(row=8, column=0, columnspan=2)

        # Delete account section
        tk.Button(content, text="DELETE ACCOUNT", bg="red", fg="white", font=("Arial", 11, "bold"),
                  relief="solid", bd=BTN_BORDER,
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
        with open(LOGIN_FILE, 'w', newline='') as f:
            for row in rows:
                if row and row[0] == self.current_user:
                    csv.writer(f).writerow([new_u, row[1]])
                else:
                    csv.writer(f).writerow(row)
        # Update username in workout data too
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
        if not (3 <= len(new_p) <= 12):
            messagebox.showerror("Error", "Password must be 3-12 characters.")
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
        rows = []
        with open(LOGIN_FILE, 'r') as f:
            rows = list(csv.reader(f))
        with open(LOGIN_FILE, 'w', newline='') as f:
            for row in rows:
                if row and row[0] != self.current_user:
                    csv.writer(f).writerow(row)
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


#simply runs the programme and everything definied in it
if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
