from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder #To find timezone of a place
from datetime import *
import requests
from PIL import Image, ImageTk
from geopy.geocoders import *
import pytz

def findValue(num_day):
   mintemp=[]
   maxtemp=[]
   desc=[]
   calc_date=datetime.fromtimestamp(date_today)+timedelta(days=num_day)
   
   for i in json_data['list']:
         if i['dt_txt'][:10]==str(calc_date)[:10]:
            mintemp+=[i['main']['temp_min']]
            maxtemp+=[i['main']['temp_max']]
            desc+=[i['weather'][0]['description']]
   return min(mintemp),max(maxtemp),max(desc,key=desc.count),calc_date.strftime("%a")
##
def hourly_Value():
   value=[]
   DATE=datetime.today()
   DATE=DATE.strftime('%Y-%m-%d')
   for DICT in json_data['list']:
      if str(DATE) in DICT['dt_txt']:
         value+=[(DICT['dt_txt'][11:16],DICT['weather'][0]['icon'],str(int(round(DICT['main']['temp'],0)))+'°')]
   return value[:7]
   

def getWeather():
   try:
      city=text_search.get()
      geolocator=Nominatim(user_agent="Project")
      location=geolocator.geocode(city)
      obj=TimezoneFinder()
      result=obj.timezone_at(lng=location.longitude,lat=location.latitude)
      city_name.config(text=city.title())
      lat_long.config(text=f"Latitude: {round(location.latitude,4)}°N         Longitude: {round(location.longitude,4)}°E")
      
      home=pytz.timezone(result)
      local_time=datetime.now(home)
      current_time=local_time.strftime("%I:%M %p")
      clock.config(text=current_time)

      #Weather
      file=open("API Key.txt")
      key=file.read()
      api="https://api.openweathermap.org/data/2.5/forecast?lat="+str(location.latitude)+"&lon="+str(location.longitude)+"&units=metric&appid="+key
      api_2="https://air-quality-api.open-meteo.com/v1/air-quality?latitude="+str(location.latitude)+"&longitude="+str(location.longitude)+"&current=us_aqi"     #api_2="http://api.openweathermap.org/data/2.5/air_pollution?lat="+str(location.latitude)+"&lon="+str(location.longitude)+"&appid="+key
      json_data_2=requests.get(api_2).json()
      #print(json_data_2)
      global json_data 
      json_data=requests.get(api).json()
      #print(json_data)

      global date_today 
      date_today=json_data['list'][0]['dt']

      #current_data
      temp=json_data['list'][0]['main']['temp']
      desc_icon=json_data['list'][0]['weather'][0]['icon']
      desc=json_data['list'][0]['weather'][0]['description']

      value=findValue(0)
      #current_display
      current_temp.config(text=str(int(round(temp,0)))+'°')
      current_desc.config(text=desc.title())

      max_min_temp.config(text=str(int(round(value[0],0)))+'° / '+str(int(round(value[1],0)))+'°')

      image = Image.open(desc_icon+'.png')
      resize_image = image.resize((100, 100))
      curr_desc=ImageTk.PhotoImage(resize_image)
      panel_curr.photo=curr_desc
      panel_curr.config(image=curr_desc)

      feelslike_temp.config(text="| Feels like "+str(int(round(json_data['list'][0]['main']['feels_like'],0)))+'°')

      aqi=json_data_2['current']['us_aqi']

      if aqi<=50:
         air_quality.config(text="Air quality: "+str(aqi)+" - Good")
      elif 51<=aqi<=100:
         air_quality.config(text="Air quality: "+str(aqi)+" - Moderate")
      elif 101<=aqi<=150:
         air_quality.config(text="Air quality: "+str(aqi)+" - Poor")
      elif 151<=aqi<=200:
         air_quality.config(text="Air quality: "+str(aqi)+" - Very poor")
      elif 201<=aqi<=300:
         air_quality.config(text="Air quality: "+str(aqi)+" - Unhealthy")
      elif 301<=aqi<=500:
         air_quality.config(text="Air quality: "+str(aqi)+" - Very unhealthy")
      elif aqi>=501:
         air_quality.config(text="Air quality: "+str(aqi)+" - Hazardous")

      ##air_conditions

      humidity.config(text=str(json_data['list'][0]['main']['humidity'])+' %')
      cloud.config(text=str(json_data['list'][0]['clouds']['all'])+' %')
      wind.config(text=str(json_data['list'][0]['wind']['speed'])+' m/s')
      pressure.config(text=str(json_data['list'][0]['main']['pressure'])+' hPa')

      #weekly_forecast_display
      #DAY 1
      min_temp1,max_temp1,desc1,day1=findValue(1)
      
      day1_disp.config(text=day1) 
      desc1_disp.config(text=desc1.title())
      temp1_disp.config(text=str(int(round(min_temp1,0)))+'/'+str(int(round(max_temp1,0))))

      day1_icon=PhotoImage(file=icon[desc1]+".png")
      panel1.photo = day1_icon
      panel1.config(image=day1_icon)      

      #DAY 2
      min_temp2,max_temp2,desc2,day2=findValue(2)
      
      day2_disp.config(text=day2)
      desc2_disp.config(text=desc2.title())
      temp2_disp.config(text=str(int(round(min_temp2,0)))+'/'+str(int(round(max_temp2,0))))

      day2_icon=PhotoImage(file=icon[desc2]+".png")
      panel2.photo = day2_icon
      panel2.config(image=day2_icon)

      #DAY 3
      min_temp3,max_temp3,desc3,day3=findValue(3)

      day3_disp.config(text=day3)
      desc3_disp.config(text=desc3.title())
      temp3_disp.config(text=str(int(round(min_temp3,0)))+'/'+str(int(round(max_temp3,0))))

      day3_icon=PhotoImage(file=icon[desc3]+".png")
      panel3.photo = day3_icon
      panel3.config(image=day3_icon)
      #DAY 4
      min_temp4,max_temp4,desc4,day4=findValue(4)

      day4_disp.config(text=day4)
      desc4_disp.config(text=desc4.title())
      temp4_disp.config(text=str(int(round(min_temp4,0)))+'/'+str(int(round(max_temp4,0))))

      day4_icon=PhotoImage(file=icon[desc4]+".png")
      panel4.photo = day4_icon
      panel4.config(image=day4_icon)
      #DAY 5
      min_temp5,max_temp5,desc5,day5=findValue(5)

      day5_disp.config(text=day5)
      desc5_disp.config(text=desc5.title())
      temp5_disp.config(text=str(int(round(min_temp5,0)))+'/'+str(int(round(max_temp5,0))))

      day5_icon=PhotoImage(file=icon[desc5]+".png")
      panel5.photo = day5_icon
      panel5.config(image=day5_icon)
      
      data=hourly_Value()
      try:
         ######HOUR1######
         hr1_disp.config(text=data[0][0])
         temp_hr1_disp.config(text=data[0][2])

         hr1_icon=PhotoImage(file=data[0][1]+".png")
         panel_hr1.photo = hr1_icon
         panel_hr1.config(image=hr1_icon)
         ######HOUR2######
         hr2_disp.config(text=data[1][0])
         temp_hr2_disp.config(text=data[1][2])

         hr2_icon=PhotoImage(file=data[1][1]+".png")
         panel_hr2.photo = hr2_icon
         panel_hr2.config(image=hr2_icon)
         ######HOUR3######
         hr3_disp.config(text=data[2][0])
         temp_hr3_disp.config(text=data[2][2])

         hr3_icon=PhotoImage(file=data[2][1]+".png")
         panel_hr3.photo = hr3_icon
         panel_hr3.config(image=hr3_icon)
         ######HOUR4######
         hr4_disp.config(text=data[3][0])
         temp_hr4_disp.config(text=data[3][2])

         hr4_icon=PhotoImage(file=data[3][1]+".png")
         panel_hr4.photo = hr4_icon
         panel_hr4.config(image=hr4_icon)
         ######HOUR5######
         hr5_disp.config(text=data[4][0])
         temp_hr5_disp.config(text=data[4][2])

         hr5_icon=PhotoImage(file=data[4][1]+".png")
         panel_hr5.photo = hr5_icon
         panel_hr5.config(image=hr5_icon)
         ######HOUR6######
         hr6_disp.config(text=data[5][0])
         temp_hr6_disp.config(text=data[5][2])

         hr6_icon=PhotoImage(file=data[5][1]+".png")
         panel_hr6.photo = hr6_icon
         panel_hr6.config(image=hr6_icon)

         ######HOUR7######
         hr7_disp.config(text=data[6][0])
         temp_hr7_disp.config(text=data[6][2])

         hr7_icon=PhotoImage(file=data[6][1]+".png")
         panel_hr7.photo = hr7_icon
         panel_hr7.config(image=hr7_icon)
      except IndexError:
         pass

   except AttributeError:
      tk.messagebox.showwarning(title="Invalid", message="Enter a valid city.")
    

