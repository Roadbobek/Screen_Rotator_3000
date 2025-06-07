import rotatescreen
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkinter import messagebox # For showing info/error dialogs

# Global variable for the spinbox so button handlers can access it
roll_spinbox = None
screens = [] # Will be populated later

# tk button 1 event handler (Consecutive Rolls)
def button_1_consecutive_roll():
    global roll_spinbox, screens
    if not screens:
        messagebox.showinfo("No Screens", "No screens detected.")
        return

    choice_indices = selection.curselection()
    if not choice_indices:
        messagebox.showinfo("No Selection", "Please select one or more monitors.")
        return

    num_rolls = 0
    try:
        num_rolls = int(roll_spinbox.get())
        if num_rolls <= 0:
            messagebox.showerror("Invalid Input", "Number of rolls must be a positive integer.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for rolls.")
        return

    choices_indices_for_screens = []
    for index in choice_indices:
        item_text = selection.get(index)
        try:
            monitor_number_str = item_text.split(":")[0]
            screen_idx = int(monitor_number_str) - 1
            if 0 <= screen_idx < len(screens):
                choices_indices_for_screens.append(screen_idx)
            else:
                print(f"Warning: Invalid screen index {screen_idx} parsed from '{item_text}' (out of range).")
        except ValueError:
            print(f"Warning: Could not parse monitor number from '{item_text}'.")

    if not choices_indices_for_screens:
        messagebox.showinfo("No Valid Selection", "No valid monitors were selected or parsed correctly.")
        return

    print(f"Selected monitor indices for consecutive roll (0-based): {choices_indices_for_screens}")

    for screen_idx in choices_indices_for_screens:
        screen = screens[screen_idx]
        start_pos = screen.current_orientation
        print(f"\nScreen {screen_idx + 1} - Starting {num_rolls} consecutive barrel roll(s)...")
        print(f"Screen {screen_idx + 1} - Initial orientation: {start_pos}°")

        # Perform num_rolls * 4 rotation commands
        for i in range(num_rolls * 4):
            # The target position is always relative to the initial start_pos for this screen's operation
            pos = (start_pos - (i + 1) * 90) % 360
            current_roll_for_print = (i // 4) + 1
            step_in_roll_for_print = (i % 4) + 1
            print(f"Screen {screen_idx + 1} - Roll {current_roll_for_print}/{num_rolls}, Step {step_in_roll_for_print}/4: Rotating to {pos}°")
            try:
                screen.rotate_to(pos)
                window.update() # Update GUI to prevent freezing during sleep
                time.sleep(1)  # Pause between rotations
            except Exception as e:
                print(f"Error rotating screen {screen_idx + 1} to {pos}°: {e}")
                messagebox.showerror("Rotation Error", f"Error rotating screen {screen_idx + 1}:\n{e}")
                break # Stop trying to rotate this screen if an error occurs

        print(f"Screen {screen_idx + 1} - {num_rolls} consecutive barrel roll(s) complete!")
    print("-" * 30)
    messagebox.showinfo("Complete", "Consecutive barrel roll(s) finished.")

# tk button 2 event handler (Simultaneous Rolls)
def button_2_simultaneous_roll():
    global roll_spinbox, screens
    if not screens:
        messagebox.showinfo("No Screens", "No screens detected.")
        return

    choice_indices = selection.curselection()
    if not choice_indices:
        messagebox.showinfo("No Selection", "Please select one or more monitors for simultaneous roll.")
        return

    num_rolls = 0
    try:
        num_rolls = int(roll_spinbox.get())
        if num_rolls <= 0:
            messagebox.showerror("Invalid Input", "Number of rolls must be a positive integer.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for rolls.")
        return

    selected_screens_data = []
    for index in choice_indices:
        item_text = selection.get(index)
        try:
            monitor_number_str = item_text.split(":")[0]
            screen_idx = int(monitor_number_str) - 1
            if 0 <= screen_idx < len(screens):
                selected_screens_data.append({
                    'screen_obj': screens[screen_idx],
                    'original_start_pos': screens[screen_idx].current_orientation,
                    'id': screen_idx + 1, # For printing
                    'name': item_text # For error messages
                })
            else:
                print(f"Warning: Invalid screen index {screen_idx} parsed from '{item_text}' (out of range).")
        except ValueError:
            print(f"Warning: Could not parse monitor number from '{item_text}'.")

    if not selected_screens_data:
        messagebox.showinfo("No Valid Selection", "No valid monitors could be processed for simultaneous roll.")
        return

    print(f"\nStarting {num_rolls} simultaneous barrel roll(s) for {len(selected_screens_data)} monitor(s)...")

    # Total 90-degree steps for the entire operation
    total_rotation_steps = num_rolls * 4

    for step_count in range(total_rotation_steps): # step_count from 0 to (num_rolls*4 - 1)
        current_roll_num_for_print = (step_count // 4) + 1
        step_in_roll_for_print = (step_count % 4) + 1
        print(f"\n--- Simultaneous Roll {current_roll_num_for_print}/{num_rolls}, Overall Step {step_in_roll_for_print}/4 ---")

        active_rotations_this_step = 0
        for screen_data in selected_screens_data:
            screen = screen_data['screen_obj']
            original_start_pos = screen_data['original_start_pos']
            screen_id_for_print = screen_data['id']
            screen_name_for_print = screen_data['name']

            # Calculate the target orientation for this screen at this step
            pos = (original_start_pos - (step_count + 1) * 90) % 360

            print(f"Screen {screen_id_for_print} ({screen_name_for_print}) - Rotating to {pos}°")
            try:
                screen.rotate_to(pos)
                active_rotations_this_step += 1
            except Exception as e:
                error_msg = f"Error rotating screen {screen_id_for_print} ({screen_name_for_print}): {e}"
                print(error_msg)
                # Remove screen from further attempts in this simultaneous roll
                selected_screens_data.remove(screen_data)
                messagebox.showwarning("Rotation Error", error_msg + "\nThis screen will be skipped for remaining steps.")


        if not selected_screens_data: # All screens failed
            print("All selected screens encountered errors. Stopping simultaneous roll.")
            messagebox.showerror("Simultaneous Roll Failed", "All selected screens encountered errors during rotation.")
            return

        if active_rotations_this_step > 0: # Only sleep if at least one screen rotated
            window.update() # Update GUI
            time.sleep(1) # Pause after all selected screens have made one 90-degree turn
        else: # No screens rotated in this step, likely all failed previously
            print("No screens successfully rotated in this step.")


    print()
    print("-" * 90)
    print(f"{num_rolls} simultaneous barrel roll(s) attempt complete for selected monitors!")
    print("-" * 90)
    messagebox.showinfo("Complete", "Simultaneous barrel roll(s) finished.")


# --- Main Application Setup ---
def setup_gui():
    global selection, roll_spinbox, screens, window # Declare globals we define/use here

    # get list of all screens
    try:
        screens = rotatescreen.get_displays()
    except Exception as e:
        print(f"Error getting display information: {e}")
        messagebox.showerror("Display Error", f"Could not retrieve display information: {e}\nThe application might not function correctly.")
        screens = []


    screens_list_for_display = []
    if screens:
        for i, screen_obj in enumerate(screens):
            screen_name = getattr(screen_obj, 'name', f"Display {i + 1}")
            if isinstance(screen_name, bytes):
                try:
                    screen_name = screen_name.decode()
                except UnicodeDecodeError:
                    screen_name = f"Display {i + 1} (undecodable name)"
            screens_list_for_display.append(f"{i + 1}: {screen_name}")
    else:
        screens_list_for_display.append("No screens detected.")

    # --- GUI Setup ---
    window = tk.Tk()
    window.title("Screen Rotator 3000 Extreme")
    window.minsize(400, 550) # Adjusted minsize for new controls

    # --- Styling ---
    style = ttk.Style(window)
    available_themes = style.theme_names()
    preferred_themes = ['clam', 'alt', 'vista', 'default']
    chosen_theme = None
    for theme in preferred_themes:
        if theme in available_themes:
            try:
                style.theme_use(theme)
                chosen_theme = theme
                break
            except tk.TclError:
                continue
    if not chosen_theme:
        print("No preferred modern themes available or loadable. Using system default.")

    try:
        heading_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        default_font = tkFont.Font(family="Segoe UI", size=11)
        button_font = tkFont.Font(family="Segoe UI", size=12, weight="bold")
    except tk.TclError:
        try:
            heading_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
            default_font = tkFont.Font(family="Helvetica", size=11)
            button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        except tk.TclError:
            heading_font = tkFont.Font(family="Arial", size=16, weight="bold")
            default_font = tkFont.Font(family="Arial", size=11)
            button_font = tkFont.Font(family="Arial", size=12, weight="bold")

    window_bg_color = '#2E2E2E'
    content_bg_color = '#373737'
    widget_bg_color = '#4D4D4D'
    text_color = 'white'
    select_bg_color = '#0078D7'

    window.configure(bg=window_bg_color)

    content_frame = ttk.Frame(window, padding="20 20 20 20", style='Content.TFrame')
    style.configure('Content.TFrame', background=content_bg_color)
    content_frame.pack(fill=tk.BOTH, expand=True)

    style.configure('Header.TLabel', background=widget_bg_color, foreground=text_color, font=heading_font, padding=(10, 10, 10, 10), anchor='center')
    heading = ttk.Label(master=content_frame, text='Select Monitor(s)', style='Header.TLabel')
    heading.pack(fill=tk.X, pady=(0, 15))

    selection = tk.Listbox(master=content_frame, activestyle='dotbox', bg=widget_bg_color, fg=text_color,
                           selectbackground=select_bg_color, selectforeground=text_color, font=default_font,
                           relief='flat', borderwidth=1, highlightthickness=1, highlightbackground='#555555',
                           highlightcolor=select_bg_color, selectmode=tk.MULTIPLE, exportselection=False)
    for item in screens_list_for_display:
        selection.insert(tk.END, item)
    if not screens: # Disable listbox if no screens
        selection.config(state=tk.DISABLED)
    selection.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

    # --- Roll Controls Frame ---
    roll_control_frame = ttk.Frame(content_frame, style='Content.TFrame')
    roll_control_frame.pack(fill=tk.X, pady=(5, 10))

    roll_label_style_name = 'RollLabel.TLabel'
    style.configure(roll_label_style_name, background=content_bg_color, foreground=text_color, font=default_font)
    roll_label = ttk.Label(roll_control_frame, text="Number of Rolls (1-100):", style=roll_label_style_name)
    roll_label.pack(side=tk.LEFT, padx=(0, 10))

    roll_spinbox_var = tk.StringVar(value="1")
    # Note: ttk.Spinbox styling is heavily theme-dependent.
    # For more control, you might need to explore specific theme options or use tk.Spinbox and style it.
    roll_spinbox = ttk.Spinbox(
        roll_control_frame, from_=1, to=100, textvariable=roll_spinbox_var, width=5, font=default_font,
        state='readonly' # Makes it behave more like a dropdown for selection, prevents arbitrary text
    )
    # Attempt to style ttk.Spinbox (may have limited effect depending on theme)
    style.configure('TSpinbox', arrowsize=15) # General spinbox style
    style.map('TSpinbox',
              fieldbackground=[('readonly', widget_bg_color), ('!disabled', widget_bg_color)],
              foreground=[('readonly', text_color), ('!disabled', text_color)],
              selectbackground=[('readonly', widget_bg_color)], # Color of text area when selected
              selectforeground=[('readonly', text_color)]
              )
    if not screens: # Disable spinbox if no screens
        roll_spinbox.config(state=tk.DISABLED)
    roll_spinbox.pack(side=tk.LEFT)


    # --- Buttons ---
    button_frame = ttk.Frame(content_frame, style='Content.TFrame')
    button_frame.pack(fill=tk.X, pady=(10,0))


    style.configure('App.TButton', font=button_font, padding=(10, 8, 10, 8))
    style.map('App.TButton',
              background=[('active', '#606060'), ('!disabled', widget_bg_color), ('disabled', '#404040')],
              foreground=[('active', text_color), ('!disabled', text_color), ('disabled', '#888888')])

    button1 = ttk.Button(button_frame, text='Consecutive Barrel Roll (Per Screen)', command=button_1_consecutive_roll, style='App.TButton')
    button1.pack(fill=tk.X, ipady=5, pady=(0,5))

    button2 = ttk.Button(button_frame, text='Simultaneous Barrel Roll (All Selected)', command=button_2_simultaneous_roll, style='App.TButton')
    button2.pack(fill=tk.X, ipady=5)

    if not screens: # Disable buttons if no screens
        button1.config(state=tk.DISABLED)
        button2.config(state=tk.DISABLED)


    window.mainloop()

if __name__ == "__main__":
    setup_gui()
