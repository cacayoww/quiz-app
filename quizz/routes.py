import datetime
import random
import requests
from flask import flash, jsonify, redirect, render_template, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from quizz import app, db
from quizz.forms import CitySearchForm, LoginForm, QuizForm, RegisterForm
from quizz.models import Quiz, User
import geocoder

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():

    current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
    current_year = datetime.datetime.now().year
    current_location = geocoder.ip('me')
    form = CitySearchForm()
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={current_location.city}&limit=1&appid=a0d923c60f5713ba036767a53e9fd928'
    r = requests.get(url).json()[0]
    url_weather = f"http://api.openweathermap.org/data/2.5/weather?lat={r['lat']}&lon={r['lon']}&units=metric&lang=id&appid=a0d923c60f5713ba036767a53e9fd928"
    r_weather = requests.get(url_weather).json()
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?lat={r['lat']}&lon={r['lon']}&units=metric&lang=id&appid=a0d923c60f5713ba036767a53e9fd928"
    r_forecast = requests.get(url_forecast).json()
    simplified_forecast = []

    for item in r_forecast['list']:
        dt = datetime.datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if (dt.date() - datetime.datetime.now().date()).days < 3:
            day_name = dt.strftime('%A')  
            time = dt.strftime('%H.%M')  
            weather = item['weather'][0]['main']
            icon_code = item['weather'][0]['icon']
            icon = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'
            simplified_forecast.append({"day":day_name, "time":time, "weather":weather, "icon": icon})

    if form.validate_on_submit():
        current_location = form.city.data
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={current_location}&limit=1&appid=a0d923c60f5713ba036767a53e9fd928'
        r = requests.get(url).json()[0]
        url_weather = f"http://api.openweathermap.org/data/2.5/weather?lat={r['lat']}&lon={r['lon']}&units=metric&appid=a0d923c60f5713ba036767a53e9fd928"
        r_weather = requests.get(url_weather).json()
        url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?lat={r['lat']}&lon={r['lon']}&units=metric&lang=id&appid=a0d923c60f5713ba036767a53e9fd928"
        r_forecast = requests.get(url_forecast).json()
        simplified_forecast = []
        for item in r_forecast['list']:
            dt = datetime.datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if (dt.date() - datetime.datetime.now().date()).days < 3:
                day_name = dt.strftime('%A')  
                time = dt.strftime('%H.%M')  
                weather = item['weather'][0]['main']
                icon_code = item['weather'][0]['icon']
                icon = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'
                simplified_forecast.append({"day":day_name, "time":time, "weather":weather, "icon": icon})
        return render_template('home.html', current_year=current_year, form=form, date=current_date, location=current_location, temp=round(r_weather['main']['temp']), forecast=simplified_forecast)

    return render_template('home.html', current_year=current_year, form=form, date=current_date, location=current_location.city, temp=round(r_weather['main']['temp']), forecast=simplified_forecast)

@app.route('/get_cities')
def get_cities():
    q = request.args.get('q', '')
    if not q:
        return jsonify([])
    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={q}&limit=5&appid=a0d923c60f5713ba036767a53e9fd928"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        cities = []
        for item in data:
            name = item.get('name')
            state = item.get('state')
            country = item.get('country')
            display_name = f"{name}, {state}, {country}" if state else f"{name}, {country}"
            cities.append(display_name)
        return jsonify(cities)
    return jsonify([])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(err)
           
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            return redirect(url_for('home'))
        else:
            flash('Username atau password salah!')
    return render_template('login.html', form=form)

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()
    quizzes = Quiz.query.all()    
    random_quiz = random.choice(quizzes)
    
    if form.validate_on_submit():
        question_id = request.form.get('question_id')
        current_quiz = Quiz.query.get(question_id)
        
        if current_quiz:
            if form.answer.data.lower() == current_quiz.correct_answer.lower():
                current_user.score += 10
                db.session.commit()
                flash('Benar! +10 poin', category='success')
            else:
                flash(f'Salah! Jawaban yang benar adalah {current_quiz.correct_answer.upper()}', category='error')
        
        return redirect(url_for('quiz'))
    
    random_quiz = random.choice(quizzes)
    return render_template('quiz.html', quiz=random_quiz, form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for('home'))