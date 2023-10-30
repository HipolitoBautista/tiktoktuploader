#main

import helper
import time
import schedule
import json
import random

# Open my users json
with open('./Accounts/accounts_config.json', 'r') as json_file:
    data = json.load(json_file)

# Create an instance of scheduler 
scheduler = schedule.Scheduler()
print("I'm working")
for user in data:
    # Generate a randome time to post daily
    hour = str(20)
    minute = str(random.randint(22, 27))    
    random_time = str(hour+":"+minute)
    # Schedule a daily job
    scheduler.every().day.at(random_time).do(lambda CurrentUser=user: helper.upload(CurrentUser, data[CurrentUser]))

all_jobs = scheduler.get_jobs()
print(all_jobs)
# Keep the script running, checks to see if job is ready to run 
while True:
    scheduler.run_pending()
    time.sleep(1)
