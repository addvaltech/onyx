import serial
import requests
import json
import pynmea2  # pip install pynmea2
import time
import datetime
import threading # timer thread
import logging
import itertools
import sys
requests.packages.urllib3.disable_warnings() 

import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P8_8", GPIO.OUT)
GPIO.output("P8_8", GPIO.HIGH)

# local files
import log

login_user = 'admin'
password = 'm@nufacturing'
url = 'https://192.168.1.1/auth/' 
headers = {'content-type' : 'application/json'}
    
# creates a Logger instance for debugging 
logging.basicConfig(filename='/var/lib/cloud9/myprojects/onyx/onyx.log',level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s: %(message)s',)
                    
signalstrength = 0.1
#   Declare latitude and longitude
latitude = 0.0
longitude = 0.0
altitude = 0.0



""" High-level API classes for LEDs settings """
""" Main class for interacting with an LEDs """
class setLed(object):
    def __init__(self):
        GPIO.setup("P8_8", GPIO.OUT)
        GPIO.setup("P8_9", GPIO.OUT)
        GPIO.setup("P8_10", GPIO.OUT)
        GPIO.setup("P8_11", GPIO.OUT)
        GPIO.setup("P8_12", GPIO.OUT)
        GPIO.output("P8_8", GPIO.LOW)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)    

    def led0(self):
        GPIO.output("P8_8", GPIO.LOW)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)  

    def led1(self):
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)  

    def led2(self):
        GPIO.output("P8_8", GPIO.LOW)
        GPIO.output("P8_9", GPIO.HIGH)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)  
        
    def led3(self):
        GPIO.output("P8_8", GPIO.LOW)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.HIGH)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)  
        
    def led4(self):
        GPIO.output("P8_8", GPIO.LOW)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.HIGH)
        GPIO.output("P8_12", GPIO.LOW)  

    def led5(self):
        GPIO.output("P8_8", GPIO.LOW)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.HIGH)          
        
    def close(self):
        GPIO.cleanup()
        

""" High-level API classes for BRM signal strength LEDs """
""" Main class for interacting with an LEDs """
class signalBar(object):
 #   global ival
    def __init__(self):
        global ledState
        GPIO.setup("P8_8", GPIO.OUT)
        GPIO.setup("P8_9", GPIO.OUT)
        GPIO.setup("P8_10", GPIO.OUT)
        GPIO.setup("P8_11", GPIO.OUT)
        GPIO.setup("P8_12", GPIO.OUT)
        GPIO.output("P8_8", GPIO.LOW)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)    
        ledState = False

        
    def bar00(self):
        GPIO.output("P8_8", GPIO.LOW)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)  

    def bar01(self):
        global ledState
        ledState = not ledState
        GPIO.output("P8_8", ledState)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)  
        
    def bar11(self):
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.LOW)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)    \

    def bar12(self):
        global ledState
        ledState = not ledState        
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", ledState)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)    

    def bar22(self):
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.HIGH)
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)    


    def bar23(self):
        global ledState
        ledState = not ledState           
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.HIGH)
        GPIO.output("P8_10", ledState)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)  
        
    def bar33(self):
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.HIGH)
        GPIO.output("P8_10", GPIO.HIGH)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)    


    def bar34(self):
        global ledState
        ledState = not ledState          
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.HIGH)
        GPIO.output("P8_10", ledState)
        GPIO.output("P8_11", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)   
        
    def bar44(self):
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.HIGH)
        GPIO.output("P8_10", GPIO.HIGH)
        GPIO.output("P8_11", GPIO.HIGH)
        GPIO.output("P8_12", GPIO.LOW)            
        
    def bar45(self):
        global ledState
        ledState = not ledState             
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.HIGH)
        GPIO.output("P8_10", GPIO.HIGH)
        GPIO.output("P8_11", GPIO.HIGH)
        GPIO.output("P8_12", ledState)   
        
    def bar55(self):
        GPIO.output("P8_8", GPIO.HIGH)
        GPIO.output("P8_9", GPIO.HIGH)
        GPIO.output("P8_10", GPIO.HIGH)
        GPIO.output("P8_11", GPIO.HIGH)
        GPIO.output("P8_12", GPIO.HIGH)      
        
    def barxx(self):
        global ledState
        ledState = not ledState             
        GPIO.output("P8_8", ledState)
        GPIO.output("P8_9", ledState)
        GPIO.output("P8_10", ledState)
        GPIO.output("P8_11", ledState)
        GPIO.output("P8_12", ledState)   
        
    def close(self):
        GPIO.cleanup()

""" Main class for for periodic timer """
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def f(s):
    logging.debug('thread function running')
#    s.bar3()
    return


