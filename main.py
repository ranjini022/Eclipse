import time
import tkinter
from tkinter import *
from tkinter import messagebox
import requests
from configparser import ConfigParser
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim


root=Tk()
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
root.title("Weather app")
bg=PhotoImage("backgroundimg.png")
bglbl=tkinter.Label(root,image=bg)
bglbl.place(relheight=1,relwidth=1)
root.geometry("800x500+300+200")
root.resizable(False,False)

config_file = "config.ini"
config=ConfigParser()
config.read(config_file)
api_key = config['ranj']['api']

def getWeather(city):
    geolocator=Nominatim(user_agent="geopiExercises")
    location=geolocator.geocode(city)
    obj=TimezoneFinder()
    res=obj.timezone_at(lng=location.longitude,lat=location.latitude)
    home=pytz.timezone(res)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M:%p")
    clock.config(text=current_time)
    name.config(text="Current weather:")
    result=requests.get(url.format(city,api_key))
    if result:
        data=result.json()
        timez=int(data['timezone'])
        temp = data['main']['temp'] - 273.1
        condition = data['weather'][0]['main']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        descrip = data['weather'][0]['description']
        w_icon = data['weather'][0]['icon']
        sunr=time.strftime("%I:%M:%S",time.gmtime(data['sys']['sunrise']-timez-3600))
        suns=time.strftime("%I:%M:%S",time.gmtime(data['sys']['sunset']-timez-3600))
        final=[temp,condition,pressure,humidity,wind,descrip,w_icon,sunr,suns]
        return final
    else:
        print("not found")

def search():
    global image
    city=city_text.get()
    weather=getWeather(city)
    if weather:
        temperature['text']='{:.2f}°C'.format(weather[0])
        condition['text']='{}'.format(weather[1])
        pressure['text'] = '{}'.format(weather[2])
        humidity['text'] = '{}'.format(weather[3])
        wind['text'] = '{}'.format(weather[4])
        description['text']='{}'.format(weather[5])
        weather_image['file']='weather_icons\{}.png'.format(weather[6])
        sunrise['text']='{}'.format(weather[7])
        sunset['text'] = '{}'.format(weather[8])
    else:
        messagebox.showerror("WEATHER APP", "Invalid Entry!!")

searchbox=PhotoImage(file="searchbox.png")
img=Label(image=searchbox)
img.place(x=20,y=20)

city_text=StringVar()
boxtext=Entry(root,justify="center",width=17,font=("poppins",25,"bold"),bg="#404040",border=0,fg="white",textvariable=city_text).place(x=50,y=40)

searchicon=PhotoImage(file="icon.png")
imgicon=Button(image=searchicon,borderwidth=0,cursor="hand2",bg="#404040",activebackground="#404040",activeforeground='white',command=search)
imgicon.place(x=400,y=34)

logoimg=PhotoImage(file="logo.png")
logo=Label(image=logoimg)
logo.place(x=80,y=100)

frameimag=PhotoImage(file="bluebox.png")
frame=Label(image=frameimag)
frame.pack(padx=5,pady=5,side=BOTTOM)

name=Label(root,font=("arial",12,'bold'))
name.place(x=330,y=110)
clock=Label(root,font=("Helvetica",11,'bold'))
clock.place(x=30,y=100)
label1=Label(root,text="WIND",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef").place(x=120,y=400)
label2=Label(root,text="HUMIDITY",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef").place(x=250,y=400)
label3=Label(root,text="DESCRIPTION",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef").place(x=430,y=400)
label4=Label(root,text="PRESSURE",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef").place(x=650,y=400)

temperature=Label(root,text=" ",font=("arial",50,'bold'),fg="#ee666d")
temperature.place(x=330,y=150)
condition=Label(root,text=" ",font=("arial",15,'bold'),fg="#ee666d")
condition.place(x=350,y=250)
wind=Label(text="...",font=("arial",14,'bold'),bg="#1ab5ef")
wind.place(x=125,y=430)
humidity=Label(text="...",font=("arial",14,'bold'),bg="#1ab5ef")
humidity.place(x=280,y=430)
description=Label(text="...",font=("arial",14,'bold'),bg="#1ab5ef")
description.place(x=450,y=430)
pressure=Label(text="...",font=("arial",14,'bold'),bg="#1ab5ef")
pressure.place(x=670,y=430)
weather_image=PhotoImage(file="")
image=Label(root,image=weather_image)
image.place(x=500,y=220)
sunrise_lbl=Label(root,text="Sunrise:",font="arial 8 bold",fg="#000").place(x=650,y=100)
sunrimg=PhotoImage(file="7795612_weather_sunrise_morning_icon.png")
srimg=Label(root,image=sunrimg).place(x=629,y=100)
sunset_lbl=Label(root,text="Sunset:",font="arial 8 bold",fg="#000").place(x=650,y=130)
sunsimg=PhotoImage(file="7795618_weather_sunset_evening_icon.png")
ssimg=Label(root,image=sunsimg).place(x=629,y=130)
sunrise=Label(root,text="",font="arial 8 bold",fg="#000")
sunrise.place(x=710,y=100)
sunset=Label(root,text="",font="arial 8 bold",fg="#000")
sunset.place(x=710,y=130)

root.configure(background="#97FFFF")
root.mainloop()
