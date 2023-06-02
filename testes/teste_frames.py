from tkinter import *

def button_click(event, row, column):
    label = event.widget
    label.config(relief=SUNKEN)

def button_release(event, row, column):
    label = event.widget
    label.config(relief=RAISED)

def desabilita(label):
    label.configure(borderwidth=0)

root = Tk()

# Create a grid of labels
labels = []
for row in range(5):
    row_labels = []
    for column in range(5):
        label = Label(root, relief=RAISED, padx=20, pady=20)
        label.grid(row=row, column=column, padx=20, pady=20, sticky="nsew")
        label.bind("<Button-1>", lambda event, r=row, c=column: button_click(event, r, c))
        label.bind("<ButtonRelease-1>", lambda event, r=row, c=column: button_release(event, r, c))
        row_labels.append(label)
    labels.append(row_labels)

# Configure row and column weights to expand the label and make it occupy the entire space
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# labels[0][1].configure(borderwidth=0)
# desabilita(labels[1][1])
root.mainloop()
