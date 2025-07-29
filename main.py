import calendar
import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime, timedelta
import json
import os

# Variables that define colors for background, text, and buttons. Also, a degree symbol for weather
main_bg = "gray20"
main_fg = "white"
button_bg = "green3"
button_fg = "black"
degree_symbol = "\u00B0"

EVENTS_FILE = "events.json"
CONFIG_FILE = "config.json"

# Load existing events from file or initialize
if os.path.exists(EVENTS_FILE):
    with open(EVENTS_FILE, "r") as f:
        events = json.load(f)
else:
    events = {}

# We added a holiday cache that reduces lag in the app
holidays = {}
holiday_cache = {}

# Color themes for the main calendar window
color_themes = [
    {"bg": "black", "fg": "white"},
    {"bg": "white", "fg": "black"},
    {"bg": "navy", "fg": "yellow"},
    {"bg": "darkgreen", "fg": "lightgray"}
]
current_theme_index = 0

# Allows the user to save events in the log
def save_events():
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=4)

# API for preset holidays
def get_holidays(year):
    global holidays
    if year in holiday_cache:
        holidays = holiday_cache[year]
        return
    try:
        response = requests.get(f'https://date.nager.at/api/v3/publicholidays/{year}/US')
        data = response.json()
        holidays = {item['date']: item['localName'] for item in data}
        holiday_cache[year] = holidays
    except Exception as e:
        print(f"Error fetching holidays: {e}")
        holidays = {}

# Change the color of the main calendar window
def change_calendar_colors():
    global current_theme_index
    current_theme_index = (current_theme_index + 1) % len(color_themes)
    theme = color_themes[current_theme_index]
    text_widget.config(bg=theme["bg"], fg=theme["fg"])

# Yearly view in calendar window
def show_year():
    try:
        global current_year, current_month
        new_year = int(year_entry.get())
        if new_year > 0:
            current_year = new_year
            current_month = None
            get_holidays(current_year)
            calendar.setfirstweekday(calendar.SUNDAY)
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.config(width=65, height=36, font=("Courier", 12))
            cal = calendar.TextCalendar(firstweekday=calendar.SUNDAY)
            year_text = cal.formatyear(current_year, 2, 1, 1, 3)
            text_widget.insert(tk.END, year_text)
            text_widget.config(state=tk.DISABLED)
            root.title(f"Yearly Calendar - {current_year}")

        else:
            messagebox.showerror("Year Error", "Please enter a year greater than 0!")
    except ValueError:
        messagebox.showerror("Year Error:", "Please enter a numeric year!")

# Monthly view in calendar window
def show_month(year, month):
    global current_year, current_month
    current_year, current_month = year, month
    get_holidays(current_year)
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.config(width=20, height=10, font=("Courier", 38), padx=10)
    text_widget.insert(tk.END, calendar.month(current_year, current_month))
    update_event_list()
    highlight_event_days(current_year, current_month)
    text_widget.config(state=tk.DISABLED)
    root.title(f"Calendar for {calendar.month_name[current_month]} {current_year}")


# Navigation for previous/next month
def navigate_month(offset):
    global current_year, current_month
    if current_month is None or current_year is None:
        return

    new_month = current_month + offset
    new_year = current_year

    if new_month > 12:
        new_month = 1
        new_year += 1
    elif new_month < 1:
        new_month = 12
        new_year -= 1

    show_month(new_year, new_month)

