#IMPORTING THE REQUIRED MODULES
from tkinter import *
import tkintermapview
from timezonefinder import TimezoneFinder
import timezonefinder, pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from turtle import Turtle, Screen
from datetime import datetime
import pytz
import time


#CREATING FIRST TKINTER WINDOW

root=Tk()
root.geometry("400x400")
bg=PhotoImage(file="/Users/Swetha/Pictures/2 transparent worldtimezones.png")
canvas1=Canvas(root,width=400,height=400)
canvas1.pack(fill="both",expand=True)
canvas1.create_image(0,0,image=bg,anchor="nw")

#CREATING TEXT IN CANVAS
canvas1.create_text(700,300,text="Welcome to The World Analog Clock portal",
                    fill="black",font=("Helvetica","60","bold"))

canvas1.create_text(700,400,text='"See the time from around the world"',
                    fill="black",font=("American Typewriter","40"))



#FUNCTION FOR NEW WINDOW UPON BUTTON CLICK

def openNewWindow():
     
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("900x700")
    newWindow.resizable(True, True)
 
    # A Label widget to show in toplevel
    map_widget=tkintermapview.TkinterMapView(newWindow,width=1400,height=1000)
    map_widget.set_zoom(5)
    map_widget.pack()

    

    #FUNCTION DEF FOR LEFT CLICK EVENT ON MAP
    def left_click_event(coordinates_tuple):
        s=coordinates_tuple

        #Finding latitude and longitude of selected city
        print(s)
        for i in s:
            if s.index(i)==0:
                long=i
            else:
                lati=i
        
        #int to str type conversion 
        lati=str(lati)
        long=str(long)

        #initialize Nominatim API
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(long+","+lati)  #long in lat place
        address = location.raw['address']
         
        #traverse the data to get exact address and city name
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        code = address.get('country_code')
        zipcode = address.get('postcode')
        print('City : ', city)
        print('State : ', state)
        print('Country : ', country)
        print('Zip Code : ', zipcode) #type is str for all
        
        #Finding timezone from the address selected
        geolocator = Nominatim(user_agent="geoapiExercises")
        lad = city
        print("Location address:", lad)
        #getting Latitude and Longitude
        location = geolocator.geocode(lad)
        # pass the Latitude and Longitude into a timezone_at() function and it returns timezone
        obj = TimezoneFinder()
        #final timezone of selected city is stored in result variable
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        print(type(result))
        print("Time Zone : ", result)

        #TURTLE MODULE SETUP FOR ANALOG CLOCK
        wn=Screen()
        wn.bgcolor("black")
        wn.setup(width=1000,height=800)
        wn.title("world analog clock")
        wn.tracer(0)
        

        #creating drawing pen
        pen=Turtle()
        pen.hideturtle()
        pen.speed(10)
        pen.pensize(3)

        #function def for clock drawing
        def draw_clock(h,m,s,pen):
            #Drawing a circle
            pen.penup()
            pen.goto(0,350)
            pen.setheading(180)
            pen.color("green")
            pen.pendown()
            pen.circle(350)

            #Drawing the lines
            pen.penup()
            pen.goto(0,0)
            pen.setheading(90)
            for i in range(12):
                pen.forward(320)
                pen.pendown()
                pen.fd(30)
                pen.up()
                pen.goto(0,0)
                pen.rt(30)

            #Draw the hour hand
            pen.penup()
            pen.goto(0,0)
            pen.color("white")
            pen.pensize(7)
            pen.setheading(90)
            angle=(h/12)*360
            pen.rt(angle)
            pen.pendown()
            pen.fd(100)

            #Draw the minute hand
            pen.penup()
            pen.goto(0,0)
            pen.color("blue")
            pen.pensize(5)
            pen.setheading(90)
            angle=(m/60)*360
            pen.rt(angle)
            pen.pendown()
            pen.fd(200)

            #Draw the second hand
            pen.penup()
            pen.goto(0,0)
            pen.color("gold")
            pen.setheading(90)
            angle=(s/60)*360
            pen.rt(angle)
            pen.pendown()
            pen.fd(300)

       
        #LOOP FOR CLOCK TICKING WITH UPDATION BASED ON CURRENT TIME
        
        while True:

            #extracting local time in selected country
            #from timezone details
            #TIME FROM TIMEZONE
            #USE OF datetime module and pytz module
            
            
            countryTz = pytz.timezone(result)
            timeInCountry = datetime.now(countryTz)
            currentTimeInCountry = timeInCountry.strftime("%H:%M:%S")
            hour=timeInCountry.strftime("%H")
            minute=timeInCountry.strftime("%M")
            second=timeInCountry.strftime("%S")
            print(currentTimeInCountry)

            h=int(timeInCountry.strftime("%H"))
            m=int(timeInCountry.strftime("%M"))
            s=int(timeInCountry.strftime("%s"))

            #calling the function to draw the analog clock
            draw_clock(h,m,s,pen)
            wn.update()
            time.sleep(1)
            
            pen.clear()
            
        
            

        wn.mainloop()

    #ACTIVATING LEFTCLICK ON MAP
    map_widget.add_left_click_map_command(left_click_event)
    newWindow.mainloop()
    
#COMPILING ALL THE FUNCTIONS INTO THE "GO TO MAP" BUTTON   
buttontomap=Button(root,text="Go to World Map",font=("American Typewriter","25"),bg="pink",command=openNewWindow)
buttontomap_canvas=canvas1.create_window(600,500,anchor="nw",window=buttontomap)
root.mainloop()






