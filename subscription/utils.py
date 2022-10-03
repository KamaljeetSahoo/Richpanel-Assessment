from datetime import datetime, timedelta

def process_date(date):
    month = date.strftime("%b")
    d = date.day
    year = date.year
    if(d%10)==1:
        sf = "st"
    elif(d%10)==2:
        sf="nd"
    elif(d%10)==3:
        sf="rd"
    else:
        sf="th"
    final_date ={
        "month":month,"day":d,"suffix":sf,"year":year
    }
    return final_date