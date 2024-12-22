from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

####################[Edit DBMS]###################################################################################

def RetriveData(Name):
    db = []
    with open(f"Data/{Name}.txt", "r") as f:
        for line in f:
            db.append(line.strip().split(","))
    #Strip all Elements
    for i in range(len(db)):
        db[i] = [element.strip() for element in db[i]]
    return db

def Clear_QueryBox(QueryBox):
    QueryBox.config(state="normal")

    if (QueryBox.get("1.0",END)).strip() != "":
        QueryBox.delete("1.0", END)

    QueryBox.config(state="disabled")

def Searching(Selection,QueryBox,Searchwin):

    QueryBox.config(state="normal")
    if QueryBox.get("1.0",END).strip() == "":
        QueryBox.config(state="disabled")
        return

    QueryBox.config(state="normal")
    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    # Widths = db[0][1::2]
    # Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    Query = QueryBox.get("1.0",END)

    for field in Fields[2::2]:
        count = (Query.strip()).count(field)
        if count > 1:
            messagebox.showwarning("Warning", "Use Comma (,) to Serach for Multiple Entries in a Field")
            Searchwin.lift()
            return

    Query = Query.strip().split(";")

    for Q in Query:
        list = Q.split(',')
        search = []
        field = list[0]  # str
        Entries = list[1:]  # list

        FieldIndex = Fields.index(field)

        serials = []
        for i in range(1, len(db)):
            serials.append(i)  # jitne serials utni entries check hongi

        for item in Entries:
            # print(item)
            for serial in serials:
                if item == db[int(serial)][int(FieldIndex / 2)]:
                    search.append(db[int(serial)])
        # print(search)
        db = search
        db.insert(0, Fields)
    # print(db)
    Searchwin.destroy()
    Display(db)

def Search_AddQuery(SearchField,SearchEntry,QueryBox):

    QueryBox.config(state="normal")
    SearchField = SearchField.get()
    Search  = SearchEntry.get().strip()
    CurrentQuery = QueryBox.get("1.0",END)
    if Search:
        if CurrentQuery.strip() == "": #if empty then print without ";"
            QueryBox.insert(END, f"{SearchField},{Search}")
        else: #Otherwise Print with ";"
            QueryBox.insert(END, f";{SearchField},{Search}")

    QueryBox.config(state="disabled")
    SearchEntry.delete(0,END)

def Edit_Search(Selection):
    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    Searchwin = Toplevel()
    Searchwin.title("Search Module")
    Searchwin.geometry("825x250+200+250")
    Searchwin.resizable(False, False)

    S_l1 = Label(Searchwin, text="Search in:")
    S_l1.grid(row=0, column=0, padx=5, pady=5)
    S_l2 = Label(Searchwin, text="Enter Search:")
    S_l2.grid(row=0, column=1, padx=5, pady=5)
    S_l3 = Label(Searchwin, text="Add to Query")
    S_l3.grid(row=0, column=2, padx=5, pady=5)

    # FieldSelector
    SearchField = StringVar()
    SearchField.set(FieldNames[0])
    SearchSelector = OptionMenu(Searchwin, SearchField, *FieldNames)
    SearchSelector.grid(row=1, column=0, padx=5, pady=5)

    SearchEntry = Entry(Searchwin, width=60)
    SearchEntry.grid(row=1, column=1, padx=5, pady=5)

    # Add Button
    AddButton = Button(Searchwin, text="Add", width=20 ,command=lambda :Search_AddQuery(SearchField,SearchEntry,QueryBox))
    AddButton.grid(row=1, column=2, padx=5, pady=5)

    # Query Box
    QueryLable =Label(Searchwin, text="Query box:")
    QueryLable.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

    QueryBox = Text(Searchwin, height=5, width=80, wrap=WORD,bd=5)
    QueryBox.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
    QueryBox.config(state="disabled")

    SearchButton = Button(Searchwin,text="Search",width=10,command=lambda: Searching(Selection,QueryBox,Searchwin))
    SearchButton.grid(row=3, column=2, padx=5, pady=5)

    ClearQuery = Button(Searchwin,text="Clear Query Box",width=20,command=lambda :Clear_QueryBox(QueryBox))
    ClearQuery.grid(row=3, column=1, padx=5, pady=5)

    Note = Label(Searchwin, text="Note: To Search Multiple \n Values in Same Field use ','\nRoll No.,12,34,42\nIn-Entry:12,34,42 ")
    Note.grid(row=3, column=0, padx=5, pady=5)

    Searchwin.mainloop()

def Edit_DeleteField2(Selection, delete_window, deleteField):
    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    deleteField = deleteField.get()

    deleteSerial = Fields.index(deleteField)
    Fields.pop(deleteSerial) #deletes Field Name
    Fields.pop(deleteSerial) #Deletes Field Length

    #Deleting Entry of that field from all Entries
    for  serial in serials:
        db[int(serial)].pop(int(deleteSerial/2))

    db[0] = Fields
    WrtieToFile(db,Name)

    delete_window.destroy()
    messagebox.showinfo(title='Update', message='Field Deleted Successfully')

def Edit_DeleteField(Selection):

    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    delete_window = Toplevel()
    delete_window.title("Edit Field")
    delete_window.resizable(False, False)
    delete_window.geometry("400x250+500+260")
    deleteFrame = Frame(delete_window, width=300, height=200, relief="ridge", bg="lightyellow", bd=5)
    deleteFrame.pack(pady=10)

    deleteLable = Label(delete_window, text="Select Field You want to Delete.", bg="lightyellow", font=(12))
    deleteLable.place(x=100, y=30)
    # Setting OptionList
    deleteField = StringVar()
    deleteField.set(FieldNames[0])
    deleteOptions = OptionMenu(deleteFrame, deleteField, *FieldNames)
    deleteOptions.config(width=20, height=2)
    deleteOptions.place(x=65, y=50)
    b4 = Button(deleteFrame, text="Delete", width=12, height=1,
                command=lambda: Edit_DeleteField2(Selection, delete_window, deleteField))
    b4.place(x=100, y=100)

