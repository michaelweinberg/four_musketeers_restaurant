import requests, json
from seeks import GOOGLE_API_KEY
#import pprint


def delivery_time():
       
    #api GOOGLE_API_KEY is required


  
    # Take source as input
    
    #destination will be a fix point
    destination= input ("Enter Your Delivery Address: ")
  
    # Take destination as input from the database
    #source = input("enter delivery address:")
    source="933 Market St, Tacoma, WA 98402"
  
    # url variable store url 
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?GOOGLE_API_GOOGLE_API_KEY={0}&origins={1}&destinations={2}&mode=driving&language=en-EN&sensor=false".format(GOOGLE_API_KEY,str(source),str(destination))
  
    # Get method of requests module and return response object
     
    req = requests.get(url + 'origins=' + source + '&destinations=' + destination + '&GOOGLE_API_KEY=' + GOOGLE_API_KEY)
    # return json format result
    x = req.json()

    time = req.json()["rows"][0]["elements"][0]["duration"]["text"]

    #prints the time
    print(time)



delivery_time()