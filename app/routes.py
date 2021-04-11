from flask import render_template, request
import os
import json
import random

from app import app
from app.data import goals
from app.forms import AllTeachers, MyRequest, Booking

def read_teachers_from_file(file):
    with open(os.path.join(os.getcwd(), file), "r") as json_file:
        teachers = json.load(json_file)
    return teachers

@app.route('/')
def index():
    teachers = read_teachers_from_file("data.json")
    random.shuffle(teachers)
    return render_template('index.html', goals=goals, teachers=teachers[:6])

@app.route('/all/', methods=["GET", "POST"])
def all():
    teachers = read_teachers_from_file("data.json")
    form = AllTeachers()
    if request.method == "POST":
        return render_template('all.html', teachers=teachers, form=form, sorting=request.form["sortes_field"])
    else:
        return render_template('all.html', teachers=teachers, form=form, sorting="randomly")

@app.route('/profile/<int:id>/')
def profile(id):
    teachers = read_teachers_from_file("data.json")
    for item in teachers:
        if item["id"] == id:
            teacher = item
            print(teacher)
    return render_template('profile.html', teacher=teacher, goals=goals)

@app.route('/booking/<int:id>/<string:day>/<int:time>/', methods=["GET", "POST"])
def booking(id, day, time):
    form = Booking(request.form)
    teachers = read_teachers_from_file("data.json")
    if request.method == "POST" and form.validate_on_submit():
        with open("booking.json", "r") as json_file:
            data_from_json_file = json_file.read()
            if data_from_json_file != '':
                content = json.loads(data_from_json_file)
            else:
                content = []
        data_from_form = {"name": form.name.data, "phone number": form.phone.data, "day": day, "time": time}
        content.append(data_from_form)
        with open("booking.json", "w") as json_file:
            json.dump(content, json_file, indent=4, ensure_ascii=False)
        return render_template('booking_done.html', day=day, time=time, name=form.name.data, phone=form.phone.data)
    for item in teachers:
        if item["id"] == id:
            teacher = item
            picture = item["picture"]
            name = item["name"]
    return render_template('booking.html', form=form, teacher=teacher ,name=name, picture=picture, day=day, time=time)

@app.route('/booking_done/', methods=["POST"])
def booking_done():
    form = Booking(request.form)
    teachers = read_teachers_from_file("data.json")
    if request.method == "POST" and form.validate_on_submit():
        print('qweqew')
        for teacher in teachers:
            if teacher["id"] == id:
                print('qweqew')
        return render_template('booking_done.html')
    return render_template('booking_done.html')

@app.route('/goal/<string:id>')
def goal(id):
    teachers = read_teachers_from_file("data.json")
    list_of_teachers = [item for item in teachers if id in item["goals"]]
    return render_template('goal.html', teachers=list_of_teachers, goals=goals[id])

@app.route('/request/', methods=["GET", "POST"])
def render_request():
    form = MyRequest(request.form)
    if request.method == "POST" and form.validate_on_submit():
        with open("request.json", "r") as json_file:
            data_from_json_file = json_file.read()
            if data_from_json_file != '':
                content = json.loads(data_from_json_file)
            else:
                content = []
        data_from_form = {"name": form.name.data, "phone number": form.phone.data, "goal": goals[form.radio_1.data]["title"], "duration": form.radio_2.data}
        content.append(data_from_form)
        with open("request.json", "w") as json_file:
            json.dump(content, json_file, indent=4, ensure_ascii=False)
        return render_template('request_done.html', goals=goals, data=form.data)
    return render_template('request.html', form=form)

@app.errorhandler(404)
def http_404_handler(error):
    return "<p><h1>404 Страница не найдена</h1></p>", 404

@app.errorhandler(500)
def http_500_handler(error):
    return "<p><h1> 500 Ошибка сервера</h1></p>", 500