# User entry for events
def add_event():
    event_name = event_name_entry.get().strip()
    event_date = event_date_entry.get().strip()
    event_time = event_time_entry.get().strip()
    event_description = event_description_entry.get("1.0", tk.END).strip()
    recurrence = recurrence_var.get()

    # Adds an error message for incorrect input
    if not event_name or not event_date or not event_time:
        messagebox.showwarning("Input Error", "Please enter event name, date, and time!")
        return

    # Adds an error message for incorrect format in date
    try:
        base_date = datetime.strptime(event_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Date Format Error", "Please enter the date in YYYY-MM-DD format!")
        return

    # Adds an error message for incorrect format in time
    try:
        datetime.strptime(event_time, "%I:%M %p")
    except ValueError:
        messagebox.showerror("Time Format Error", "Please enter the time in HH:MM AM/PM format!")
        return

    event_details = f"{event_name} at {event_time}\n{event_description}"

    def add_event_for_date(d):
        d_str = d.strftime("%Y-%m-%d")
        if d_str in events:
            events[d_str].append(event_details)
        else:
            events[d_str] = [event_details]

    # List for repeating events
    recurrence_map = {
        "None": 0,
        "Weekly": 7,
        "Biweekly": 14,
        "Monthly": 30,
        "6 Months": 182,
        "Yearly": 365
    }

    delta_days = recurrence_map.get(recurrence, 0)
    add_event_for_date(base_date)

    if delta_days > 0:
        next_date = base_date + timedelta(days=delta_days)
        limit_date = datetime(base_date.year + 2, 12, 31)  # Recurring events go up to 2 years
        while next_date <= limit_date:
            add_event_for_date(next_date)
            next_date += timedelta(days=delta_days)

    save_events()
    update_event_list()
    event_name_entry.delete(0, tk.END)
    event_date_entry.delete(0, tk.END)
    event_time_entry.delete(0, tk.END)
    event_description_entry.delete("1.0", tk.END)

# List box for saved events
def update_event_list():
    event_listbox.delete(0, tk.END)
    if not current_year or not current_month:
        return
    month_str = f"{current_year}-{str(current_month).zfill(2)}"

    for date, name in holidays.items():
        if month_str in date:
            event_listbox.insert(tk.END, f"{date}: [Holiday] {name}")

    for date, event_list in events.items():
        if month_str in date:
            for event in event_list:
                event_listbox.insert(tk.END, f"{date}: {event.splitlines()[0]}")

# Highlighting the events in the calendar
def highlight_event_days(year, month):
    days_with_user_events = set()
    for date_str in events:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            if dt.year == year and dt.month == month:
                days_with_user_events.add(dt.day)
        except ValueError:
            continue

    days_with_holidays = set()
    for date_str, name in holidays.items():
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            if dt.year == year and dt.month == month:
                days_with_holidays.add(dt.day)
        except ValueError:
            continue

    text_widget.tag_delete("user_event_day")
    text_widget.tag_delete("holiday_day")

# Changes the color in the calendar for User Events / Events from the API
    text_widget.tag_config("user_event_day", foreground="blue", font=("Courier", 38, "bold"))
    text_widget.tag_config("holiday_day", foreground="red", font=("Courier", 38, "bold"))

# Applies the User/Holiday events
    def apply_tag(day_set, tag_name):
        for day in day_set:
            day_str = f"{day:2}"
            start = "1.0"
            while True:
                pos = text_widget.search(day_str, start, stopindex=tk.END)
                if not pos:
                    break
                line, col = map(int, pos.split("."))
                before = text_widget.get(f"{line}.{col - 1}") if col > 0 else " "
                after = text_widget.get(f"{line}.{col + len(day_str)}")
                if before.isdigit() or after.isdigit():
                    start = f"{pos}+1c"
                    continue
                text_widget.tag_add(tag_name, pos, f"{pos}+{len(day_str)}c")
                start = f"{pos}+1c"

    apply_tag(days_with_user_events, "user_event_day")
    apply_tag(days_with_holidays, "holiday_day")

# Shows a popup box for Event Details
def view_event():
    try:
        selected_index = event_listbox.curselection()[0]
        selected_event = event_listbox.get(selected_index)
        selected_date = selected_event.split(":")[0]
        if selected_date in events:
            messagebox.showinfo("Event Details", "\n".join(events[selected_date]))
        else:
            messagebox.showinfo("Holiday Info", holidays.get(selected_date, "No details."))
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select an event to view.")

# Allows the user to delete selected event
def delete_event():
    try:
        selected_index = event_listbox.curselection()[0]
        selected_event = event_listbox.get(selected_index)
        selected_date, selected_info = selected_event.split(":", 1)
        selected_info = selected_info.strip()

        # Get event name and time to match across all dates
        event_key = selected_info.split(" at ")[0]
        event_time = selected_info.split(" at ")[1].split("\n")[0] if " at " in selected_info else None

        if not event_key or not event_time:
            raise ValueError("Event parsing failed")

        # Delete all matching recurring events
        to_delete = []
        for date, event_list in events.items():
            matching_events = [e for e in event_list if e.startswith(f"{event_key} at {event_time}")]
            for match in matching_events:
                event_list.remove(match)
            if not event_list:
                to_delete.append(date)

        for date in to_delete:
            del events[date]

        save_events()
        update_event_list()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select an event to delete.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete event: {e}")

# Weather API. Default city is Raleigh. Shows current weather conditions in selected city.
def update_weather(city="Raleigh"):
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=c2b4383ff668c2d6157da5a08bf233cf&units=imperial")
        data = response.json()
        if data.get("weather"):
            description = data["weather"][0]["description"]
            temp = round(data["main"]["temp"])
            city = data["name"]
            weather_label.config(text=f"{city}: {description}, {temp}{degree_symbol}F")
        else:
            weather_label.config(text="Weather data currently unavailable.")
    except Exception as e:
        weather_label.config(text=f"Error fetching weather: {e}")

# GUI Setup
root = tk.Tk()
root.title("Interactive Calendar")
root.geometry("1075x775")
root.configure(bg=main_bg)

# Centers the calendar in fullscreen mode
container = tk.Frame(root, bg=main_bg)
container.pack(expand=True, anchor="center")
calendar_frame = tk.Frame(container, bg=main_bg)
calendar_frame.grid(row=0, column=0, padx=5, pady=5)

# Initial format for the main calendar window, before "Change Calendar Colors" is selected
text_widget = tk.Text(calendar_frame, width=80, height=36, font=("Courier", 10), bg="black", fg="white")
text_widget.pack()

# Toolbar for the weather.
weather_label = tk.Label(calendar_frame, text="Loading Weather...", font=("Segoe UI", 18), bg=main_bg, fg=main_fg)
weather_label.pack(pady=10)
tk.Label(calendar_frame, text="Enter City:", font=("Segoe UI", 10), bg=main_bg, fg=main_fg).pack()
city_entry = tk.Entry(calendar_frame, font=("Segoe UI", 10), width=20)
city_entry.pack()
tk.Button(calendar_frame, text="Update Weather", bg=button_bg, fg=button_fg, command=lambda: update_weather(city_entry.get())).pack(pady=5)
root.after(100, update_weather)
control_frame = tk.Frame(container, bg=main_bg)
control_frame.grid(row=0, column=1, padx=20, pady=10)

# Labels for year selection
year_label = tk.Label(control_frame, text="Enter Year:", font=("Segoe UI", 14), bg=main_bg, fg=main_fg)
year_label.pack()
year_entry = tk.Entry(control_frame, font=("Segoe UI", 12))
year_entry.pack()
year_button = tk.Button(control_frame, text="Show Year", font=("Segoe UI", 10), command=show_year, bg=button_bg, fg=button_fg)
year_button.pack(pady=5)

month_buttons_frame = tk.Frame(control_frame, bg=main_bg)
month_buttons_frame.pack()

# Shows an error popup if a month is chosen before the year is selected
def handle_month_button(month):
    try:
        year = int(year_entry.get())
        show_month(year, month)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid year before selecting a month.")

for i, month_name in enumerate(calendar.month_name[1:], start=1):
    btn = tk.Button(month_buttons_frame, text=month_name, width=10,
                    command=lambda m=i: handle_month_button(m), bg=button_bg, fg=button_fg)
    btn.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)