def KeepEntries(win,Name,x,y,EditSerial):
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])

    Fields[EditSerial] = x
    Fields[EditSerial + 1] = y

    db[0] = Fields
    WrtieToFile(db, Name)
    win.destroy()
    messagebox.showinfo(title='Update', message='Field Edited Successfully!')

def Edit_EditField4(win, Name, serials, Entries, Fields, Widths, EF_Entry, y, EF_l, db,EditSerial,x):

    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    length = int(y)
    EF_list = []
    for entry, serial in zip(Entries, serials):
        value = entry.get()
        if len(value) > length:
            EF_l.config(text=f"Entry of S-No: {serial}\nShould be With-in Specified length: {length}")
            return
        EF_list.append(value)

    for item ,serial in zip(EF_list, serials):
        db[int(serial)][int(EditSerial/2)] = item
    Fields[EditSerial] = x
    Fields[EditSerial+1] = y

    db[0] = Fields
    WrtieToFile(db,Name)
    win.destroy()
    messagebox.showinfo(title='Update', message='Field Edited Successfully!')

def Edit_EditField3(Selection,win,db,EF_Entry,EF_lenghtEntry,EF_l,Name,EditSerial):

    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    # EF = Add Field

    x = EF_Entry.get()
    y = EF_lenghtEntry.get()
    if x == "" or y == "":
        messagebox.showerror("Error", "Please Fill 'All' Above Data")
        win.lift()
    elif not (y.isdigit()) or y == "0":
        messagebox.showerror("Error", "Length of Field should be Numeric and Can't be 0")
        win.lift()
    elif int(y) < 0:
        messagebox.showerror("Error", "Length of Field Should be Positive")
        win.lift()
    elif len(x) > int(y):
        messagebox.showerror("Error", "Length of Field should be Greater than Field Name")
        win.lift()

    else:
        win.destroy()
        Fields.append(x)  # Append New Field Name
        Fields.append(y)  # Append New Field Length
        Widths.append(int(y))  # Append length

        win = Tk()
        win.title("Editing Field")
        CanvasWidth = 450
        CanvasHeight = 400
        win.geometry(f"{CanvasWidth}x{CanvasHeight}+400+180")
        win.resizable(False, False)

        # Scroll Bar
        scroll = Scrollbar(win, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        # Setting it to Control OUR Canvas
        canvas = Canvas(win, width=CanvasWidth, height=CanvasHeight, yscrollcommand=scroll.set)
        canvas.pack()
        scroll.config(command=canvas.yview)

        # Frame to Put Entries
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=NW)

        #To keep All Entries Same
        KeepButton = Button(frame, text="Finish", width=20, height=2,
                    command=lambda: KeepEntries(win,Name,x,y,EditSerial))
        KeepButton.grid(row=0, column=1, padx=10, pady=10)

        KeepLable = Label(frame, text=f"Press To Keep All Previous Entries")
        KeepLable.grid(row=0, column=0, padx=10, pady=10)
        # Entries Layout
        Entries = []
        for r, serial in zip(range(len(serials)), serials):
            label = Label(frame, text=f"Enter Data For S-No: '{serial}': ")
            entry = Entry(frame, width=30)
            label.grid(row=r+1, column=0, padx=10, pady=10)
            entry.grid(row=r+1, column=1, padx=10, pady=10)
            Entries.append(entry)  # create a list of all entry Widget data~~!

        b2 = Button(frame, text="Edit Field", width=20, height=2,
                    command=lambda: Edit_EditField4(win, Name, serials, Entries, Fields, Widths, EF_Entry, y, EF_l, db,EditSerial,x))
        b2.grid(row=r + 2, column=1, padx=10, pady=10)

        l1 = Label(frame, text=f"Please Fill Above Data to Add Entries\nin Field: {x}")
        l1.grid(row=r + 2, column=0, padx=10, pady=10)

        # Update scrollable area
        frame.update_idletasks()  # Ensure the frame has been updated before getting the bounding box
        canvas.config(scrollregion=canvas.bbox("all"))

        # using tab to move Scroll bar
        win.bind("<Tab>", lambda event: canvas.yview_scroll(1, "units"))

        win.mainloop()

def Edit_EditField2(Selection,edit_window,EditField):
    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    EditSerial = Fields.index(EditField.get())
    win = Tk()
    win.title("Edit Field")
    win.geometry("400x170+450+270")
    win.resizable(False, False)

    # EF = EditField
    EF_Lable = Label(win, text=f"Enter Name Of Field")
    EF_Lable.pack()
    EF_Entry = Entry(win, width=20)
    EF_Entry.pack()

    EF_lenghtLable = Label(win, text=f"Enter Length Of Field")
    EF_lenghtLable.pack()
    EF_lenghtEntry = Entry(win, width=20)
    EF_lenghtEntry.pack()

    EF_l = Label(win, text="Please Fill Above Entries")
    EF_l.pack(pady=10)

    EF_b = Button(win, text="Edit", width=10,
                  command=lambda: Edit_EditField3(Selection,win,db,EF_Entry,EF_lenghtEntry,EF_l,Name,EditSerial))
    EF_b.pack()

    edit_window.destroy()

