from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

owm = OWM('d280c53fd2ba6942f8ad96efb30f7624')
mgr = owm.weather_manager()



def get_temp(location):
    
    observation = mgr.weather_at_place(location)
    w = observation.weather
    temp = w.temperature('fahrenheit')  
    return temp

  