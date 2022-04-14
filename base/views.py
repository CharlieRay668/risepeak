from django.shortcuts import render
import pandas as pd
import numpy as np
import json
import ast
from .models import Team

# Create your views here.
def base(response):
    student_lookup = pd.read_csv("student_lookup.csv")
    students = set()
    for index, row in student_lookup.iterrows():
        print(row["students"])
        student_list = ast.literal_eval(row["students"])
        #student_list = json.loads(row["students"])
        print(type(student_list))
        for student_name in student_list:
            students.add(student_name)
    students = list(students)
    ss = Team.objects.get(name="ss")
    fj = Team.objects.get(name="fj")
    payload = {
        "students": students,
        "ss_score": ss.score,
        "fj_score": fj.score,
    }
    return render(response, "base/home.html", payload)

def staff(response, staff_pass):
    if staff_pass != "5970":
        return render(response, "base/invalid.html")
    ss_score = 0
    fj_score = 0
    if response.method == "POST":
        data = response.POST
        print(data)
        try:
            ss_score = int(data["ss_score"])
        except:
            ss_score = 0
        try:
            fj_score = int(data["fj_score"])
        except:
            fj_score = 0
        
    
    ss = Team.objects.get(name="ss")
    fj = Team.objects.get(name="fj")
    true_ss_score = ss.score + ss_score
    ss.score = true_ss_score
    ss.save()
    true_fj_score = fj.score + fj_score
    fj.score = true_fj_score
    fj.save()
    payload = {
        "ss_score": true_ss_score,
        "fj_score": true_fj_score,
    }
    return render(response, "base/staff.html", payload)

def student(response, student_name):
    print(student_name)
    student_lookup = pd.read_csv("student_lookup.csv")
    events = pd.read_csv("base/events.csv")
    student_schedule = []
    for index, row in student_lookup.iterrows():
        if student_name in row["students"]:
            event = events.loc[events["Event Name"] == row["event"]]
            student_schedule.append({
                "name": event["Event Name"].values[0],
                "time": event["Time"].values[0],
                "location": event["Location"].values[0],
                "stuco": event["StuCo Reps"].values[0],
                "staff": event["Staff Reps"].values[0]
            })
    payload = {"schedule": student_schedule, "student_name": student_name}
    return render(response, "base/student.html", payload)