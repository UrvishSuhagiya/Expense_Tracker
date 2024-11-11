import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
from tkcalendar import DateEntry

def update_table():
    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        month = entry_month.get()
        year = entry_year.get()

        if month and year:
            query = "SELECT * FROM Monthly_budget WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?"
            dbcursor.execute(query, (month, year))
        elif month:
            query = "SELECT * FROM Monthly_budget WHERE strftime('%m', Date) = ?"
            dbcursor.execute(query, (month,))
        elif year:
            query = "SELECT * FROM Monthly_budget WHERE strftime('%Y', Date) = ?"
            dbcursor.execute(query, (year,))
        else:
            query = "SELECT * FROM Monthly_budget"
            dbcursor.execute(query)

        expenses = dbcursor.fetchall()

        expense_table.delete(*expense_table.get_children())

        for expense in expenses:
            expense_table.insert("", "end", values=expense)

        dbconnector.close()

        total_expense = sum(expense[4] for expense in expenses)
        total_expense_label.config(text="Expenses\n$" + str(total_expense))

        total_budget = get_monthly_budget(month, year)
        amount_used = total_expense
        amount_remaining = total_budget - amount_used

        label_budget.config(text="Budget\n$" + str(total_budget))
        label_remaining.config(text="Balance\n$" + str(amount_remaining))

        if total_expense > total_budget:
            messagebox.showwarning("Budget Exceeded", "You have exceeded the total budget.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

def add_expense():
    date = entry_date.get_date()
    payee = entry_payee.get()
    description = entry_description.get()
    amount = entry_amount.get()
    payment = entry_payment.get()

    if not date or not payee or not amount or not payment:
        messagebox.showerror("Error", "Please fill in all the required fields.")
        return

    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        dbcursor.execute("INSERT INTO Monthly_budget (Date, Payee, Description, Amount, Payment) VALUES (?, ?, ?, ?, ?)",
                         (date, payee, description, amount, payment))
        dbconnector.commit()

        entry_date.set_date(datetime.datetime.now().date())
        entry_payee.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_payment.delete(0, tk.END)

        update_table()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

def edit_expense():
    selected_item = expense_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to edit.")
        return

    expense_id = expense_table.item(selected_item)["values"][0]

    date = entry_date.get_date()
    payee = entry_payee.get()
    description = entry_description.get()
    amount = entry_amount.get()
    payment = entry_payment.get()

    if not date or not payee or not amount or not payment:
        messagebox.showerror("Error", "Please fill in all the required fields.")
        return

    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        dbcursor.execute("UPDATE Monthly_budget SET Date=?, Payee=?, Description=?, Amount=?, Payment=? WHERE ID=?",
                         (date, payee, description, amount, payment, expense_id))
        dbconnector.commit()

        entry_date.set_date(datetime.datetime.now().date())
        entry_payee.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_payment.delete(0, tk.END)

        update_table()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

def delete_expense():
    selected_item = expense_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to delete.")
        return

    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected expense?")
    if not confirmation:
        return

    expense_id = expense_table.item(selected_item)["values"][0]

    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        dbcursor.execute("DELETE FROM Monthly_budget WHERE ID=?", (expense_id,))
        dbconnector.commit()

        entry_date.set_date(datetime.datetime.now().date())
        entry_payee.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_payment.delete(0, tk.END)

        update_table()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

def populate_form(event):
    selected_item = expense_table.focus()
    if selected_item:
        expense_data = expense_table.item(selected_item)["values"]
        date_str = expense_data[1]
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        entry_date.set_date(date_obj)
        entry_payee.delete(0, tk.END)
        entry_payee.insert(0, expense_data[2])
        entry_description.delete(0, tk.END)
        entry_description.insert(0, expense_data[3])
        entry_amount.delete(0, tk.END)
        entry_amount.insert(0, expense_data[4])
        entry_payment.delete(0, tk.END)
        entry_payment.insert(0, expense_data[5])

def add_budget():
    month = entry_month.get()
    year = entry_year.get()
    budget = entry_budget.get()

    if not month or not year or not budget:
        messagebox.showerror("Error", "Please select a month and year, and enter the budget.")
        return

    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        dbcursor.execute("SELECT * FROM Budget WHERE Month=? AND Year=?", (month, year))
        existing_budget = dbcursor.fetchone()

        if existing_budget:
            dbcursor.execute("UPDATE Budget SET Budget=? WHERE Month=? AND Year=?", (budget, month, year))
        else:
            dbcursor.execute("INSERT INTO Budget (Month, Year, Budget) VALUES (?, ?, ?)", (month, year, budget))

        dbconnector.commit()

        entry_budget.delete(0, tk.END)

        messagebox.showinfo("Budget Added", "Monthly budget added successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

def get_monthly_budget(month, year):
    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        dbcursor.execute("SELECT Budget FROM Budget WHERE Month=? AND Year=?", (month, year))
        budget = dbcursor.fetchone()

        dbconnector.close()

        return budget[0] if budget else 0

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return 0

def filter_expenses():
    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        month = entry_month.get()
        year = entry_year.get()

        if month and year:
            query = "SELECT * FROM Monthly_budget WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?"
            dbcursor.execute(query, (month, year))
        elif month:
            query = "SELECT * FROM Monthly_budget WHERE strftime('%m', Date) = ?"
            dbcursor.execute(query, (month,))
        elif year:
            query = "SELECT * FROM Monthly_budget WHERE strftime('%Y', Date) = ?"
            dbcursor.execute(query, (year,))
        else:
            query = "SELECT * FROM Monthly_budget"
            dbcursor.execute(query)

        expenses = dbcursor.fetchall()

        expense_table.delete(*expense_table.get_children())

        for expense in expenses:
            expense_table.insert("", "end", values=expense)

        dbconnector.close()

        total_expense = sum(expense[4] for expense in expenses)
        total_expense_label.config(text="Expenses\n$" + str(total_expense))

        total_budget = get_monthly_budget(month, year)  # Retrieve the monthly budget
        amount_used = total_expense
        amount_remaining = total_budget - amount_used

        label_budget.config(text="Budget\n$" + str(total_budget))
        label_remaining.config(text="Balance\n$" + str(amount_remaining))

        if total_expense > total_budget:
            messagebox.showwarning("Budget Exceeded", "You have exceeded the total budget.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

def update_table():
    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        current_date = datetime.datetime.now()
        month = current_date.strftime('%m')
        year = current_date.strftime('%Y')

        if month and year:
            query = "SELECT * FROM Monthly_budget WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?"
            dbcursor.execute(query, (month, year))
        else:
            query = "SELECT * FROM Monthly_budget"
            dbcursor.execute(query)

        expenses = dbcursor.fetchall()

        expense_table.delete(*expense_table.get_children())

        for expense in expenses:
            expense_table.insert("", "end", values=expense)

        dbconnector.close()

        total_expense = sum(expense[4] for expense in expenses)
        total_expense_label.config(text="Expenses\n$" + str(total_expense))

        total_budget = get_monthly_budget(month, year)
        amount_used = total_expense
        amount_remaining = total_budget - amount_used

        label_budget.config(text="Budget\n$" + str(total_budget))
        label_remaining.config(text="Balance\n$" + str(amount_remaining))

        if total_expense > total_budget:
            messagebox.showwarning("Budget Exceeded", "You have exceeded the total budget.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

window = tk.Tk()
window.title("Expense Tracker")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.geometry(f"{screen_width}x{screen_height}")
window.state('zoomed')

lable = tk.Label(window,
                 text="Expense Tracker",
                 anchor=tk.CENTER,
                 fg="white",
                 bg="#3e3d53",
                 height=2,
                 width=10,
                 font=("Arial",17,"bold"))
lable.pack(fill=tk.BOTH)

frame_left = tk.Frame(window,bg="#7f7d9c")
frame_left.pack(side=tk.LEFT,fill=tk.BOTH)

frame_budget = tk.Frame(frame_left,bg="#7f7d9c")
frame_budget.pack(fill=tk.BOTH,side=tk.TOP)

label_month = tk.Label(frame_budget, 
                       text="Month:",
                       bg="#acadc9",
                       width=10,
                       font=("Arial",15))
label_month.grid(row=0, column=0, padx=10,pady=10)
entry_month = ttk.Combobox(frame_budget,
                           width=17,
                           font=("Arial",15), 
                           values=["01", "02", "03", "04", "05", "06",
                                    "07", "08", "09", "10", "11", "12"])
entry_month.grid(row=0, column=1,sticky=tk.W,padx=10,pady=10)

label_year = tk.Label(frame_budget, 
                      text="Year:",
                      bg="#acadc9",
                      width=10,
                      font=("Arial",15))
label_year.grid(row=1, column=0,padx=10,pady=10)
entry_year = ttk.Combobox(frame_budget,
                          width=17,
                          font=("Arial",15), 
                          values=["2021", "2022", "2023"])
entry_year.grid(row=1, column=1,sticky=tk.W,padx=10,pady=10)

label_budget_amount = tk.Label(frame_budget, 
                               text="Budget:",
                               bg="#acadc9",
                               width=10,
                               font=("Arial",15))
label_budget_amount.grid(row=2, column=0, padx=10,pady=10)
entry_budget = tk.Entry(frame_budget,
                        width=19,
                        font=("Arial",15))
entry_budget.grid(row=2, column=1,sticky=tk.W, padx=10,pady=10)

frame_filter=tk.Frame(frame_left,bg="#7f7d9c")
frame_filter.pack(fill=tk.BOTH)

button_add_budget = tk.Button(frame_filter,
                           text="Add Budget", 
                           command=add_budget,
                           font=("Arial",13,"bold"),
                           width=25,
                           height=1,
                           fg="white",
                           bg="#2f2f4f")
button_add_budget.grid(row=0, column=0,sticky=tk.W, padx=50,pady=10)

button_filter = tk.Button(frame_filter, text="Filter", 
                       command=filter_expenses,
                       font=("Arial",13,"bold"),
                       width=25,
                       height=1,
                       fg="white",
                       bg="#2f2f4f")
button_filter.grid(row=1, column=0,sticky=tk.W, padx=50,pady=10)

frame_label=tk.Frame(frame_left,bg="#7f7d9c")
frame_label.pack(fill=tk.BOTH)

label_date = tk.Label(frame_label, 
                      text="Date:",
                      bg="#acadc9",
                      width=10,
                      font=("Arial",15))
label_date.grid(row=0, column=0, padx=10,pady=10)
entry_date = DateEntry(frame_label, 
                       background='darkblue',
                       foreground='white', 
                       borderwidth=2,
                       width=17,
                       font=("Arial",15))
entry_date.set_date(datetime.datetime.now().date())
entry_date.grid(row=0, column=1,sticky=tk.W, padx=10,pady=10)

label_payee = tk.Label(frame_label, 
                       text="Payee:",
                       bg="#acadc9",
                       width=10,
                       font=("Arial",15))
label_payee.grid(row=1, column=0, padx=10,pady=10)
entry_payee = tk.Entry(frame_label,
                       width=19,
                       font=("Arial",15))
entry_payee.grid(row=1, column=1,sticky=tk.W, padx=10,pady=10)

label_description = tk.Label(frame_label, 
                             text="Description:",
                             bg="#acadc9",
                             width=10,
                             font=("Arial",15))
label_description.grid(row=3, column=0, padx=10,pady=10)
entry_description = tk.Entry(frame_label,
                             width=19,
                             font=("Arial",15))
entry_description.grid(row=3, column=1,sticky=tk.W, padx=10,pady=10)

label_amount = tk.Label(frame_label, 
                        text="Amount:",
                        bg="#acadc9",
                        width=10,
                        font=("Arial",15))
label_amount.grid(row=4, column=0, padx=10,pady=10)
entry_amount = tk.Entry(frame_label,
                        width=19,
                        font=("Arial",15))
entry_amount.grid(row=4, column=1,sticky=tk.W, padx=10,pady=10)

label_payment = tk.Label(frame_label, 
                         text="Payment:",
                         bg="#acadc9",
                         width=10,
                         font=("Arial",15))
label_payment.grid(row=5, column=0, padx=10,pady=10)
entry_payment = tk.Entry(frame_label,
                         width=19,
                         font=("Arial",15))
entry_payment.grid(row=5, column=1,sticky=tk.W, padx=10,pady=10)

frame_button = tk.Frame(frame_left,bg="#7f7d9c")
frame_button.pack(fill=tk.BOTH)

button_add = tk.Button(frame_button, 
                    text="Add Expense", 
                    command=add_expense,
                    font=("Arial",13,"bold"),
                    width=25,
                    height=1,
                    fg="white",
                    bg="#2f2f4f")
button_add.grid(row=0, column=0,sticky=tk.W, padx=50,pady=10)

button_edit = tk.Button(frame_button, 
                     text="Edit Expense", 
                     command=edit_expense,
                     font=("Arial",13,"bold"),
                     width=25,
                     height=1,
                     fg="white",
                     bg="#2f2f4f")
button_edit.grid(row=1, column=0,sticky=tk.W, padx=50,pady=10)

button_delete = tk.Button(frame_button, 
                       text="Delete Expense", 
                       command=delete_expense,
                       font=("Arial",13,"bold"),
                       width=25,
                       height=1,
                       fg="white",
                       bg="#2f2f4f")
button_delete.grid(row=2, column=0,sticky=tk.W, padx=50,pady=10)

frame_right=tk.Frame(window,bg="#acadc9")
frame_right.pack(fill=tk.BOTH,side=tk.RIGHT,expand=tk.TRUE)

frame_amount = tk.Frame(frame_right,bg="#acadc9")
frame_amount.pack(fill=tk.BOTH)

total_expense_label = tk.Label(frame_amount, 
                            text="Expence\n$0",
                            font=("Arial",12,"bold"),
                            width=36,
                            height=4,
                            bg="#7f7d9c")
total_expense_label.grid(row=0,column=1,sticky=tk.W,padx=10,pady=10)

label_budget = tk.Label(frame_amount, 
                     text="Budget\n$0",
                     font=("Arial",12,"bold"),
                     width=36,
                     height=4,
                     bg="#7f7d9c")
label_budget.grid(row=0,column=0,sticky=tk.W,padx=10,pady=10)

label_remaining = tk.Label(frame_amount, 
                     text="Balance\n$0",
                     font=("Arial",12,"bold"),
                     width=36,
                     height=4,
                     bg="#7f7d9c")
label_remaining.grid(row=0,column=2,sticky=tk.W,padx=10,pady=10)

frame_table = tk.Frame(frame_right,bg="#acadc9")
frame_table.pack(fill=tk.BOTH,expand=tk.TRUE)

style = ttk.Style()
style.configure("Treeview", font=("Arial", 12))

style = ttk.Style(frame_table)
style.configure("Treeview.Heading",
                highlightthickness=0,
                bd=1,
                font=("Arial",13))

expense_table = ttk.Treeview(frame_table, 
                             columns=(1, 2, 3, 4, 5, 6),
                             show="headings", 
                             selectmode=tk.BROWSE)

scrollbar = ttk.Scrollbar(frame_table, 
                          orient=tk.VERTICAL, 
                          command=expense_table.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
expense_table.configure(yscrollcommand=scrollbar.set)

expense_table.heading(1, text="ID",anchor=tk.CENTER)
expense_table.heading(2, text="Date",anchor=tk.CENTER)
expense_table.heading(3, text="Payee",anchor=tk.CENTER)
expense_table.heading(4, text="Description",anchor=tk.CENTER)
expense_table.heading(5, text="Amount",anchor=tk.CENTER)
expense_table.heading(6, text="Payment",anchor=tk.CENTER)

expense_table.column('#1',width=100,stretch=tk.NO, anchor=tk.CENTER)
expense_table.column('#2',width=150,stretch=tk.NO, anchor=tk.CENTER)
expense_table.column('#3',width=191,stretch=tk.NO, anchor=tk.CENTER)
expense_table.column('#4',width=285,stretch=tk.NO, anchor=tk.CENTER)
expense_table.column('#5',width=171,stretch=tk.NO, anchor=tk.CENTER)
expense_table.column('#6',width=260,stretch=tk.NO, anchor=tk.CENTER)

expense_table.place(relx=0,y=0,relheight=1,relwidth=1)

expense_table.bind("<<TreeviewSelect>>", populate_form)

update_table()

window.mainloop()