def Edit_EditField(Selection):

    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    edit_window = Toplevel()
    edit_window.title("Edit Field")
    edit_window.resizable(False, False)
    edit_window.geometry("400x250+500+260")
    EditFrame = Frame(edit_window,width=300,height=200,relief="ridge",bg="lightyellow",bd=5)
    EditFrame.pack(pady=10)

    EditLable = Label(edit_window, text="Select Field You want to Edit.", bg="lightyellow",font=(12))
    EditLable.place(x=100, y=30)
    #Setting OptionList
    EditField = StringVar()
    EditField.set(FieldNames[0])
    editOptions = OptionMenu(EditFrame, EditField, *FieldNames)
    editOptions.config(width=20, height=2)
    editOptions.place(x=65, y=50)
    b4 = Button(EditFrame, text="Confirm", width=12, height=1,
                command=lambda:Edit_EditField2(Selection,edit_window,EditField))
    b4.place(x=100, y=100)


def Edit_AddField3(win,Name,serials,Entries,Fields,Widths,AF_Entry,y,AF_l,db):

    length = int(y)
    AF_list = []
    for entry,serial in zip(Entries,serials):
        value = entry.get()
        if len(value) > length:
            AF_l.config(text=f"Entry of S-No: {serial}\nShould be With-in Specified length: {length}")
            return
        AF_list.append(value)


    for item,serial in zip(AF_list,serials):
        db[int(serial)].append(item)

    db[0] = Fields
    WrtieToFile(db,Name)
    win.destroy()
    messagebox.showinfo("Update","New Field Added Successfully")

def Edit_AddField2(win,db,AF_Entry,AF_lenghtEntry,AF_l,Name):

    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    #AF = Add Field

    x = AF_Entry.get()
    y = AF_lenghtEntry.get()
    if x == "" or y == "":
        messagebox.showerror("Error", "Please Fill 'All' Above Data")
        win.lift()
    elif not (y.isdigit()) or y == "0":
        messagebox.showerror("Error", "Length of Field should be Numeric and Can't be 0")
        win.lift()
    elif int(y) < 0:
        messagebox.showerror("Error", "Length of Field Should be Positive")
        win.lift()
    elif len(x) > int(y):
        messagebox.showerror("Error", "Length of Field should be Greater than Field Name")
        win.lift()

    else:
        win.destroy()
        Fields.append(x) #Append New Field Name
        Fields.append(y) #Append New Field Length
        Widths.append(int(y)) #Append length

        win = Tk()
        win.title("Adding Field")
        CanvasWidth = 450
        CanvasHeight = 400
        win.geometry(f"{CanvasWidth}x{CanvasHeight}+400+180")
        win.resizable(False, False)

        # Scroll Bar
        scroll = Scrollbar(win, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        # Setting it to Control OUR Canvas
        canvas = Canvas(win, width=CanvasWidth, height=CanvasHeight, yscrollcommand=scroll.set)
        canvas.pack()
        scroll.config(command=canvas.yview)

        # Frame to Put Entries
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=NW)

        # Entries Layout
        Entries = []
        for r,serial in zip(range(len(serials)),serials):
            label = Label(frame, text=f"Enter Data For S-No: '{serial}': ")
            entry = Entry(frame, width=30)
            label.grid(row=r, column=0, padx=10, pady=10)
            entry.grid(row=r, column=1, padx=10, pady=10)
            Entries.append(entry)  # create a list of all entry Widget data~~!

        b2 = Button(frame, text="Add Field", width=20, height=2, command=lambda:Edit_AddField3(win,Name,serials,Entries,Fields,Widths,AF_Entry,y,AF_l,db))
        b2.grid(row=r + 1, column=1, padx=10, pady=10)

        l1 = Label(frame, text=f"Please Fill Above Data to Add Entries\nin Field: {x}")
        l1.grid(row=r + 1, column=0, padx=10, pady=10)

        # Update scrollable area
        frame.update_idletasks()  # Ensure the frame has been updated before getting the bounding box
        canvas.config(scrollregion=canvas.bbox("all"))

        #using tab to move Scroll bar
        win.bind("<Tab>", lambda event: canvas.yview_scroll(1, "units"))

        win.mainloop()


def Edit_AddField(Selection):

    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    win = Tk()
    win.title("Add Field")
    win.geometry("400x170+400+250")
    win.resizable(False, False)

    # AF = AddField
    AF_Lable = Label(win, text=f"Enter Name Of Field")
    AF_Lable.pack()
    AF_Entry = Entry(win, width=20)
    AF_Entry.pack()

    AF_lenghtLable = Label(win, text=f"Enter Length Of Field")
    AF_lenghtLable.pack()
    AF_lenghtEntry = Entry(win, width=20)
    AF_lenghtEntry.pack()

    AF_l = Label(win, text="Please Fill Above Entries")
    AF_l.pack(pady=10)

    AF_b = Button(win, text="Add",width=10,command=lambda :Edit_AddField2(win,db,AF_Entry,AF_lenghtEntry,AF_l,Name))
    AF_b.pack()


def Edit_DeleteEntry2(serials,Delete_SerialEntry,db,Name,Delete_win):
    DeleteSerial = Delete_SerialEntry.get()
    Delete_SerialEntry.delete(0, END)

    if (DeleteSerial == "") or (DeleteSerial not in serials) or (DeleteSerial == "0"):
        messagebox.showerror("Error", "Please Enter a Valid Serial Number.")
        Delete_win.lift()
    elif int(DeleteSerial) <= 0:
        messagebox.showerror("Error", "Please Enter a Valid Serial Number.")
        Delete_win.lift()
    else:
        Delete_win.destroy()
        DeleteSerial = int(DeleteSerial)
        db.pop(DeleteSerial)

        serials = serials[:-1]

        for serial in serials:
            db[int(serial)][0] = serial

        WrtieToFile(db,Name)
        messagebox.showinfo("Success", "Entry Successfully Deleted.")

