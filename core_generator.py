from datetime import date, datetime, timedelta
import random
from os import path, getcwd, mkdir

def Generate_Schedule(topic_name, description, t2s, rem_study_weekends): 
    
    semesterend = datetime.strptime('2022-12-15', "%Y-%m-%d").date()

    cwd = str(getcwd())
    outdir = cwd+"/generated_schedules/"
    if path.isdir(outdir) == False:
        mkdir(outdir)

    today = date.today()

    dates2study = [today,
    today+timedelta(days=1),
    today+timedelta(days=3),
    today+timedelta(days=7),
    today+timedelta(days=14),
    today+timedelta(days=30)]

    if rem_study_weekends == "yes":
        #print("\n[+] Modifying dates to study to only be on weekdays...")
        for studyday in dates2study:
            if studyday.weekday() >= 5:
                new_studyday = studyday
                while new_studyday.weekday() != 0:
                    new_studyday += timedelta(1)
                #print("- Changing a "+calendar.day_name[studyday.weekday()]+" to a "+calendar.day_name[new_studyday.weekday()])
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
    for studyday in dates2study:
        #print("- Studying: "+str(studyday)+" - "+calendar.day_name[studyday.weekday()])
        if studyday > semesterend:
            pass
        else:
            f.write("""
BEGIN:VEVENT
DTSTART:{}T{}
DTEND:{}T{}
SUMMARY:{}
DESCRIPTION:{}
SEQUENCE:0
STATUS:CONFIRMED
TRANSP:TRANSPARENT
END:VEVENT
""".format(str(studyday).replace('-', ''), t2s, str(studyday).replace('-', ''), str(int(t2s)+500), topic_name, description))

    f.write("END:VCALENDAR")
    f.close()
    #print("\n[+] Schedule generated…")
    return fname2