root=Tk()
root.title("WeatherCast")
root.geometry("950x705+250+-5")
root.configure(bg="#0b131e")
root.resizable(False,False)
ICON = PhotoImage(file='Logo.png')
root.iconphoto(False, ICON)

background_image = tk.PhotoImage(file="Weather App UI.png")
myimage = tk.Label(root, image=background_image, anchor=CENTER)
myimage.pack()
myimage.place(x=0, y=0)
myimage.config(bd=0)

#Search box
def temp_text(e):
   text_search.delete(0,"end")

text_search=tk.Entry(root,justify="left",width=60,font=('Calibri',12),bg='#202b3b',border=0,fg='#7e8592')
text_search.place(x=20,y=25)
text_search.insert(0,"Search for cities")
text_search.bind("<FocusIn>", temp_text)
#text_search.focus() #Automatically puts cursor on search bar

search_icon=PhotoImage(file="search_icon2.png")
search_button=Button(image=search_icon,height=35,width=35,borderwidth=0,cursor="hand2",bg="#202b3b",activebackground="#202b3b",command=getWeather)
search_button.place(x=540,y=16)

#Label
city_name=Label(root,font=('Calibri',28,'bold'),bg='#0b131e',fg='#dde0e6')
city_name.place(x=55,y=80)

air_con=Label(root,text='AIR CONDITIONS',font=('Calibri',10,'bold'),bg='#202b3b',fg='#7e8592')
air_con.place(x=35,y=500)

