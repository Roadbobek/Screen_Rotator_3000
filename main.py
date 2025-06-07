import rotatescreen
import time
import tkinter as tk

# tk button 1 event handler
def button_1():
    # Get the indices of selected items
    choice_indices = selection.curselection()

    # Get the actual text values
    choice = []
    for index in choice_indices:
        choice.append(selection.get(index))

    # turn choice into a list with just the monitors number as an int then subtract 1 to make it usable in python
    choices = []
    for iterator in choice:
        choices.append(int(iterator[0]) - 1)

    print(f"Choices: {choices}")
    print(screens)
    print(f"Choice: {choice}")
    print()


    # index = loop index
    # choices is our list of indexed screens, for example 0, 1, 2 ect
    # we loop through each screen in choices and assign it to index
    for index in choices:
        # we get item `index` (eg 0, 1, 2) from the screens list. eg `index` 0 = first item/monitor in list, item 0
        screen = screens[index]
        # get current screens orientation
        start_pos = screen.current_orientation
        print(f"Starting orientation: {start_pos}°")
        # now we do whatever we want to the current screen and then continue to the next
        print(index)
        print(screen.info)
        # For a clockwise rotation, we subtract 90° each time
        # This gives us: original → (original-90°) → (original-180°) → (original-270°) → original
        for i in range(0, 5):  # 0,1,2,3,4 for a complete rotation (5 positions)
            # Calculate the new position
            # The % 360 keeps it in the range 0-359
            pos = (start_pos - i*90) % 360
            print(f"Rotating to {pos}°")
            screen.rotate_to(pos)
            time.sleep(1)  # Pause between rotations

        print("Clockwise barrel roll complete!")


# get list of all screens
screens = rotatescreen.get_displays()

screens_list = []

# iterate through screens to get an index
# i = loop index 0, 1, 2, ect, starting on 0 so we add 1 to it for readability
for i, screen in enumerate(screens):
    screens_list.append(f"{i + 1}: {screen}")
print(f"Screens: {screens_list}")


# initiate main tk program loop
# The mainloop() method is used to run application once it is ready.
# It is an infinite loop that keeps the application running,waits for events to occur (such as button clicks) and processes these events as long as the window is not closed.

# create the main window
window = tk.Tk(screenName='easy screen flip', baseName='easy screen flip', className='easy screen flip', useTk=True, sync=False, use=None) #

frame = tk.Frame(borderwidth=64, bg='#373737') ##################

heading = tk.Label(master=frame, text='Select Monitor(s)', background='#4D4D4D', width=27, height=1)
heading.pack()

selection = tk.Listbox(master=frame, activestyle='dotbox', bg='#4D4D4D', width=31, height=10, selectmode=tk.MULTIPLE)
for item in screens_list:
    selection.insert(tk.END, item)
selection.pack()

# button 1
button = tk.Button(master=frame, text='Consecutive Barrel Role', command=button_1, bg='#4D4D4D', width=27, height=2)
button.pack()

frame.pack() ##################

# Change the background color using configure
window.configure(bg='#373737')

# Run the application
window.mainloop() #