def Edit_DeleteEntry(Selection):

    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials
    # print(serials)
    Delete_win = Tk()
    Delete_win.title("Edit Entry")
    Delete_win.geometry("400x150+550+330")
    Delete_win.resizable(False, False)

    Delete_lable = Label(Delete_win, text=f"Enter Serial No. of Entry You want to Delete, Max Serial: {serials[-1]}")
    Delete_lable.pack(pady=10)

    Delete_SerialEntry = Entry(Delete_win)
    Delete_SerialEntry.pack(pady=10)

    Delete_Button = Button(Delete_win, text="Delete", font=("Bold"), width=15,command=lambda: Edit_DeleteEntry2(serials,Delete_SerialEntry,db,Name,Delete_win))
    Delete_Button.pack(pady=10)

    Delete_win.mainloop()

def Edit_EditEntry2(db, Entries, Widths, Fields, l1, i, Name,Edit_SerialEntry):
    # Basic Data:
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    serials = []
    for i in range(1, len(db)):
        serials.append(db[i][0])  # creates a list of all Serials

    EditSerial = Edit_SerialEntry.get()
    Edit_SerialEntry.delete(0, END)

    if (EditSerial not in serials) or (EditSerial == "") or (EditSerial == None) or EditSerial == "0":
        l1.config(text=f"Please enter a valid Serial\nMax Serial: {serials[-1]}")
    elif int(EditSerial) <=0:
        l1.config(text=f"Please enter a valid Serial\nMax Serial: {serials[-1]}")
    else:
        EditSerial = int(EditSerial)

        Add = []  #to be added in db
        Add.append(str(EditSerial)) #add initial Serial No.
        for entry, lenght, field in zip(Entries, Widths[1:], Fields[2::2]):
            x = entry.get()
            if len(x) > lenght:
                l1.config(text=f"Entry of {field}\nShould be With-in Specified length: {lenght}")
                return

            Add.append(x)
            entry.delete(0, END)
        db[EditSerial] = Add
        l1.config(text="Edited!\nFill Above Data to Edit More ")
        WrtieToFile(db, Name)

def Edit_EditEntry(Selection):
    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    win = Tk()
    win.title("Adding Entries")
    CanvasWidth = 450
    CanvasHeight = 450
    win.geometry(f"{CanvasWidth}x{CanvasHeight}+400+180")
    win.resizable(False, False)

    # Scroll Bar
    scroll = Scrollbar(win, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)

    # Setting it to Control OUR Canvas
    canvas = Canvas(win, width=CanvasWidth, height=CanvasHeight, yscrollcommand=scroll.set)
    canvas.pack()
    scroll.config(command=canvas.yview)

    # Frame to Put Entries
    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=NW)

    #Edit-Serials
    label = Label(frame, text=f"S-No. of Entry You Want to Edit")
    Edit_SerialEntry = Entry(frame, width=30)
    label.grid(row=0, column=0, padx=10, pady=10)
    Edit_SerialEntry.grid(row=0, column=1, padx=10, pady=10)

    # Entries Layout
    Entries = []
    for i, r in zip(range(1, No_fields + 1), range(No_fields)):
        label = Label(frame, text=f"Enter Data In '{FieldNames[r]}': ")
        entry = Entry(frame, width=30)
        label.grid(row=r+1, column=0, padx=10, pady=10)
        entry.grid(row=r+1, column=1, padx=10, pady=10)
        Entries.append(entry)  # create a list of all entry Widget data~~!
    i = []
    i.append(int(db[-1][0]) + 1)
    b1 = Button(frame, text="Edit Entry", width=20, height=2,
                command=lambda: Edit_EditEntry2(db, Entries, Widths, Fields, l1, i, Name,Edit_SerialEntry))
    b1.grid(row=r + 2, column=0, padx=10, pady=10)

    b2 = Button(frame, text="Finish", width=20, height=2, command=lambda: Finish(win,"Edited"))
    b2.grid(row=r + 2, column=1, padx=10, pady=10)

    l1 = Label(frame, text="Please Fill Above Data to Edit Entries")
    l1.grid(row=r + 3, column=0, padx=10, pady=10)

    l2 = Label(frame, text="Press Finish To Complete Editing")
    l2.grid(row=r + 3, column=1, padx=10, pady=10)
    # Update scrollable area
    frame.update_idletasks()  # Ensure the frame has been updated before getting the bounding box
    canvas.config(scrollregion=canvas.bbox("all"))

    win.mainloop()

def Edit_AddEntry(Selection):
    Name = Selection.get()
    db = RetriveData(Name)
    Fields = db[0]
    Widths = db[0][1::2]
    Widths = list(map(int, Widths))
    FieldNames = Fields[2::2]
    No_fields = len(FieldNames)
    win = Tk()
    win.title("Adding Entries")
    CanvasWidth = 450
    CanvasHeight = 400
    win.geometry(f"{CanvasWidth}x{CanvasHeight}+400+180")
    win.resizable(False, False)

    # Scroll Bar
    scroll = Scrollbar(win, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)

    # Setting it to Control OUR Canvas
    canvas = Canvas(win, width=CanvasWidth, height=CanvasHeight, yscrollcommand=scroll.set)
    canvas.pack()
    scroll.config(command=canvas.yview)

    # Frame to Put Entries
    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=NW)

    # Entries Layout
    Entries = []
    for i, r in zip(range(1, No_fields + 1), range(No_fields)):
        label = Label(frame, text=f"Enter Data In '{FieldNames[r]}': ")
        entry = Entry(frame, width=30)
        label.grid(row=r, column=0, padx=10, pady=10)
        entry.grid(row=r, column=1, padx=10, pady=10)
        Entries.append(entry)  # create a list of all entry Widget data~~!
    i = []
    i.append(int(db[-1][0])+1)
    b1 = Button(frame, text="Add Entry", width=20, height=2,
                command=lambda: AddEntry(db, Entries, Widths, Fields, l1, i, Name))
    b1.grid(row=r + 1, column=0, padx=10, pady=10)

    b2 = Button(frame, text="Finish", width=20, height=2, command=lambda: Finish(win,"Edited"))
    b2.grid(row=r + 1, column=1, padx=10, pady=10)

    l1 = Label(frame, text="Please Fill Above Data to Add Entries")
    l1.grid(row=r + 2, column=0, padx=10, pady=10)

    l2 = Label(frame, text="Press Finish To Complete Creation")
    l2.grid(row=r + 2, column=1, padx=10, pady=10)
    # Update scrollable area
    frame.update_idletasks()  # Ensure the frame has been updated before getting the bounding box
    canvas.config(scrollregion=canvas.bbox("all"))

    win.mainloop()