forecast=Label(root,text="TODAY'S FORECAST",font=('Calibri',10,'bold'),bg='#202b3b',fg='#7e8592')
forecast.place(x=35,y=300)

week_forcast=Label(root,text="5-DAY FORECAST",font=('Calibri',10,'bold'),bg='#202b3b',fg='#7e8592')
week_forcast.place(x=635,y=165)

air_humidity=Label(root,text='Humidity',font=('Calibri',13,'bold'),bg='#202b3b',fg='#7e8592')
air_humidity.place(x=35,y=530)

air_cloud=Label(root,text='Cloudiness',font=('Calibri',13,'bold'),bg='#202b3b',fg='#7e8592')
air_cloud.place(x=330,y=530)

air_wind=Label(root,text='Wind speed',font=('Calibri',13,'bold'),bg='#202b3b',fg='#7e8592')
air_wind.place(x=35,y=605)

air_pressure=Label(root,text='Air pressure',font=('Calibri',13,'bold'),bg='#202b3b',fg='#7e8592')
air_pressure.place(x=330,y=605)


current_temp=Label(root,font=('Calibri',43),bg='#0b131e',fg='#dde0e6')
current_temp.place(x=55,y=135)

current_icon=PhotoImage()
panel_curr=tk.Label(root,bg='#0b131e')
panel_curr.place(x=450,y=80)

current_desc=Label(root,font=('Calibri',13,'bold'),bg='#0b131e',fg='#dde0e6')
current_desc.place(x=460,y=185)

max_min_temp=Label(root,font=('Calibri',13,'bold'),bg='#0b131e',fg='#dde0e6')
max_min_temp.place(x=460,y=210)

clock=Label(root,font=('Calibri',30,'bold'),bg='#202b3b',fg='#dde0e6')
clock.place(x=690,y=95)

