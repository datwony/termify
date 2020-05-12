
try:
    import tkinter as tk        # python v3
except:
    import Tkinter as tk        # python v2

# This function is called when the submit button is clicked
def submit_callback(input_entry):
    print("User entered : " + input_entry.get())
    return None


#######################  GUI ###########################
root = tk.Tk()
root.geometry('600x350')       #Set window size

# Heading
heading = tk.Label(root, text="Termify")
heading.config(font=("Courier", 44))

heading.place(x = 175, y = 0)


input_label = tk.Label(root, text="Enter your email to receive \nyour weekly vocabulary digest!")
input_label.config(font=("Courier", 15))
input_label.place(x = 115, y = 80)

input_entry = tk.Entry(root, width = "70")
input_entry.place(x = 95, y = 160)


submit_button = tk.Button(root, text = "Submit", command = lambda: submit_callback(input_entry))
submit_button.place(x = 260, y = 200)
root.mainloop()
