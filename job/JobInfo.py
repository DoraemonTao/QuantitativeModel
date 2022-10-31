class JobInfo():
    def __init__(self,service,isPeriodic,isPersisted,intervalMills,flexMills):
        self.service = service
        self.isPeriodic = isPeriodic
        self.isPersisted = isPersisted
        self.intervalMills = intervalMills
        self.flexMills = flexMills


    def getService(self):
        return self.service

    def isPeriodic(self):
        return self.service

    def isPersisteed(self):
        return self.isPersisted

    def getIntervalMills(self):
        return self.intervalMills

    def getFlexMill(self):
        return self.flexMills

    def setIntervalMills(self, newIntervalMills):
        self.intervalMills = newIntervalMills

    def extendInterval(self, ratio):
        self.intervalMills = self.intervalMills * ratio


