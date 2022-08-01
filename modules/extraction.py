import motor.motor_asyncio as mongodb
import asyncio
import json


class extract:
    def __init__(self, start_time, end_time):
        '''
        Initialize MongoDB client adn get start_time and end_time variables
        '''
        self.client = mongodb.AsyncIOMotorClient()
        self.mydb = self.client["test"]
        self.mycol = self.mydb["sensor_data"]
        self.start_time = start_time
        self.end_time = end_time
        print(str(self.start_time) + '-' + str(self.end_time))

    async def do_find(self):
        '''
        Find the relevant values in the given time frame
        '''
        self.data = []
        cursor = self.mycol.find({'start_epoch': {'$gte': self.start_time}, 'end_epoch': {'$lt': self.end_time}})
        async for document in cursor:
            document = dict(document)
            # self.data.append([document['sensor_name'], document['start_epoch'], document['end_epoch']])
            # self.data.append(document['sensor_name'])
            for i in document['data']:
                i['timestamp'] = i['timestamp'].strftime('%m-%d-%YT%H:%M:%S')
            self.data.append({"name": document['sensor_name'], "data": document['data']})

    def to_json(self, name, operation, lists):
        # convert data file to json
        with open(name, operation) as infile:
            if operation == "r":
                lists = json.load(infile)
                return lists
            else:
                json_object = json.dumps(lists)
                infile.write(json_object)
                del json_object

    def run(self):
        check = []
        loop = asyncio.get_event_loop()
        # Loop over a certain times to get data relative to Start time, 
        # implemented a checklist to prevent duplicates
        for i in range(0, 50):
            self.end_time = self.start_time + 5 * 86385
            name = "data/data_" + str(self.start_time) + '-' + str(self.end_time) + ".json"
            print(name)
            try:
                check = self.to_json('checklist.json', "r", check)
            except Exception as E:
                print(E)
                self.to_json('checklist.json', "w", check)
            if name in check:
                self.start_time = self.end_time
                continue
            check.append(name)
            loop.run_until_complete(self.do_find())
            # print(self.data)
            print(len(self.data))
            if len(self.data) == 1:
                print(self.start_time, ' - ', self.end_time)
                break
            self.to_json(name, "w", self.data)
            self.to_json('checklist.json', "w", check)
            del self.data
            self.start_time = self.end_time
        loop.close()


initial = 1514764815
extract(initial, initial + (4) * 86385).run()