"""
Desc:   Function that start LEDs light up pattern
Input:  none
Output: none
"""
def start_leds():
    setled = setLed()
    print 'Start LEDs sequence...'
#    for led in [setled.led0,setled.led1,setled.led2,setled.led3,setled.led4,setled.led5]:
#        led
#        print led
#        time.sleep(0.2)


    setled.led0()
    time.sleep(0.15) 
    setled.led1()
    time.sleep(0.15) 
    setled.led2()
    time.sleep(0.15) 
    setled.led3()
    time.sleep(0.15)     
    setled.led4()
    time.sleep(0.15)     
    setled.led5()
    time.sleep(0.15) 
    
    return



"""
Desc:   Set LEDs bar according to BRM signal strength
Global: Updates global variables DEVICE_ID and URL
Input:  sgnalStrength class
Output: Displays output LEDS to let user know the signal 
        strength level (0-5)
"""
def signalStrength(s):
    global signalstrength
    #print datetime.datetime.now()
    sig = float(signalstrength)
    print sig
    
    if sig > 55.0:
        s.bar55()
    elif sig > 53.25:
        s.bar45()
    elif sig > 52.25:
        s.bar44()
    elif sig > 51.25:
        s.bar34()
    elif sig > 50.25:
        s.bar33()
    elif sig > 49.25:
        s.bar23()
    elif sig > 48.25:
        s.bar22()
    elif sig > 47.25:
        s.bar12()
    elif sig > 41.0:
        s.bar11()
    elif sig > 0.0:
        s.bar01()   
        print "Signal LOW!" 
    elif sig == 0.0:
        s.bar01()   
        print "Signal ZERO!"         
    elif sig < 0.0:
        s.barxx()   
        print "Signal failed!"           
    else:
        s.bar01() #s.barxx()

"""
Desc:   Get GeoCode from Google MAP API for testing purpose
Global: none
Input:  location in string (i.e Tai Seng Singapore)
Output: GPS latitude, longitude, formatted_address
"""
def getGeoCode(location):
    # api-endpoint
    URL = "http://maps.googleapis.com/maps/api/geocode/json"
     
    # location given here
    #location = "tai seng mrt"
     
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'address':location}
     
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
     
    # extracting data in json format
    data = r.json()
     
     
    # extracting latitude, longitude and formatted address 
    # of the first matching location
    latitude = data['results'][0]['geometry']['location']['lat']
    longitude = data['results'][0]['geometry']['location']['lng']
    formatted_address = data['results'][0]['formatted_address']
     
    # printing the output
    print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
          %(latitude, longitude,formatted_address))  
    
    return data

""" Main class for for BRM RestFUL API """
class MyRestFul():
   
    def __init__(self):
        self.s = requests.Session()
        self.s.auth = (login_user, password)
    
    def get(self, rest):
        req = self.s.get(url+rest,auth=(login_user, password), verify=False) 
        return req
    def post(self, rest, payload):
        req = self.s.post(url+rest,auth=(login_user, password), verify=False, data=payload, headers={'Content-Type': 'application/json'})
        return req
    def put(self, rest, payload):
        req = self.s.put(url+rest,auth=(login_user, password), verify=False, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        return req        
    def logout(self):
#        req = self.s.get(url+"v1/config/setting/serial_number",auth=(login_user, password), verify=False) 
        self.s.close()
#        return resp
 

"""
Desc:   A threaded callback function to run in another thread when events are detected  
Input:  channel
""" 
# Define a threaded callback function to run in another thread when events are detected  
def gpio_8_7_callback(channel):  
    #if GPIO.input('P8_7'):     # if port P8_7 == 1  
    logging.info('Exit Antenna-pointing triggered.')
    if GPIO.event_detected("P8_7"):
        log.info("Rising edge detected on " + channel)
    else:                  # if port P8_7 != 1  
        log.info("Falling edge detected on " + channel)
    t1.stop()        
    t0.start()

    
    if signalstrength < 0.0:
        log.err('Signal not available!')
#    else:
#        start_leds()
    

    logging.debug('AT Cmd: AT_IPOINT=1')
    at_data = {'command' : 'AT_IPOINT=1'} # Exit antenna-poiting At-cmd (AT_IPOINT)
    at_data = json.dumps(at_data)
    log.infog(at_data)
    req = requests.post('https://192.168.1.1/auth/v1/at',auth=('admin','m@nufacturing'), verify=False, data=at_data,headers={'Content-Type': 'application/json'})
    if req.status_code == 200:
        d = json.loads(req.text)
        at_resp = d['response']
        log.infog('AT:' + at_resp)
        logging.debug('AT Resp: ' + at_resp)
    else:
        log.err('AT command failure!')
        print (req.text)  
        logging.warning('AT command failure: '+ req.text)
  
    t0.stop()
         
    t1.start()  


def connected_to_brm(url='https://192.168.1.1/auth/v1/device/firmware/status', timeout=3):
    try:
        req = requests.get(url, auth=('admin','m@nufacturing'), verify=False, timeout=timeout)
        print req.text
        # HTTP errors are not raised by default, this statement does that
        req.raise_for_status()
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
        e.response.status_code))
        logging.warning('Checking internet connection failed.')
    except requests.ConnectionError:
        print("No internet connection available.")
        logging.warning('BRM Websocket not reachable.')
    return False
    