####################[Functions for all]##################################################################

def WriteEmptyFile(Name):

    with open(f'Data/{Name}.txt', "w") as g:  # creates Empty file
        g.write("S.No,5")

def WrtieToFile(db,name):
    fields = db[0]
    widths = db[0][1::2]
    with open(f'Data/{name}.txt', "w") as f:
        # Writing Header
        f.write(','.join(f'{field}' for field in (fields[:])) + '\n')
        # Write the entry as a formatted line
        for part in db[1:]:
            f.write(','.join(f'{entry}' for entry, width in zip(part, widths)) + '\n')

####################[Delete DBMS]#################################################################################
def DeleteDatabase(Selection,Selector,frame):
    Del = Selection.get()
    DBnames = Update_DataBaseNames()
    os.remove(f'Data/{Del}.txt')

    DelIndex = DBnames.index(Del)
    del DBnames[DelIndex]
    with open("Databases Names.txt", "w") as f:
        for name in DBnames:
            f.write(f"{name+","}")
    messagebox.showinfo("Update", f"Database '{Selection.get()}' has been Deleted")

    DBnames = Update_DataBaseNames()
    Selection.set(DBnames[0])
    Selector = OptionMenu(frame, Selection, *DBnames)
    Selector.config(width=20, height=2)
    Selector.place(x=200, y=50)

####################[Display DBMS]#####################################################################

def DisplayDataBase(Selection):

    Select = Selection.get()
    data = []
    with open(f"Data/{Select}.txt","r") as h:
        for line in h:
            data.append(line.strip().split(","))

    #Strip all Elements
    for i in range(len(data)):
        data[i] = [element.strip() for element in data[i]]

    Display(data,Select) # Show it

def Display(data,Select="Search"):

    root = Tk()
    root.title(f"{Select} View")

    # Calculate total width for the window
    total_width = sum(int(data[0][i]) * 10 for i in range(1, len(data[0]), 2)) + 100
    root.geometry(f"{total_width}x500+200+100")

    # Create a frame to hold the Display and scrollbars
    frame = ttk.Frame(root)
    frame.pack(fill=BOTH, expand=True)

    #Create a Treeview widget to display the data AND remove Phantom Column
    tree = ttk.Treeview(frame, show='headings')

    #scrollbars
    v_scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)  # Vertical scrollbar
    h_scroll = ttk.Scrollbar(frame, orient=HORIZONTAL, command=tree.xview)  # Horizontal scrollbar

    # Configure the Treeview to use the scrollbars
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    # Extract the column names and widths from the first list
    columns = data[0][::2]

    # Set the columns of the Treeview
    tree["columns"] = columns

    #Setting the headings and column widths
    for i in range(len(columns)):
        col_name = columns[i]
        width = int(data[0][2 * i + 1]) * 10  # Scale width for better visibility
        tree.heading(col_name, text=col_name)
        tree.column(col_name, width=width, anchor='center')  # Center align the text

    # Show Entries~
    for row in data[1:]:
        tree.insert("", "end", values=row)

    # Pack the Treeview and scrollbars in the frame
    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")  # Vertical scrollbar on the right and stretch up-down
    h_scroll.grid(row=1, column=0, sticky="ew")  # Horizontal scrollbar at the bottom and stretch left-right

    # frame resizable
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    root.mainloop()

def STR_Db(db):

    #Loop to convert all elements to strings
    for i in range(len(db)):
        for j in range(len(db[i])):
            db[i][j] = str(db[i][j])

    #Returns the Db
    return db

####################[Create DBMS]#####################################################################

def TempInputs(win,E1,L3,db):
    Name = E1.get()
    DBnames = Update_DataBaseNames()

    Widths = db[0][1::2]
    STR_Db(db)
    Fields = db[0]
    No_fields = len(Fields[2::2])

    if Name == "":
        L3.config(text="Please Fill 'All' Above Entries")
    elif Name in DBnames:
        L3.config(text="Database with that Name Already Exist.")
    else:
        win.destroy()
        DBnames.append(Name)
        with open('Databases Names.txt', "w") as f:
            for name in DBnames:
                f.write(f"{name},")
        WriteEmptyFile(Name)
        FieldNames = Fields[2::2]
        win = Tk()
        win.title("Adding Entries")
        CanvasWidth = 450
        CanvasHeight = 400
        win.geometry(f"{CanvasWidth}x{CanvasHeight}+400+180")
        win.resizable(False, False)

        # Scroll Bar
        scroll = Scrollbar(win, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        # Setting it to Control OUR Canvas
        canvas = Canvas(win, width=CanvasWidth, height=CanvasHeight, yscrollcommand=scroll.set)
        canvas.pack()
        scroll.config(command=canvas.yview)

        # Frame to Put Entries
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=NW)

        # Entries Layout
        Entries = []
        for i, r in zip(range(1, No_fields + 1), range(No_fields)):
            label = Label(frame, text=f"Enter Data In '{FieldNames[r]}': ")
            entry = Entry(frame, width=30)
            label.grid(row=r, column=0, padx=10, pady=10)
            entry.grid(row=r, column=1, padx=10, pady=10)
            Entries.append(entry)  # create a list of all entry Widget data~~!
        i = [1]
        b1 = Button(frame, text="Add Entry", width=20, height=2,
                    command=lambda: AddEntry(db, Entries, Widths, Fields, l1, i, Name))
        b1.grid(row=r + 1, column=0, padx=10, pady=10)

        b2 = Button(frame, text="Finish", width=20, height=2, command=lambda: Finish(win,"Created"))
        b2.grid(row=r + 1, column=1, padx=10, pady=10)

        l1 = Label(frame, text="Please Fill Above Data to Add Entries")
        l1.grid(row=r + 2, column=0, padx=10, pady=10)

        l2 = Label(frame, text="Press Finish To Complete Creation")
        l2.grid(row=r + 2, column=1, padx=10, pady=10)
        # Update scrollable area
        frame.update_idletasks()  # Ensure the frame has been updated before getting the bounding box
        canvas.config(scrollregion=canvas.bbox("all"))

        win.mainloop()

