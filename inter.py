from tkinter import *
from ex2 import *

# Frame definition
frame_width = 450
frame_height = 250
frame_title = "Simple GUI for TAL"

# Sentence definition
text_label_header = "Please enter your request : "
text_button = "Search"
text_listbox_header = "10 firsts ID docs"

# Placement definition
x_label_header = 20
y_label_header = 20
x_entry_text = 200
y_entry_header = y_label_header
x_button_search = 350
y_button_search = y_label_header
x_listbox = 100
y_listbox = 50

# Color definition
button_fg_color = "green"


class Interface(Frame):
    """Our main frame
    All widgets used are stored as a field."""

    # Create the main frame
    def __init__(self, fenetre, **kwargs):
        # Initialize Frame
        Frame.__init__(self, fenetre, width=frame_width, height=frame_height, **kwargs)
        self.pack()
        
        # Label to help user (top)
        self.label_header = Label(self, text=text_label_header)
        self.label_header.place(x=x_label_header, y=y_label_header)
    
        # Text field for user entry
        self.text = Entry(self)
        self.text.place(x=x_entry_text, y=y_entry_header)

        # Button search
        self.button_search = Button(self, text=text_button, fg=button_fg_color, command=self.click)
        self.button_search.place(x=x_button_search, y=y_button_search)

        # Result (list)
        self.listbox = Listbox(self)
        self.listbox.place(x=x_listbox, y=y_listbox)
        self.listbox.insert(END, text_listbox_header)

        

    # Method called when user click on the search button
    def click(self):
        self.listbox.delete(0, END)
        self.listbox.insert(END, text_listbox_header)
        # Get the result from TP2
        docs = read_docs()
        index = build_index(docs)
        # Get the query from user entry
        query = self.text.get()
        ranking = rank_docs(index, query)
        for item in ranking[:10]:
            self.listbox.insert(END, item)
        


fenetre = Tk()
fenetre.title(frame_title)
interface = Interface(fenetre)

interface.mainloop()
