'''
Title: chief_drone.py
Author: Conor Green
Description: Class to maintain the same drone object (from ps_drone). Holds methods to get navdata and fly
Usage: Call from principal_drone to multiprocess navdata and flying
Public Methods:
    get_navdata_background - Queries the drone for navdata for a set period of time. See method for kwargs arguments
Version:
1.0 - June 17 2019 - Initial creation. Copy/pasted methods from previous scripts
'''

#Standard lib imports
import time

#Extended library
import numpy as np

#Philip's backbone import
import ps_drone

#Imports from this porject

### TODOs: see __init__
###
###
###

class Chief:


    ## TODO: Update for python3 and change version
    def __init__(self):
        self.__Version = "2.7.15"

        #Connect to drone
        self.drone = drone = ps_drone.Drone()
        drone.startup()
        drone.reset()

        #Wait for reset to complete
        while(drone.getBattery()[0] == -1): time.sleep(.01)

        return


    def fly():
        pass


    '''
    ----------- Navdata section ----------
    '''
    #Return: flight_data - list of dictionaries of numpy arrays
    #        and the delta_t
    def get_navdata_background(desired_data , **kwargs):
        options = {'req_take_off' : False , 'demo' : True , 'time_lim' : 20}
        options.update(kwargs)

        #Determines packet rate
        #True = 15packets/s
        #False = 200pk/s
        self.drone.useDemoMode(options['demo'])
        #and use that to determine the delta time between each packet/frame
        if options['demo']:
            delta_t = 1/ 15
        else:
            delta_t = 1/200


        #Determine which packets to recieve
        self.drone.getNDpackage(desired_data)

        #Wait for takeoff
        while options['req_take_off']:
            print("stuck here?")
            if self.drone.State == 1:
                options['req_take_off'] = False
                break
            time.sleep(.5)

        print("about to gather_flight_data")
        flight_data = gather_data_set_time(options['time_lim'])
        print("Have gathered data")


        return (flight_data , delta_t)


        ###Gathers data as specified by the arguments in main for a specified amount of time
        ###Returns: List of time slices of data (data is dictionary of lists ----not numpy arrays anymore)
        def gather_data_set_time(time_lim):
            t_end = time.time() + time_lim

            print(t_end)

            flight_data = []
            last_NDC = self.drone.NavDataCount -1

            while time.time() < t_end:
                print(time.time())

                while self.drone.NavDataCount == last_NDC:
                    print(self.drone.NavDataCount)
                    #if drone.getKey():
                    #	end = True
                    time.sleep(.00045)

                last_NDC = self.drone.NavDataCount

                _data_slice = self.get_nav_frame()
                flight_data.append(_data_slice)

            return flight_data


        '''
        Queries drone for navdata after waiting for new data and packages them nicely.
        Has slim parameter to only take values deemed important
        Return: Dictionary of numpy arrays and last navdatacount
        '''

        #TODO: Finish list of VISION later

        def get_nav_frame(*kwargs):

            print("Within navframe")
            print(self.drone.NavDataCount)
            options = {'slim' : True}
            options.update(kwargs)

            #For slim, important indicies of the parameter are given
            #All of demo is important*   *maybe
            #none of zimmu_3000 is important because it is unknown
            important = {'demo': range(0,12) , 'time' : [0], 'wifi' : [0] , \
                        'magneto': range(0,4) , 'altitude' : range(0,5) , 'pressure_raw': [0,1] , \
                        'wind_speed' : [0 , 1] , 'kalman_pressure':[1] , 'zimmu_3000':[] , \
                        'raw_measures' : range(0,4) , 'phys_measures' : [2 , 3] , 'references' : range(0,5) , \
                        'rc_references' : range(0,5) , 'gyros_offsets' : [0] , 'euler_angles' : [0 ,1] , \
                        'watchdog' : [] , 'trims' : range(0,4) , 'pwm' : range(0,12) , \
                        'state' : []
                        }
            ################################
            #TODO: Finish list of VISION later




            last_NDC = self.drone.NavDataCount

            data = {}

            if options['slim']:
                for _d_param in self.drone.NavData:

                    data[_d_param] = []

                    #for important element, copy that
                    for _important_elem in important[_d_param]:
                        data[_d_param].append(self.drone.NavData[_d_param][_important_elem])
                    #data[_d_param] = np.array(drone.NavData[_d_param][_important_elems])

            else:
                for _d_param in self.drone.NavData:
                    data[_d_param] = self.drone.NavData[_d_param]
                    #data[_d_param] = np.array(drone.NavData[_d_param])

            print("\n++++++++++++++++++++++++++++++++++++")
            print(data)
            print(last_NDC)
            print("------------------------------------\n")

            return data