def Select(win,Templates,selection):
    selection=selection.get()
    win.destroy()
    db = []
    db.append(Templates[selection])
    win = Tk()
    win.title("Create Custom Database")
    win.geometry("400x120+400+250")
    win.resizable(False, False)

    L1 = Label(win, text="Enter Database Name")
    E1 = Entry(win,width=30)
    L1.pack()
    E1.pack()

    L3 = Label(win, text="Please Fill Above Entry")
    L3.pack(pady=10)

    b1 = Button(win, text="Create", command=lambda: TempInputs(win,E1,L3,db))
    b1.pack()

    win.mainloop()

def Preview(win,Templates,selection,PreviewLable):

    select=selection.get()

    PreviewLable.config(text=f"|| {'  ||  '.join(Templates[select][::2])} ||",bg="white",anchor=CENTER,justify="center")

    if select in ["Inventory","Library Books"]:
        PreviewLable.place(x=100,y=400)
    elif select in ["School","Customer"]:
        PreviewLable.place(x=75,y=400)
    elif select in ["Employees"]:
        PreviewLable.place(x=50,y=400)
    elif select in ["Medical Records"]:


        PreviewLable.config(font=("Arial",10))
        PreviewLable.place(x=50,y=400)
    win.update()

def Finish(win,show):
    win.destroy()

    messagebox.showinfo("Info",f"DataBase Successfully {show}")

def AddEntry(db,Entries,Widths,Fields,l1,i,Name):
    Add = [str(i[0])]

    for entry,lenght,field in zip(Entries,Widths[1:],Fields[2::2]):
        x = entry.get()
        if len(x) > lenght:
            l1.config(text=f"Entry of {field}\nShould be With-in Specified length: {lenght}")
            return

        Add.append(x)
        entry.delete(0, END)
    db.append(Add)
    i[0]+=1
    l1.config(text = "Added!\nFill Above Data to Add More ")
    WrtieToFile(db,Name)

def InputFieldsData(win, E3, E4, L4,L5,L6,i,Fields,Widths,No_fields,Name):

    db = []
    x = E3.get()
    y = E4.get()
    if x == "" or y == "":
        L6.config(text="Please Enter all above Entries")
    elif not(y.isdigit()) or y == "0":
        L6.config(text="Length of Field should be Numeric and Can't be 0")
    elif int(y)<0:
        L6.config(text="Length of Field should be Positive")
    elif len(x) > int(y):
        L6.config(text="Length of Field should be Greater than Field Name")
    else:
        Fields.append(x)
        Fields.append(y)
        Widths.append(int(y))
        i[0]+=1
        E3.delete(0,END)
        E4.delete(0,END)
        L4.config(text=f"Enter Name Of Field No.{i[0]}")
        L5.config(text=f"Enter Length of Field No.{i[0]}")
        L6.config(text="Please Fill Above Entries")
        if i[0] == No_fields+1:
            db.append(Fields)
            win.destroy()
            FieldNames = Fields[2::2]
            win = Tk()
            win.title("Adding Entries")
            CanvasWidth = 450
            CanvasHeight = 400
            win.geometry(f"{CanvasWidth}x{CanvasHeight}+400+180")
            win.resizable(False, False)

            # Scroll Bar
            scroll = Scrollbar(win, orient=VERTICAL)
            scroll.pack(side=RIGHT, fill=Y)

            # Setting it to Control OUR Canvas
            canvas = Canvas(win, width=CanvasWidth, height=CanvasHeight, yscrollcommand=scroll.set)
            canvas.pack()
            scroll.config(command=canvas.yview)

            # Frame to Put Entries
            frame = Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor=NW)

            # Entries Layout
            Entries = []
            for i, r in zip(range(1, No_fields + 1), range(No_fields)):
                label = Label(frame, text=f"Enter Data In '{FieldNames[r]}': ")
                entry = Entry(frame, width=30)
                label.grid(row=r, column=0, padx=10, pady=10)
                entry.grid(row=r, column=1, padx=10, pady=10)
                Entries.append(entry)  # create a list of all entry Widget data~~!
            i = [1]
            b1 = Button(frame, text="Add Entry", width=20, height=2,
                        command=lambda: AddEntry(db, Entries, Widths, Fields, l1, i,Name))
            b1.grid(row=r + 1, column=0, padx=10, pady=10)

            b2 = Button(frame, text="Finish", width=20, height=2, command=lambda: Finish(win,"Created"))
            b2.grid(row=r + 1, column=1, padx=10, pady=10)

            l1 = Label(frame, text="Please Fill Above Data to Add Entries")
            l1.grid(row=r + 2, column=0, padx=10, pady=10)

            l2 = Label(frame, text="Press Finish To Complete Creation")
            l2.grid(row=r + 2, column=1, padx=10, pady=10)
            # Update scrollable area
            frame.update_idletasks()  # Ensure the frame has been updated before getting the bounding box
            canvas.config(scrollregion=canvas.bbox("all"))

            win.mainloop()

