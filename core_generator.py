from datetime import date, datetime, timedelta
import random
from os import path, getcwd, mkdir
from telnetlib import TN3270E
import uuid

semesterend = datetime.strptime('2022-12-15', "%Y-%m-%d").date()

def Generate_Schedule(dnt, topic_name, description, t2s, rem_study_weekends): 

    cwd = str(getcwd())
    outdir = cwd+"/generated_schedules/"
    if path.isdir(outdir) == False:
        mkdir(outdir)

    dnt = datetime.strptime(dnt, "%Y-%m-%d").date()
    #new_dnt = str(dnt).replace("-", "")

    dates2study = [dnt,
    dnt+timedelta(days=1),
    dnt+timedelta(days=7),
    dnt+timedelta(days=28),
    dnt+timedelta(days=84)]

    if rem_study_weekends == "yes":
        #print("\n[+] Modifying dates to study to only be on weekdays...")
        for studyday in dates2study:
            if studyday.weekday() >= 4:
                pass
            else:
                if studyday.weekday() == 5:
                    new_studyday = studyday+timedelta(days=2)
                elif studyday.weekday() == 6:
                    new_studyday = studyday+timedelta(days=1)
                dates2study[dates2study.index(studyday)] = new_studyday


    def fname_rand(n1):
        n2 = n1+"-"+str(random.randint(111111,999999))
        if path.exists(outdir+n2+".ics"):
            fname_rand(n1)
        return outdir+n2

    fname = (topic_name.title()+"_Study_Schedule").replace(" ", "_")
    #print("\n[+] Generating schedule for: "+fname)
    fname2 = fname_rand(fname)+".ics"
    f = open(fname2, "a")
    f.write("BEGIN:VCALENDAR")

    uid = str(uuid.uuid4()).replace("-", "")

    for studyday in dates2study:
        #print("- Studying: "+str(studyday)+" - "+calendar.day_name[studyday.weekday()])
        #print(type(semesterend))
        if studyday > semesterend:
            pass
        else:
            t3s = str(int(t2s)+500)
            if len(t3s) == 5:
                t3s = "0"+t3s
            f.write("""
BEGIN:VEVENT
DTSTART:{}T{}
DTEND:{}T{}
UID:{}
RECURRENCE-ID:{}T{}
SUMMARY:{}
DESCRIPTION:{}
SEQUENCE:0
STATUS:CONFIRMED
TRANSP:OPAQUE
END:VEVENT
""".format(str(studyday).replace('-', ''), 
    t2s, 
    str(studyday).replace('-', ''), 
    t3s, 
    uid+"@google.com",
    str(studyday).replace('-', ''),
    t3s,
    "Review: " + topic_name,
    description))

    f.write("END:VCALENDAR")
    f.close()
    #print("\n[+] Schedule generated…")
    return fname2