# Button to change the calendar colors
color_button = tk.Button(control_frame, text="Change Calendar Colors", command=change_calendar_colors, bg=button_bg, fg=button_fg)
color_button.pack(pady=5)

# Buttons to cycle between Next/Previous month
nav_frame = tk.Frame(control_frame, bg=main_bg)
nav_frame.pack()
prev_button = tk.Button(nav_frame, text="<< Previous", command=lambda: navigate_month(-1), bg=button_bg, fg=button_fg)
prev_button.pack(side=tk.LEFT, padx=5)
next_button = tk.Button(nav_frame, text="Next >>", command=lambda: navigate_month(1), bg=button_bg, fg=button_fg)
next_button.pack(side=tk.RIGHT, padx=5)

# User entry for events
tk.Label(control_frame, bg=main_bg, fg=main_fg, text="Event Name:").pack(pady=2)
event_name_entry = tk.Entry(control_frame, width=40)
event_name_entry.pack(pady=2)
tk.Label(control_frame, bg=main_bg, fg=main_fg, text="Event Date (YYYY-MM-DD):").pack(pady=2)
event_date_entry = tk.Entry(control_frame, width=40)
event_date_entry.pack(pady=2)
tk.Label(control_frame, bg=main_bg, fg=main_fg, text="Event Time (HH:MM AM/PM):").pack(pady=2)
event_time_entry = tk.Entry(control_frame, width=40)
event_time_entry.pack(pady=2)
tk.Label(control_frame, bg=main_bg, fg=main_fg, text="Event Description:").pack(pady=2)
event_description_entry = tk.Text(control_frame, width=40, height=3, font=("Segoe UI", 8))
event_description_entry.pack(pady=2)

add_repeat_frame = tk.Frame(control_frame, bg=main_bg)
add_repeat_frame.pack(pady=5)

add_button = tk.Button(add_repeat_frame, text="Add Event", command=add_event, bg=button_bg, fg=button_fg)
add_button.pack(side=tk.LEFT, padx=(0, 10))

# Allows recurrence of events
recurrence_var = tk.StringVar(value="None")
repeat_menu = tk.OptionMenu(add_repeat_frame, recurrence_var, "None", "Weekly", "Biweekly", "Monthly", "6 Months", "Yearly")
repeat_menu.config(bg=button_bg, fg=button_fg, font=("Segoe UI", 10), highlightthickness=0)
repeat_menu["menu"].config(bg=button_bg, fg=button_fg, font=("Segoe UI", 10))
repeat_menu.pack(side=tk.LEFT)

# Shows the user-input events and the holidays from the API
tk.Label(control_frame, bg=main_bg, fg=main_fg, text="Events for the Month:").pack(pady=2)
event_listbox = tk.Listbox(control_frame, width=50, height=5)
event_listbox.pack(pady=5)
view_button = tk.Button(control_frame, text="View Event Details", command=view_event, bg=button_bg, fg=button_fg)
view_button.pack()
delete_button = tk.Button(control_frame, text="Delete Event", command=delete_event, bg=button_bg, fg=button_fg)
delete_button.pack(pady=5)

root.mainloop()
