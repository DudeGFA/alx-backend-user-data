from datetime import datetime, timedelta
creation_time = datetime(2015,8,25,0,0,0,0)
if (creation_time + timedelta(seconds = 50)) < datetime.now():
    print("yeah")