def Inputs(win,E1,E2,L3):
    Name = E1.get()
    No_fields = E2.get()
    DBnames = Update_DataBaseNames()

    if Name == "" or No_fields == "":
        L3.config(text="Please Fill 'All' Above Entries")
    elif Name in DBnames:
        L3.config(text="Database with that Name Already Exist.")
    elif not(No_fields.isdigit()) or No_fields == "0":
        L3.config(text="Number of Fields should be a Numeric Value and Can't be zero")
    else:
        ClearFrame(win)
        DBnames.append(Name)
        with open('Databases Names.txt', "w") as f:
            for name in DBnames:
                f.write(f"{name},")

        WriteEmptyFile(Name) #writes a file with that name and Serial-No. Header

        i = [1]
        Fields = ["S.No","5"]
        Widths = [5]
        No_fields = int(No_fields)
        L4 = Label(win, text=f"Enter Name Of Field No.1")
        L4.pack()
        E3 = Entry(win,width=20)
        E3.pack()
        L5 = Label(win, text=f"Enter Length Of Field No.1")
        L5.pack()
        E4 = Entry(win,width=20)
        E4.pack()

        L6 = Label(win, text="Please Fill Above Entries")
        L6.pack(pady=10)

        b2 = Button(win, text="Create", command=lambda: InputFieldsData(win,E3,E4,L4,L5,L6,i,Fields,Widths,No_fields,Name))
        b2.pack()

##################################[Custom DBMS Creation]##################################################

def CreateDBMS():
    win = Tk()
    win.title("Create Custom Database")
    win.geometry("400x170+400+250")
    win.resizable(False, False)
    L1 = Label(win, text="Enter Database Name")
    E1 = Entry(win,width=30)
    L1.pack()
    E1.pack()

    L2 = Label(win, text="Enter Database Name of Fields")
    E2 = Entry(win,width=30)
    L2.pack()
    E2.pack()

    L3 = Label(win, text="Please Fill Above Entries")
    L3.pack(pady=10)

    b1 = Button(win, text="Create", command=lambda: Inputs(win,E1,E2,L3))
    b1.pack()


    win.mainloop()

###################################[Using Templates]###########################################################
def TempDBMS(root):
    Templates = {
        'Customer': ['S No.', 5, 'CustomerID', 15, 'Name', 18, 'Email', 15, 'Phone', 14, 'Address', 20, 'City', 15],
        'Inventory': ['S No.', 5, 'ProductID', 15, 'Name', 18, 'Price', 8, 'Stock', 8, 'SupplierID', 10],
        'Employees': ['S No.', 5, 'EmployeeID', 10, 'Name', 18, 'Email', 15, 'Department', 15, 'Title', 10, 'Salary',
                      7],
        'School': ['S No.', 5, 'Roll No.', 8, 'Name', 18, "Father's Name", 18, 'Class', 8, 'Address', 20],
        'Library Books': ['S No.', 5, 'BookID', 10, 'Title', 30, 'Author', 18, 'Year', 6, 'Genre', 15, 'Availability',
                          14],
        'Medical Records': ['S No.', 5, 'PatientID', 10, 'Name', 18, 'Age', 6, 'Gender', 8, 'Diagnosis', 25,
                            'Treatment', 30, 'VisitDate', 12]}

    win = Toplevel(root)
    win.title("Create Database")
    win.geometry("600x500+400+100")
    win.resizable(False, False)
    win.configure(background="lightblue")
    selection = StringVar()
    selection.set("Customer") #initial Value

    title_label = Label(win, text="Select one of the Following Templates:", font=("Arial", 12, "bold"), pady=10,bg="lightblue")
    title_label.pack()
    frame = Frame(win,bg="lightyellow",borderwidth=1,relief="ridge",width=500,height=500)
    frame.place(x=225,y=50)

    #Radio-Buttons
    rb1 = Radiobutton(frame, text="Customer", variable=selection, value="Customer",relief="raised", font=("Arial", 12,))
    rb1.pack(padx=5,pady=10)

    rb2 = Radiobutton(frame, text="Inventory", variable=selection, value="Inventory",relief="raised", font=("Arial", 12,))
    rb2.pack(padx=5,pady=10)

    rb3 = Radiobutton(frame, text="Employees", variable=selection, value="Employees",relief="raised", font=("Arial", 12,))
    rb3.pack(padx=5,pady=10)

    rb4 = Radiobutton(frame, text="School", variable=selection, value="School",relief="raised", font=("Arial", 12,))
    rb4.pack(padx=5,pady=10)

    rb5 = Radiobutton(frame, text="Library Books", variable=selection, value="Library Books",relief="raised", font=("Arial", 12,))
    rb5.pack(padx=5,pady=10)

    rb6 = Radiobutton(frame, text="Medical Records", variable=selection, value="Medical Records",relief="raised", font=("Arial", 12,))
    rb6.pack(padx=5,pady=10)

    b1 = Button(win,text="Preview of Fields",width=20,height=2,command=lambda: Preview(win,Templates,selection,PreviewLable))
    b1.place(x=150,y=350)

    b1 = Button(win, text="Select", width=20, height=2,command=lambda: Select(win,Templates,selection))
    b1.place(x=305, y=350)

    PreviewLable=Label(win,text="\t       Previews Will be Shown Here",bg="lightblue",font=("Arial", 12))
    PreviewLable.place(x=100, y=400)


    win.mainloop()

#####################[Main BDMS]##################################################################

#Making a List of Available DataBases
def Update_DataBaseNames():
    with open("Databases Names.txt") as f:
        DBnames = f.readline().strip().split(",")
        DBnames = DBnames[:-1] #remove last element, as it's a Null String~~!
        return DBnames

def ClearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