feelslike_temp=Label(root,font=('Calibri',13,'bold'),bg='#0b131e',fg='#dde0e6')
feelslike_temp.place(x=125,y=172)

lat_long=Label(root,font=('Calibri',10,'bold'),bg='#202b3b',fg='#7e8592')
lat_long.place(x=639,y=635)

air_quality=Label(root,font=('Calibri',13,'bold'),bg='#0b131e',fg='#dde0e6')
air_quality.place(x=55,y=210)

########AIR CONDITIONS#######
humidity=Label(root,font=('Calibri',14,'bold'),bg='#202b3b',fg='#dde0e6')
humidity.place(x=37,y=560)

cloud=Label(root,font=('Calibri',14,'bold'),bg='#202b3b',fg='#dde0e6')
cloud.place(x=332,y=560)

wind=Label(root,font=('Calibri',14,'bold'),bg='#202b3b',fg='#dde0e6')
wind.place(x=37,y=635)

pressure=Label(root,font=('Calibri',14,'bold'),bg='#202b3b',fg='#dde0e6')
pressure.place(x=332,y=635)

######ICONS######
thunderstorm={'thunderstorm with light rain':'11d','thunderstorm with rain':'11d','thunderstorm with heavy rain':'11d','light thunderstorm':'11d','thunderstorm':'11d','heavy thunderstorm':'11d','ragged thunderstorm':'11d','thunderstorm with light drizzle':'11d','thunderstorm with drizzle':'11d','thunderstorm with heavy drizzle':'11d'}
drizzle={'light intensity drizzle':'09d','Drizzle	drizzle':'09d','Drizzle	heavy intensity drizzle':'09d','Drizzle	light intensity drizzle rain':'09d','Drizzle	drizzle rain':'09d','Drizzle	heavy intensity drizzle rain':'09d','Drizzle	shower rain and drizzle':'09d','Drizzle	heavy shower rain and drizzle':'09d','Drizzle	shower drizzle':'09d'}
rain={'light rain':'10d','moderate rain':'10d','heavy intensity rain	':'10d','very heavy rain':'10d','extreme rain':'10d','freezing rain':'10d','light intensity shower rain':'10d','shower rain':'10d','heavy intensity shower rain':'10d','ragged shower rain':'10d',}
clouds={'few clouds':'02d','scattered clouds':'03d','broken clouds':'04d','overcast clouds':'04d','clear sky':'01d'}
atmosphere={'mist':'50d','smoke':'50d','haze':'50d','sand/dust whirls':'50d','fog':'50d','sand':'50d','dust':'50d','volcanic ash':'50d','squalls':'50d','tornado':'50d'}
snow={'light snow':'13d','snow':'13d','heavy snow':'13d','sleet':'13d','light shower sleet':'13d','shower sleet':'13d','light rain and snow':'13d','rain and snow':'13d','light shower snow':'13d','shower snow':'13d','heavy shower snow':'13d',}
icon={}
icon.update(thunderstorm)
icon.update(drizzle)
icon.update(rain)
icon.update(clouds)
icon.update(atmosphere)
icon.update(snow)

######DAY1#######
day1_disp=Label(root,font=('Calibri',12),bg='#202b3b',fg='#7e8592')
day1_disp.place(x=635,y=230)
      
desc1_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#dde0e6')
desc1_disp.place(x=740,y=230)
      
temp1_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
temp1_disp.place(x=862,y=230)

img1=PhotoImage()
panel1 = tk.Label(root,bg='#202b3b')
panel1.place(x=671,y=210)

######DAY2######
day2_disp=Label(root,font=('Calibri',12),bg='#202b3b',fg='#7e8592')
day2_disp.place(x=635,y=312)

desc2_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#dde0e6')
desc2_disp.place(x=740,y=312)

temp2_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
temp2_disp.place(x=862,y=312)

img2=PhotoImage()
panel2 = tk.Label(root,bg='#202b3b')
panel2.place(x=671,y=292)

######DAY3######
day3_disp=Label(root,font=('Calibri',12),bg='#202b3b',fg='#7e8592')
day3_disp.place(x=635,y=393)

