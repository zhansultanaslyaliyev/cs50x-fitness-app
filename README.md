# Fitness App

#### Description:

The **Fitness App** is my final project for Harvard's CS50x Introduction to Computer Science. I built this web application to help users calculate their daily calorie needs and track fitness goals using **Flask**, **Python**, **SQLite**, **HTML**, **CSS**, and **Flask-WTF**. Combining my passion for fitness with CS50x skills, I created a secure, user-friendly tool that allows users to register, log in, calculate calories, and view their profile history in a clean, responsive interface. This project showcases my ability to build a full-stack application from scratch, applying concepts from CS50x lectures.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Design Choices](#design-choices)
- [Challenges](#challenges)
- [Setup Instructions](#setup-instructions)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)

---

## Overview
The Fitness App enables users to calculate their daily calorie requirements based on personal metrics like age, gender, height, weight, activity level, and fitness goals (maintain, lose, or gain weight). It features secure user authentication, a calorie calculator using the Mifflin-St Jeor equation, and a profile history stored in a SQLite database. The interface is styled with a soft blue and white palette, featuring a sticky navigation bar, card-based forms, and flash messages for feedback.

---

## Features
- **User Authentication**: Register and log in with a username and password (hashed using Werkzeug’s `generate_password_hash`).
- **Calorie Calculator**: Input age, gender, height, weight, activity level, and goal to calculate daily calories.
- **Profile History**: Save calculations to a SQLite database and display them in a table.
- **Responsive UI**: Clean design with a sticky navigation bar, responsive forms, and flash messages for success/error feedback.
- **Security**: CSRF protection via Flask-WTF and a secure `FLASK_SECRET_KEY` loaded from a `.env` file.

---

## File Structure
The project includes the following files:

- **`app.py`**:
  - Main Flask application with routes for `/` (landing), `/register`, `/login`, `/logout`, and `/dashboard`.
  - Implements the `calculate_calories` function using the Mifflin-St Jeor equation.
  - Manages SQLite database connections and initializes `users` and `profiles` tables.
  - Uses Flask-WTF for form validation and `python-dotenv` for secure key management.

- **`requirements.txt`**:
  - Lists dependencies: `flask`, `flask-wtf`, `python-dotenv`, `werkzeug`.

- **`.gitignore`**:
  - Excludes sensitive files: `.env` (with `FLASK_SECRET_KEY`) and `models.db` (SQLite database).

- **`static/style.css`**:
  - Custom CSS with a white and soft blue palette (`--accent: #3b82f6`).
  - Styles responsive forms, a sticky navigation bar, and flash messages.

- **`templates/layout.html`**:
  - Base template with a dynamic navigation bar (login/register or dashboard/logout) and flash message display.

- **`templates/index.html`**:
  - Landing page with a welcome message and login/register buttons.

- **`templates/dashboard.html`**:
  - Contains the calorie calculator form and profile history table.

- **`templates/login.html` and `templates/register.html`**:
  - Authentication forms with CSRF protection, styled consistently.

---

## Design Choices
I chose **Flask** for its lightweight nature and familiarity from CS50x Lecture 9, making it ideal for a small-scale web app. **SQLite** was selected for its simplicity and integration with Flask, though I researched foreign key constraints to link `users` and `profiles` tables.

For security, I initially hardcoded the `FLASK_SECRET_KEY` but switched to a `.env` file with `python-dotenv` after learning best practices, enhancing safety. **Flask-WTF** was critical for CSRF protection and form validation (e.g., ensuring positive numbers), preventing crashes and attacks. I considered adding a password confirmation field for registration but prioritized simplicity, enforcing a minimum password length instead.

The UI uses a custom CSS stylesheet with a responsive grid layout for forms, optimized for mobile devices. The sticky navigation bar improves usability, though it required careful CSS tuning. I debated including calorie results in the history table but chose to display only input data to keep it clean.

---

## Challenges
Building the app was challenging:
- **Database Setup**: I initially forgot to call `init_db()`, causing SQLite errors. Debugging taught me to verify table creation.
- **Form Validation**: Learning Flask-WTF’s validators (e.g., `NumberRange`) was complex but prevented invalid input issues.
- **Responsive Design**: Iterating on CSS to make forms mobile-friendly was time-consuming but improved the user experience.
- **Security**: Implementing `.env` and CSRF protection required research into secure practices.

These hurdles deepened my understanding of debugging and resourcefulness, using CS50x notes and online documentation.

---

## Setup Instructions
To run the Fitness App locally:
1. Clone the repository:
   ```bash
   git clone https://github.com/zhansultanaslyaliyev/cs50x-fitness-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd cs50x-fitness-app
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with a secure key:
   ```bash
   echo FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(16))") > .env
   ```
5. Run the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in a browser.

---

## Future Improvements
With more time, I’d enhance the app by:
- Adding a password confirmation field for registration.
- Allowing users to edit or delete profile entries.
- Including timestamps in the `profiles` table.
- Deploying to Heroku for public access.

---

## Conclusion
The Fitness App is the culmination of my CS50x journey, integrating **Python**, **Flask**, **SQL**, **HTML**, and **CSS** from Lectures 6–9. I’m proud of building a secure, functional, and visually appealing app from scratch, overcoming challenges like database setup and form validation. This project demonstrates my ability to apply CS50x concepts to a real-world problem, creating a tool that could genuinely help users with fitness goals. I hope you enjoy exploring it as much as I enjoyed building it!