#Functuality
def Create(root,frame,preLable):
    preLable.destroy()
    ClearFrame(frame)
    frame.config(relief="ridge", bg="lightyellow", bd=5,width=300,height=300)
    frame.place(x=250, y=250)
    b4 = Button(frame, text="Use Pre-Defined Templates", width=20, height=3,command=lambda: TempDBMS(root))
    b4.place(x=70,y=40)
    b5 = Button(frame, text="Create Custom Database", width=20, height=3, command=CreateDBMS)
    b5.place(x=70, y=150)

def Editbuttons(frame,Selection):
    # Destroy All Previous Widgets
    ClearFrame(frame)
    b5 = Button(frame, text="Add Entry", width=20, height=3,command=lambda : Edit_AddEntry(Selection))
    b5.place(x=50,y=40)
    b6 = Button(frame, text="Edit Entry", width=20, height=3,command=lambda :Edit_EditEntry(Selection))
    b6.place(x=50, y=120)
    b7 = Button(frame, text="Delete Entry", width=20, height=3,command=lambda :Edit_DeleteEntry(Selection))
    b7.place(x=50, y=200)

    #Fields
    b8 = Button(frame, text="Add Field", width=20, height=3,command=lambda :Edit_AddField(Selection))
    b8.place(x=220,y=40)
    b9 = Button(frame, text="Edit Field", width=20, height=3,command=lambda: Edit_EditField(Selection))
    b9.place(x=220, y=120)
    b10 = Button(frame, text="Delete Field", width=20, height=3,command=lambda :Edit_DeleteField(Selection))
    b10.place(x=220, y=200)

    #More
    b11 = Button(frame, text="View DataBase", width=20, height=3,command=lambda: DisplayDataBase(Selection))
    b11.place(x=390, y=40)
    b12 = Button(frame, text="Search/Filter DataBase", width=20, height=3,command=lambda:Edit_Search(Selection))
    b12.place(x=390, y=120)

def Edit(DBname,frame,preLable):
    DBname = Update_DataBaseNames()
    preLable.destroy()
    ClearFrame(frame)
    l2 = Label(frame, text="Select DataBase To Edit",font="Courier",justify="center",fg="black",bg="lightyellow")
    l2.place(x=170,y=10,)
    frame.config(relief="ridge", bg="lightyellow", bd=5,width=570,height=325)
    frame.place(x=120, y=250)
    Selection = StringVar()
    Selection.set(DBname[0])
    Selector = OptionMenu(frame, Selection, *DBname)
    Selector.config(width=20, height=2)
    Selector.place(x=200, y=50)
    b4 = Button(frame, text="Confirm", width=12, height=1,command=lambda:Editbuttons(frame,Selection))
    b4.place(x=240, y=100)

def View(DBname,frame,preLable):
    DBname = Update_DataBaseNames()
    preLable.destroy()
    ClearFrame(frame)
    frame.config(relief="ridge", bg="lightyellow", bd=5,width=570,height=325)
    frame.place(x=120, y=250)
    l2 = Label(frame, text="Select DataBase To View",font="Courier",justify="center",fg="black",bg="lightyellow")
    l2.place(x=170,y=10,)
    Selection = StringVar()
    Selection.set(DBname[0])
    Selector = OptionMenu(frame, Selection, *DBname)
    Selector.config(width=20, height=2)
    Selector.place(x=200, y=50)
    b4 = Button(frame, text="View", width=12, height=1,command=lambda:DisplayDataBase(Selection))
    b4.place(x=240, y=100)

def delete(DBname,frame,preLable):
    preLable.destroy()
    ClearFrame(frame)
    l2 = Label(frame, text="Select DataBase To Delete",font="Courier",justify="center",fg="black",bg="lightyellow")
    l2.place(x=170,y=10,)
    frame.config(relief="ridge", bg="lightyellow", bd=5,width=570,height=325)
    frame.place(x=120, y=250)
    DBname = Update_DataBaseNames()
    Selection = StringVar()
    Selection.set(DBname[0])
    Selector = OptionMenu(frame, Selection, *DBname)
    Selector.config(width=20, height=2)
    Selector.place(x=200, y=50)
    b4 = Button(frame, text="Delete", width=12, height=1,command=lambda: DeleteDatabase(Selection,Selector,frame))
    b4.place(x=240, y=100)

#Create New DataBase
def Main():
    root = Tk()
    root.title("DataBase Management System")
    root.geometry("800x600+250+50")
    root.resizable(False, False)
    frame = Frame(root, relief="ridge", bg="lightyellow", bd=5, width=570, height=325)
    frame.place(x=120, y=250)
    preLable = Label(frame, text="Click on Above Buttons to See Respective Options Here.", bg="lightyellow")
    preLable.place(x=140, y=150)

    DBname = Update_DataBaseNames()
    t1 =("\t\t================================\n"
        "\t\t*****   *****   **    **  *****\n"
        "\t\t**  **  **  **  ***  ***  **   \n"
        "\t\t**  **  ******  ** ** **  *****\n"
        "\t\t**  **  **  **  **    **     **\n"
        "\t\t*****   *****   **    **  *****\n"
        "\t\t================================")
    l1 = Label(root, text=t1,font="Courier",justify="center",fg="black")
    l1.place(x=95,y=0)

    b1 = Button(root, text="Create New DataBase",width=20,height=3, command=lambda: Create(root,frame,preLable))
    b1.place(x=70,y = 150)

    #Edit DataBase
    b2 = Button(root, text="Edit Existing DataBase",width=20,height=3,command=lambda: Edit(DBname,frame,preLable) )
    b2.place(x=240,y = 150)

    #View Existing
    b3 = Button(root, text="View Existing DataBase",width=20,height=3, command=lambda: View(DBname,frame,preLable))
    b3.place(x=410,y = 150)

    #Delete Existing DataBase
    b3 = Button(root, text="Delete Existing DataBase",width=20,height=3,command=lambda: delete(DBname,frame,preLable))
    b3.place(x=580,y = 150)

    root.mainloop()

Main()