"""
Main
"""
def main():
    global skywire, latitude, longitude, ledState, signalstrength, t1
    url = ""
    device_id = ""
    fw_ver = ""
    user = "admin"
    password = "m@nufacturing"
    
    url = 'https://192.168.1.1/auth/'
    brm_err_cnt = 5

    logging.info('ONYX main started.')

    t0 = RepeatedTimer(2, start_leds)
    t0.start()
#   start_leds()   
#    time.sleep(20)
    
    for i in range(0, 5, 1):
        print("Waiting BRM connection...")
        if connected_to_brm():
            break

    check_usim = True
    set_ant_flag = True
    s = requests.Session()
    s.auth = (user, password)
   
    t0.stop()
   
    try:
        # initial BRM websocket checking
        response = s.get(url,verify=False) 
        print response.status_code        
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(e.response.status_code))
        logging.warning('No internet connection available.')
    except requests.ConnectionError:
        print("No internet connection available.")
        logging.error('Initial BRM websocket checking error. \nExit Onyx main!')
        sys.exit(1)

     
#    start_leds() 


#    t0 = RepeatedTimer(1, start_leds,sb)
#    t0.start()
#    req = requests.get(url,auth=(user, password), verify=False)    
#    s = requests.Session()
#    s.get(url,auth=('admin', 'm@nufacturing'), cert=False, verify=False)    

    #r = requests.get(url, auth=('admin', 'm@nufacturing'), cert=False, verify=False)    
    # r = requests.get('https://192.168.1.1/auth/', auth=('admin', 'm@nufacturing'))
#    print req.status_code




    log.info('== BRM INFORMATION ==')
    req = s.get(url+"v1/config/setting/serial_number",auth=('admin', 'm@nufacturing'), verify=False) 
    print 'Serial number :' + req.text
    logging.info('Serial number :' + req.text)
    req = s.get(url+"v1/device/temp",auth=('admin', 'm@nufacturing'), verify=False) 
    data = json.loads(req.text)
    print 'BRM Temperature :' , data['brmTemp'], 'Celcius'
    logging.info('Temperature :' + req.text)
    
#    geocode = getGeoCode('tai seng mrt')
    
#    latitude = geocode['results'][0]['geometry']['location']['lat']
#    longitude = geocode['results'][0]['geometry']['location']['lng']
#    print("Latitude:%s\nLongitude:%s\n"%(latitude, longitude))  


    req = s.get(url+"v1/device/signalstrength",auth=('admin', 'm@nufacturing'), verify=False) 
    if req.status_code == 200:
        data = json.loads(req.text)
        print 'Signal Strength :' , data, 'dBHz'
    else:
        log.err('Signal strength request failed!')
        print (req.status_code)


    rest=MyRestFul()
    r = rest.get('v1/config/setting/serial_number')
    print r.text
 
    r = rest.get('v1/device/temp')
    print ' temperature: ' + r.text

    r = rest.get('v1/device/id')
    print 'id.: ' + r.text 

#    r = rest.get('v1/device/firmware')
#    #r.text = r.text.encode('utf-8').strip()
#    print 'firmware ver.: ' + r.text

    r = rest.get('v1/device/bist')
    print 'BIST: ' + r.text

    r = rest.get('v1/config')
    print 'configuration: ' + r.text
    log.info('== BRM INFORMATION ==')
    logging.info(r.text)
        
    #rest.logout()
    
    # Get antenna pointing status (bypass antenna pointing)   
    req = rest.get('v1/device/antenna_pointing')
    if req.status_code == 200:
        data = json.loads(req.text)
        ant_pointing = data['enabled']
        print ant_pointing
    else:
        log.err('antenna_pointing!')
        print (req.text)

    
#    time.sleep(5)    


    #   Setup GPS
