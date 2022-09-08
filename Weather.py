from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

#omw = OMW(API KEY)
mgr = owm.weather_manager()



def get_temp(location):
    
    observation = mgr.weather_at_place(location)
    w = observation.weather
    temp = w.temperature('fahrenheit')  
    return temp

  