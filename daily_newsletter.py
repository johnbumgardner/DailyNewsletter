#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3

def wind_description(i):
        switcher={
                0:"calm",
                1:"light air",
                2:"light breeze",
                3:"gentle breeze",
                4:"moderate breeze",
                5:"fresh breeze",
                6:"strong breeze",
                7:"high wind",
                8:"gale",
                9:"strong gale",
                10:"storm",
                11:"violent storm",
                12:"hurricane"
             }
        return switcher.get(i,"Invalid wind")

def trello_tasks():
    trello_api_key = "Enter Key"
    trello_token = "Enter Token"
    trello_secret = "Enter Secret"

    #Get board ID of my personal board
    url = "https://api.trello.com/1/members/me/boards?key=" + trello_api_key + "&token=" + trello_token
    response = requests.get(url)
    x = response.json()
    board_id = x[0]["id"]


    #Get lists on my board and find list ID of my to-do/working board
    url = "https://api.trello.com/1/boards/" + board_id + "/lists?key=" + trello_api_key + "&token=" + trello_token
    lists = requests.request(
        "GET",
        url
    )
    lists = lists.json()

    for i in lists:
        if i['name'] == 'Working':
            working_list = i['id']



    #Get cards from my working list
    url = "https://api.trello.com/1/lists/"+ working_list + "/cards?key=" + trello_api_key + "&token=" + trello_token

    response = requests.request(
        "GET",
        url
    )

    tasks_to_notify = []

    cards = response.json()
    for i in cards:
        tasks_to_notify.append((i['name'],i['due'][0:10]))
    

    return tasks_to_notify




# Python program to find daily forecasts details of any city using openweathermap api 

# import required modules 
import requests, json
import getpass
from datetime import date

today = date.today()




# Enter your API key here 
api_key = "Enter API ke"

# base_url variable to store url 
base_url = "https://api.openweathermap.org/data/2.5/onecall?"

# Give city name 
city_name = "Charlotte"
state_name = "NC"
password = "password"



city_list = open("city.list.json")
# returns JSON object as a dictionary 
data = json.load(city_list) 

#iterate through and find the longitude and lattitudes that match

for obj in data:
    if obj["name"] == city_name and obj["state"] == state_name:
        print("Found Location")
        lat = obj["coord"]["lat"]
        lon = obj["coord"]["lon"]

# complete_url variable to store 
# complete url address 
complete_url = base_url + "lat=" + str(lat) + "&lon=" + str(lon) +  "&appid=" + api_key +  "&exclude=,current,minutely,hourly"+"&units=imperial"

# get method of requests module 
# return response object 
response = requests.get(complete_url) 

# json method of response object 
# convert json format data into 
# python format data 
x = response.json()

daily_max = x["daily"][0]["temp"]["max"]
daily_min = x["daily"][0]["temp"]["min"]
daily_description = x["daily"][0]["weather"][0]["description"]
daily_wind = x["daily"][0]["wind_speed"]

text = "Hi John,\n\nHere is your daily weather report for " + city_name + ", " + state_name + " on " + str(today) + ".\n\nThe weather today is expected to be " + daily_description + ".\n\n"+ "Expect temperatures ranging from " + str(daily_min) + "F to " + str(daily_max) + "F.\n\n"

#classify the wind speed
beaufort_scale = 0
if daily_wind <= 1:
    beaufort_scale = 0
elif daily_wind > 1 and daily_wind <= 3:
    beaufort_scale = 1
elif daily_wind > 3 and daily_wind <= 7:
    beaufort_scale = 2
elif daily_wind > 7 and daily_wind <= 12:
    beaufort_scale = 3
elif daily_wind > 12 and daily_wind <= 18:
    beaufort_scale = 4
elif daily_wind > 18 and daily_wind <= 24:
    beaufort_scale = 5
elif daily_wind > 24 and daily_wind <= 31:
    beaufort_scale = 6
elif daily_wind > 31 and daily_wind <= 38:
    beaufort_scale = 7
elif daily_wind > 38 and daily_wind <= 46:
    beaufort_scale = 8
elif daily_wind > 46 and daily_wind <= 54:
    beaufort_scale = 9
elif daily_wind > 54 and daily_wind <= 63:
    beaufort_scale = 10
elif daily_wind > 63 and daily_wind <= 72:
    beaufort_scale = 11
elif daily_wind >= 72:
    beaufort_scale = 12

text = text + "Based on the Beaufort Scale, the wind conditions are classified as " + wind_description(beaufort_scale) + ".\n\n"



#come up with what to wear based on rain
if "rain" in daily_description or "drizzle" in daily_description or "storm" in daily_description:
    rain_suggestion = "Anticipate some form of inclement weather. Consider having a jacket or umbrella. \n\n"
else:
    rain_suggestion = "There is no expectation of inclement weather. \n\n"

avg_temp = (daily_max + daily_min) / 2

if daily_min >= 50:
    if avg_temp < 50:
        temp_suggestion = "It is cold outside. Wear a sweater and long pants.\n\n"
    elif avg_temp < 70:
        temp_suggestion = "The weather is fair. Wear shorts and a sweater.\n\n"
    else:
        temp_suggestion = "It is warm outside. Wear shorts and a short-sleeved T-shirt.\n\n"
else:
    if avg_temp < 50:
        temp_suggestion = "It is cold outside. Wear a sweater and long pants.\n\n"
    elif avg_temp < 70:
        temp_suggestion = "The weather is fair, but will likely start cold. Wear shorts and a sweater.\n\n"
    else:
        temp_suggestion = "It is warm outside. Wear shorts and a short-sleeved T-shirt.\n\n"

trello_updates = "Keep these following items in mind today. They are due soon.\n\n"


tasks = trello_tasks()

for i in tasks:
    trello_updates = trello_updates + i[0] + " is due by " + i[1] + ".\n"


text = text + rain_suggestion + temp_suggestion + trello_updates +"\nHave a great day!"



#send the email
import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "burner_email@gmail.com"
receiver_email = "main_email@domain.com"

subject = "Weather Report for " + str(today)
message = 'Subject: {}\n\n{}'.format(subject, text)

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