#    setupAGPS()

    # Create push button for BRM exit antenna pointing
    GPIO.setup("P8_7", GPIO.IN)
    GPIO.add_event_detect("P8_7", GPIO.RISING, callback=gpio_8_7_callback)
    
    #GPIO.wait_for_edge('P8_7', GPIO.RISING)
    
    #your amazing code here
    #detect wherever:
    #if GPIO.event_detected("P8_7"):
    #    print "event detected!"    

    ledState = False
    
######### timer ##############
    sb = signalBar()
    t1 = RepeatedTimer(1, signalStrength, sb)
    logging.debug('Signal strength timer started...')
    t1.start()
    
#   t0 = RepeatedTimer(1, start_leds)
#    t0.start()
#    t2.start()
#    logging.debug('waiting before canceling %s', t2.getName())
#    time.sleep(2)
#    logging.debug('canceling %s', t2.getName())
#    print 'before cancel t2.is_alive() = ', t2.is_alive()
#    t2.cancel()
#    time.sleep(1)
#    print 'after cancel t2.is_alive() = ', t2.is_alive()

#    t1.join()
#    t2.join()
#    t1.stop()

    logging.debug('done')
########################################    

    print("Main loop...\r\n")
    while True:

        try:
            # TODO: write code...
     
            req = rest.get('v1/device/signalstrength')
            if req.status_code == 200:
                data = json.loads(req.text)
    #            print data
                if req.text == '{}':# or data == '':
    #                print req.text
                    signalstrength = -1.0
                else:
                    signalstrength = data['signalstrength']
                    print (req.text)
                logging.debug(req.text)
            else:
                log.err('Signal strength request failed!')
                print (req.text)    
                signalstrength = -1.0
                logging.warn(req.text)
    
            # USIM Status
            if check_usim:
                req = rest.get('v1/device/usim/status')
                if req.status_code == 200:
                    data = json.loads(req.text)
                    sim_status = data['status']
                    log.infog('USIM Status: ' + sim_status)
                    logging.debug(req.text)
                    check_usim = False;
                else:
                    #if req.status_code == 403:
                    data = json.loads(req.text)
                    err_msg = data['errors']['message']
                    log.err('USIM error: ' + err_msg)
                    logging.err(req.text)
                
                
            # Location Update    
            req = rest.get('v1/location')
            if req.status_code == 200:
                data = json.loads(req.text)
                #print data
                gps_fix = data['fix']['fixdesc']
                lon = data['lon']
                lat = data['lat']
                log.info('Location (GPS) : %s (Lon:%s Lat:%s)' % (gps_fix, lon, lat))
                logging.info(data)
    #            print '  Lon : %s Lat: %s' % (lon, lat)
            else:
                log.err('location request failed!')
                print (req.text)
                logging.err(req.text)
                
            
            if (gps_fix == '3d') and (set_ant_flag) and (ant_pointing):
               
                req = rest.get('v1/device/satellites_table')
                if req.status_code == 200:
                    data = json.loads(req.text)
                    print data
                    ele_max = max(data,key=lambda item:item['elevation'])
                    sat_id = ele_max['id']
                    sat_elevation = ele_max['elevation']
                    sat_azimuth = ele_max['azimuth']
                    log.infog('Select satellites id: #%s (Elevation:%s Azimuth:%s)' % (sat_id, sat_elevation, sat_azimuth))
                    logging.info('Select satellites id: #%s (Elevation:%s Azimuth:%s)' % (sat_id, sat_elevation, sat_azimuth))
                    #set_ant_flag = True # set current satellte id
                else:
                    log.err('location satellites request failed!')
                    print (req.text)
                    logging.err('location satellites request failed!')
                
                time.sleep(3)  
            #if set_ant_flag:   ## Set current satellite          
                data = {'satid':sat_id}            
                print data
                req = rest.put('v1/device/current_satellite', payload=data)      
                if req.status_code == 200:
                    d = json.loads(req.text)
                    log.infog('Set current satellite id:' + str(sat_id))
                    logging.info('Set current satellite id:' + str(sat_id))
                   # connection = data['co']
                else:
                    log.err('command failure')
                    print (req.text)       
                    logging.err(req.text)
                set_ant_flag = False
            time.sleep(1)  
            
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry, or continue in a retry loop
            print ("Error Timeout:",e)
            logging.error("Error Timeout:",e)
        except requests.exceptions.ConnectionError as e:
            print ("Error Connecting:",e)      
            logging.error("Error Connecting:",e)
        except requests.exceptions.TooManyRedirects as e:
            # Tell the user their URL was bad and try a different one
            print ("Error TooManyRedirects:",e)    
            logging.error("Error TooManyRedirects:",e)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print ("Error RequestException:",e)             
            print e
            logging.error("Error RequestException:",e)
            sys.exit(1)
            
             

if __name__== '__main__':
    main()