desc3_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#dde0e6')
desc3_disp.place(x=740,y=393)

temp3_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
temp3_disp.place(x=862,y=393)

img3=PhotoImage()
panel3 = tk.Label(root,bg='#202b3b')
panel3.place(x=671,y=373)

######DAY4######
day4_disp=Label(root,font=('Calibri',12),bg='#202b3b',fg='#7e8592')
day4_disp.place(x=635,y=468)
      
desc4_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#dde0e6')
desc4_disp.place(x=740,y=468)
      
temp4_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
temp4_disp.place(x=862,y=468)

img4=PhotoImage()
panel4 = tk.Label(root,bg='#202b3b')
panel4.place(x=671,y=448)

######DAY5######
day5_disp=Label(root,font=('Calibri',12),bg='#202b3b',fg='#7e8592')
day5_disp.place(x=635,y=548)

desc5_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#dde0e6')
desc5_disp.place(x=740,y=548)

temp5_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
temp5_disp.place(x=862,y=548)

img5=PhotoImage()
panel5 = tk.Label(root,bg='#202b3b')
panel5.place(x=671,y=528)


######HOUR1######
hr1_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
hr1_disp.place(x=40,y=335)

img_hr1=PhotoImage()
panel_hr1 = tk.Label(root,bg='#202b3b')
panel_hr1.place(x=30,y=360)

temp_hr1_disp=Label(root,font=('Calibri',16,'bold'),bg='#202b3b',fg='#dde0e6')
temp_hr1_disp.place(x=42,y=425)

######HOUR2######
hr2_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
hr2_disp.place(x=120,y=335)

img_hr2=PhotoImage()
panel_hr2 = tk.Label(root,bg='#202b3b')
panel_hr2.place(x=110,y=360)

temp_hr2_disp=Label(root,font=('Calibri',16,'bold'),bg='#202b3b',fg='#dde0e6')
temp_hr2_disp.place(x=122,y=425)
######HOUR3######
hr3_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
hr3_disp.place(x=200,y=335)

img_hr3=PhotoImage()
panel_hr3 = tk.Label(root,bg='#202b3b')
panel_hr3.place(x=190,y=360)

temp_hr3_disp=Label(root,font=('Calibri',16,'bold'),bg='#202b3b',fg='#dde0e6')
temp_hr3_disp.place(x=202,y=425)
######HOUR4######
hr4_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
hr4_disp.place(x=280,y=335)

img_hr4=PhotoImage()
panel_hr4 = tk.Label(root,bg='#202b3b')
panel_hr4.place(x=270,y=360)

temp_hr4_disp=Label(root,font=('Calibri',16,'bold'),bg='#202b3b',fg='#dde0e6')
temp_hr4_disp.place(x=282,y=425)
######HOUR5######
hr5_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
hr5_disp.place(x=360,y=335)

img_hr5=PhotoImage()
panel_hr5 = tk.Label(root,bg='#202b3b')
panel_hr5.place(x=350,y=360)

temp_hr5_disp=Label(root,font=('Calibri',16,'bold'),bg='#202b3b',fg='#dde0e6')
temp_hr5_disp.place(x=362,y=425)
######HOUR6######
hr6_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
hr6_disp.place(x=440,y=335)

img_hr6=PhotoImage()
panel_hr6 = tk.Label(root,bg='#202b3b')
panel_hr6.place(x=430,y=360)

temp_hr6_disp=Label(root,font=('Calibri',16,'bold'),bg='#202b3b',fg='#dde0e6')
temp_hr6_disp.place(x=442,y=425)

######HOUR7######
hr7_disp=Label(root,font=('Calibri',12,'bold'),bg='#202b3b',fg='#7e8592')
hr7_disp.place(x=520,y=335)

img_hr7=PhotoImage()
panel_hr7 = tk.Label(root,bg='#202b3b')
panel_hr7.place(x=510,y=360)

temp_hr7_disp=Label(root,font=('Calibri',16,'bold'),bg='#202b3b',fg='#dde0e6')
temp_hr7_disp.place(x=522,y=425)


root.mainloop()
