from flask import Flask, render_template, send_file, request, redirect, after_this_request
from core_generator import *
from os import path
import os

app = Flask(__name__)

@app.route('/')
def schedule_home():
    return render_template('index.html')

@app.route('/how2')
def how2():
    return render_template('how2.html')

@app.route('/', methods=["POST"])
def schedule_gen():
    if request.form.get("clear"):
        return redirect("/")
    else:
        dnt = request.form.get("dnt")
        topic_name = request.form['topic']
        description = request.form['description']
        if request.form.get("rem_study_weekends"):
            rem_study_weekends = "yes"
        if request.form.get("t2s"):
            t2s = request.form.get('t2s')
        else:
            t2s = "120000"
        if not topic_name:
            topic_name = "Hello World"
        if not description:
            description = "Review of: "+topic_name
        if not request.form.get("rem_study_weekends"):
            rem_study_weekends = "no"
        new_schedule = Generate_Schedule(dnt, topic_name, description, t2s, rem_study_weekends)
        @app.after_request
        def rem_file(response):
            if path.exists(new_schedule):
                os.remove(new_schedule)
            return response
        return send_file(new_schedule, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0')