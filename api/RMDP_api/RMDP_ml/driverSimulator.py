# from generatingData import generateTestData
# from Math.Geometry import interSectionCircleAndLine
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
# from Math import Geometry


from Database_Operator.Mongo_Operator import Mongo_Operate
from Math import Geometry


class driverSimulator:
    def __init__(self):
        self.totalCurrentWorker = 2
        self.DEBUG = False if int(os.environ['DEBUG']) == 1 else True
        self.DBclient = Mongo_Operate()
        self.updateTime = 1

    def generateThread(self):
        cityList = self.DBclient.getAllCity()
        logging.info("start generating city")
        with ThreadPoolExecutor(max_workers=self.totalCurrentWorker) as executor:
            threads = []
            for i in range(len(cityList)):
                threads.append(executor.submit(self.updateDriverLocation, index=i, cityName=(cityList[i]['City'])))
        logging.info("task completed")

    def updateDriverLocation(self, index, cityName):
        try:
            driverList = self.DBclient.getHasOrderDriverBaseOnCity(cityName)
            restaurantIdList = list(
                map(lambda x: int(x['Restaurant_ID']), self.DBclient.getRestaurantIDBaseOnCity(cityName)))
            orderList = self.DBclient.getPairedOrderBaseOnCity(restaurantIdList)
            if len(driverList) > 0:
                for currentDriver in driverList:

                    targetDestination = currentDriver['Route'][0]
                    DistanceRemain = Geometry.coorDistance(currentDriver['Latitude'],
                                                           currentDriver['Longitude'],
                                                           targetDestination['Latitude'],
                                                           targetDestination['Longitude'])
                    DistanceTraveled = currentDriver['Velocity'] * self.updateTime

                    if DistanceTraveled > DistanceRemain:
                        currentDriver['Latitude'] = targetDestination['Latitude']
                        currentDriver['Longitude'] = targetDestination['Longitude']
                        travelLocation = currentDriver['Route'].pop(0)
                        currentOrder = next(
                            order for order in orderList if order['Order_ID'] == travelLocation['Order_ID'])

                        if travelLocation['nodeType'] == 0:
                            currentOrder['order_status'] = 'delivered'
                            currentOrder['order_delivered_customer_date'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        else:
                            currentOrder['order_status'] = 'headToCus'
                            currentOrder['order_restaurant_carrier_date'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        self.DBclient.updateOrder(targetDestination)
                        currentDriver['Capacity'] -= 1

                        if currentDriver['Route'] is None:
                            currentDriver['Velocity'] = 0
                    else:
                        updatedLon, updatedLat = Geometry.interSectionCircleAndLine(currentDriver['Longitude'],
                                                                                    currentDriver['Latitude'],
                                                                                    DistanceTraveled,
                                                                                    currentDriver['Longitude'],
                                                                                    currentDriver['Latitude'],
                                                                                    targetDestination['Longitude'],
                                                                                    targetDestination['Latitude'])
                        currentDriver['Latitude'] = updatedLon
                        currentDriver['Longitude'] = updatedLat
                    self.DBclient.updateDriver(currentDriver)
        except Exception as e:
            logging.critical(e, exc_info=True)


test = driverSimulator()
test.generateThread()
