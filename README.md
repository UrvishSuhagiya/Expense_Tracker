# Expense Tracker Django Project

Welcome to the *Expense Tracker Django Project*! This is a simple, interactive web application built using Django that allows users to track their personal expenses. The project is containerized using Docker to ensure a smooth and easy deployment process.

---

## 🛠 Technologies Used

- *Django* (Web framework)
- *Tkinter* (GUI for the desktop app)
- *Docker* (Containerization)
- *SQLite* (Database)
- *Pillow* (Image Handling)
- *tkcalendar* (Calendar for Date Selection)

---

## ✨ About the Project

The *Expense Tracker Django* project allows users to:
- *Track their daily expenses* by adding records of income and expenditure.
- *Manage categories* for different types of expenses.
- *View reports* to understand their spending patterns over time.

The project is built with the following features:
- *User Authentication*: Secure login and registration system.
- *Expense Management*: Add, view, update, and delete expenses.
- *Dockerized*: The app is packaged with Docker, making it easy to deploy in any environment.

---

## 🚀 How to Run the Project

### Prerequisites

Before running the project, make sure you have the following installed:

- *Docker* (for containerization)
  - To install Docker, follow the [official guide](https://docs.docker.com/get-docker/).
  
- *Git* (to clone the repository)
  - To install Git, follow the [official guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

### 1. Clone the Repository

Start by cloning the project repository to your local machine.

  git clone https://github.com/UrvishSuhagiya/Expense_Tracker.git
  cd expense-tracker-django

### 2. Build the Docker Image
Once you've cloned the repository, navigate to the project folder. In the root directory of the project, there is a Dockerfile that will help you create a Docker container.

Build the Docker image with the following command:

 - docker build -t expense-tracker-django .

This command will:

Create an image named expense-tracker-django using the instructions in the Dockerfile.
Install all the dependencies listed in requirements.txt (such as Django, Pillow, and Tkcalendar).
Set up the application.

### 3. Run the Docker Container
Once the image is successfully built, you can run the application with the following command:

- docker run -p 8000:8000 expense-tracker-django
  
This will:

Expose port 8000 on your local machine to port 8000 in the Docker container (the default port for Django's development server).
Start the Django application.

### 4. Access the Application
Now that the container is running, open your browser and go to:

- http://localhost:8000
  
You should see the home page of the Expense Tracker Django App.

### 5. Admin Access
To access the Django admin panel, you can use the following credentials:

Username: user
Password: user123

### 6. Database Migrations
If you haven't already applied migrations, you can run the following command to ensure your database is set up correctly:

- docker exec -it <container_id> python manage.py migrate

You can find the container_id by running:

- docker ps

### 🐳 Dockerfile Key Points:

Python Base Image: We use a slim version of the official Python 3.10 image to minimize the image size.
System Dependencies: We install system libraries such as tk for Tkinter (GUI support) and libsqlite3-dev for SQLite support.
Dependencies Installation: All Python dependencies are installed via pip using the requirements.txt file.
Expose Port: The container will expose port 8000 for the Django development server.
Migrations: The RUN python manage.py migrate command ensures that the database schema is up to date.
Start Django Server: The app is started using the Django development server (python manage.py runserver).

## 🎨 Screenshots

Here are some screenshots of the app:

| ![Screenshot 1](https://github.com/user-attachments/assets/1b87c0ce-d901-476e-a48d-d350d54fc773) | ![Screenshot 2](https://github.com/user-attachments/assets/0a2e1ac2-b1b6-48d4-8802-df27fbc1a983) |
| --- | --- |
| *Screenshot 1* | *Screenshot 2* |

| ![Screenshot 3](https://github.com/user-attachments/assets/9dfc9df7-5f0b-41cc-b625-4a7769ce36f9) | ![Screenshot 4](https://github.com/user-attachments/assets/5a777226-4170-417c-a5e8-a87fd5de3d41) |
| --- | --- |
| *Screenshot 3* | *Screenshot 4* |
