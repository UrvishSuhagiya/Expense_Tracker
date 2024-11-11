from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
from tkcalendar import DateEntry

# Function to update the expense table and total expense
def update_table():
    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        # Retrieve expenses from the database
        month = entry_month.get()
        year = entry_year.get()

        # Construct the SQL query based on the search filter
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

        # Clear the expense table
        expense_table.delete(*expense_table.get_children())

        # Populate the expense table with the retrieved expenses
        for expense in expenses:
            expense_table.insert("", "end", values=expense)

        dbconnector.close()

        # Update the total expense display
        total_expense = sum(expense[4] for expense in expenses)
        total_expense_label.config(text="Total Expense: $" + str(total_expense))

        # Calculate the amount used from the total monthly budget
        total_budget = get_monthly_budget(month, year)  # Retrieve the monthly budget
        amount_used = total_expense
        amount_remaining = total_budget - amount_used

        # Update the budget label
        label_budget.config(text="Total Monthly Budget: $" + str(total_budget) +
                                 "\n\nAmount Remaining: $" + str(amount_remaining))

        # Check if expenses exceed the total budget
        if total_expense > total_budget:
            messagebox.showwarning("Budget Exceeded", "You have exceeded the total budget.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return


# Function to add an expense
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

        # Insert the expense into the database
        dbcursor.execute("INSERT INTO Monthly_budget (Date, Payee, Description, Amount, Payment) VALUES (?, ?, ?, ?, ?)",
                         (date, payee, description, amount, payment))
        dbconnector.commit()

        # Clear the entry fields
        entry_date.set_date(datetime.datetime.now().date())
        entry_payee.delete(0, END)
        entry_description.delete(0, END)
        entry_amount.delete(0, END)
        entry_payment.delete(0, END)

        # Update the expense table and total expense
        update_table()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

# Function to edit an expense
def edit_expense():
    # Check if an expense is selected
    selected_item = expense_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to edit.")
        return

    # Get the expense ID
    expense_id = expense_table.item(selected_item)["values"][0]

    # Get the updated expense details from the entry fields
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

        # Update the expense in the database
        dbcursor.execute("UPDATE Monthly_budget SET Date=?, Payee=?, Description=?, Amount=?, Payment=? WHERE ID=?",
                         (date, payee, description, amount, payment, expense_id))
        dbconnector.commit()

        # Clear the entry fields
        entry_date.set_date(datetime.datetime.now().date())
        entry_payee.delete(0, END)
        entry_description.delete(0, END)
        entry_amount.delete(0, END)
        entry_payment.delete(0, END)

        # Update the expense table and total expense
        update_table()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

# Function to delete an expense
def delete_expense():
    # Check if an expense is selected
    selected_item = expense_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to delete.")
        return

    # Prompt for confirmation
    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected expense?")
    if not confirmation:
        return

    # Get the expense ID
    expense_id = expense_table.item(selected_item)["values"][0]

    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        # Delete the expense from the database
        dbcursor.execute("DELETE FROM Monthly_budget WHERE ID=?", (expense_id,))
        dbconnector.commit()

        # Clear the entry fields
        entry_date.set_date(datetime.datetime.now().date())
        entry_payee.delete(0, END)
        entry_description.delete(0, END)
        entry_amount.delete(0, END)
        entry_payment.delete(0, END)

        # Update the expense table and total expense
        update_table()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

# Function to populate the entry fields with the details of the selected expense
def populate_form(event):
    selected_item = expense_table.focus()
    if selected_item:
        expense_data = expense_table.item(selected_item)["values"]
        date_str = expense_data[1]
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        entry_date.set_date(date_obj)
        entry_payee.delete(0, END)
        entry_payee.insert(0, expense_data[2])
        entry_description.delete(0, END)
        entry_description.insert(0, expense_data[3])
        entry_amount.delete(0, END)
        entry_amount.insert(0, expense_data[4])
        entry_payment.delete(0, END)
        entry_payment.insert(0, expense_data[5])



# Function to add the monthly budget to the separate table
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

        # Check if the budget already exists for the selected month and year
        dbcursor.execute("SELECT * FROM Budget WHERE Month=? AND Year=?", (month, year))
        existing_budget = dbcursor.fetchone()

        if existing_budget:
            # Update the existing budget
            dbcursor.execute("UPDATE Budget SET Budget=? WHERE Month=? AND Year=?", (budget, month, year))
        else:
            # Insert a new budget
            dbcursor.execute("INSERT INTO Budget (Month, Year, Budget) VALUES (?, ?, ?)", (month, year, budget))

        dbconnector.commit()

        # Clear the budget entry field
        entry_budget.delete(0, END)

        messagebox.showinfo("Budget Added", "Monthly budget added successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

# Function to retrieve the monthly budget from the separate table
def get_monthly_budget(month, year):
    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        # Retrieve the monthly budget from the table
        dbcursor.execute("SELECT Budget FROM Budget WHERE Month=? AND Year=?", (month, year))
        budget = dbcursor.fetchone()

        dbconnector.close()

        return budget[0] if budget else 0

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return 0

# Function to filter expenses by month
def filter_expenses():
    try:
        dbconnector = sqlite3.connect("Expense_Tracker.db")
        dbcursor = dbconnector.cursor()

        # Retrieve the selected month and year from the entry fields
        month = entry_month.get()
        year = entry_year.get()

        # Construct the SQL query based on the selected month and year
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

        # Clear the expense table
        expense_table.delete(*expense_table.get_children())

        # Populate the expense table with the filtered expenses
        for expense in expenses:
            expense_table.insert("", "end", values=expense)

        dbconnector.close()

        # Update the total expense display
        total_expense = sum(expense[4] for expense in expenses)
        total_expense_label.config(text="Total Expense: $" + str(total_expense))

        # Calculate the amount used from the total monthly budget
        total_budget = get_monthly_budget(month, year)  # Retrieve the monthly budget
        amount_used = total_expense
        amount_remaining = total_budget - amount_used

        # Update the budget label
        label_budget.config(text="Total Monthly Budget: $" + str(total_budget) +
                                 "\n\nAmount Remaining: $" + str(amount_remaining))

        # Check if expenses exceed the total budget
        if total_expense > total_budget:
            messagebox.showwarning("Budget Exceeded", "You have exceeded the total budget.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

# Create the main window
window = Tk()
window.title("Expense Tracker")

# Create a frame for the budget section
frame_budget = Frame(window)
frame_budget.pack(pady=10)

# Create a button to filter expenses by month
button_filter = Button(frame_budget, text="Filter", command=filter_expenses)
button_filter.grid(row=0, column=7, padx=5)

# Create a label and entry fields for month and year
label_month = Label(frame_budget, text="Month:")
label_month.grid(row=0, column=0, padx=5)
entry_month = ttk.Combobox(frame_budget, values=["01", "02", "03", "04", "05", "06",
                                                 "07", "08", "09", "10", "11", "12"])
entry_month.grid(row=0, column=1, padx=5)
label_year = Label(frame_budget, text="Year:")
label_year.grid(row=0, column=2, padx=5)
entry_year = ttk.Combobox(frame_budget, values=["2021", "2022", "2023"])  # Modify the list of years as needed
entry_year.grid(row=0, column=3, padx=5)

# Create a label and entry field for the budget
label_budget_amount = Label(frame_budget, text="Budget:")
label_budget_amount.grid(row=0, column=4, padx=5)
entry_budget = Entry(frame_budget)
entry_budget.grid(row=0, column=5, padx=5)

# Create a button to add the monthly budget
button_add_budget = Button(frame_budget, text="Add Budget", command=add_budget)
button_add_budget.grid(row=0, column=6, padx=5)

# Create a frame for the expense section
frame_expenses = Frame(window)
frame_expenses.pack(pady=10)

# Create a date picker for selecting the expense date
label_date = Label(frame_expenses, text="Date:")
label_date.grid(row=0, column=0, padx=5)
entry_date = DateEntry(frame_expenses, width=12, background='darkblue',
                       foreground='white', borderwidth=2)
entry_date.set_date(datetime.datetime.now().date())
entry_date.grid(row=0, column=1, padx=5)

# Create entry fields for payee, description, amount, and payment
label_payee = Label(frame_expenses, text="Payee:")
label_payee.grid(row=0, column=2, padx=5)
entry_payee = Entry(frame_expenses)
entry_payee.grid(row=0, column=3, padx=5)

label_description = Label(frame_expenses, text="Description:")
label_description.grid(row=0, column=4, padx=5)
entry_description = Entry(frame_expenses)
entry_description.grid(row=0, column=5, padx=5)

label_amount = Label(frame_expenses, text="Amount:")
label_amount.grid(row=0, column=6, padx=5)
entry_amount = Entry(frame_expenses)
entry_amount.grid(row=0, column=7, padx=5)

label_payment = Label(frame_expenses, text="Payment:")
label_payment.grid(row=0, column=8, padx=5)
entry_payment = Entry(frame_expenses)
entry_payment.grid(row=0, column=9, padx=5)

# Create buttons for adding, editing, and deleting expenses
button_add = Button(frame_expenses, text="Add Expense", command=add_expense)
button_add.grid(row=0, column=10, padx=5)

button_edit = Button(frame_expenses, text="Edit Expense", command=edit_expense)
button_edit.grid(row=0, column=11, padx=5)

button_delete = Button(frame_expenses, text="Delete Expense", command=delete_expense)
button_delete.grid(row=0, column=12, padx=5)

# Create a frame for the expense table
frame_table = Frame(window)
frame_table.pack(pady=10)

# Create a scrollable table for displaying expenses
expense_table = ttk.Treeview(frame_table, columns=(1, 2, 3, 4, 5, 6),
                             show="headings", selectmode="browse")
expense_table.pack(side="left", fill="y")

# Configure the scrollbar for the expense table
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=expense_table.yview)
scrollbar.pack(side="right", fill="y")
expense_table.configure(yscrollcommand=scrollbar.set)

# Create columns for the expense table
expense_table.heading(1, text="ID")
expense_table.heading(2, text="Date")
expense_table.heading(3, text="Payee")
expense_table.heading(4, text="Description")
expense_table.heading(5, text="Amount")
expense_table.heading(6, text="Payment")

# Bind the populate_form function to the expense table
expense_table.bind("<<TreeviewSelect>>", populate_form)

# Create a label for displaying the total expense
total_expense_label = Label(window, text="Total Expense: $0")
total_expense_label.pack()

# Create a label for displaying the total monthly budget and amount remaining
label_budget = Label(window, text="Total Monthly Budget: $0\n\nAmount Remaining: $0")
label_budget.pack()

# Update the expense table and total expense initially
update_table()

# Run the main window
window.mainloop()