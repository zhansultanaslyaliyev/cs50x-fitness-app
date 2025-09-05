from flask import Flask, render_template, request, redirect, session, g, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key_for_dev")
DATABASE = "models.db"

# Database setup
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                age INTEGER,
                gender TEXT,
                height REAL,
                weight REAL,
                activity TEXT,
                goal TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()

# Forms
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class CalorieForm(FlaskForm):
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=1)])
    gender = SelectField("Gender", choices=["male", "female"], validators=[DataRequired()])
    height = FloatField("Height (cm)", validators=[DataRequired(), NumberRange(min=1)])
    weight = FloatField("Weight (kg)", validators=[DataRequired(), NumberRange(min=1)])
    activity = SelectField("Activity Level", choices=[
        ("sedentary", "Sedentary"), 
        ("light", "Lightly Active"), 
        ("moderate", "Moderately Active"), 
        ("active", "Active"), 
        ("very_active", "Very Active")
    ], validators=[DataRequired()])
    goal = SelectField("Goal", choices=[
        ("maintain", "Maintain"), 
        ("lose", "Lose Weight"), 
        ("gain", "Gain Muscle")
    ], validators=[DataRequired()])

# Calorie Calculation
def calculate_calories(age, gender, height, weight, activity, goal):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_levels = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }

    calories = bmr * activity_levels.get(activity, 1.2)

    if goal == "lose":
        calories -= 500
    elif goal == "gain":
        calories += 500

    return round(calories)

# Routes
@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = generate_password_hash(form.password.data)
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Username already taken!", "error")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            flash("Logged in successfully!", "success")
            return redirect("/dashboard")
        flash("Invalid username or password!", "error")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect("/login")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    form = CalorieForm()
    db = get_db()
    profiles = db.execute("SELECT * FROM profiles WHERE user_id = ? ORDER BY id DESC", (session["user_id"],)).fetchall()
    if form.validate_on_submit():
        calories = calculate_calories(
            form.age.data, form.gender.data, form.height.data, 
            form.weight.data, form.activity.data, form.goal.data
        )
        db.execute("INSERT INTO profiles (user_id, age, gender, height, weight, activity, goal) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (session["user_id"], form.age.data, form.gender.data, form.height.data, 
                    form.weight.data, form.activity.data, form.goal.data))
        db.commit()
        flash("Calculation saved!", "success")
        return render_template("dashboard.html", form=form, calories=calories, profiles=profiles)
    return render_template("dashboard.html", form=form, calories=None, profiles=profiles)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)