from alarm.AlarmManager import *

# 对齐模块中alarm的数据结构
class BatchingAlarmStore:


    def __init__(self):
        self.mAlarmBatches = []
        self.mSize = 0
        self.deliveryBatchNum = 0

    def add(self, alarm):
        self.insertAndBatchAlarm(alarm)
        self.mSize = self.mSize + 1

    def addAll(self, alarms):
        if (alarms == None):
            return
        for a in alarms:
            self.add(a)

    # 模块暂不需要，后续根据情况编写
    def remove(self):
        return

    def removeBatch(self,index):
        self.mSize -= len(self.mAlarmBatches[index])
        self.mAlarmBatches.pop(index)


    def rebatchAllAlarms(self):
        oldBatched = self.mAlarmBatches
        self.mAlarmBatches = []
        for batch in oldBatched:
            for i in range(len(batch)):
                self.insertAndBatchAlarm(batch[i])

    def getSize(self):
        return self.mSize

    # 得到下次的交付时间
    def getNextDeliveryTime(self):
        if len(self.mAlarmBatches):
            return self.mAlarmBatches[0].mStart

    def getNextWakeFromIdleAlarm(self):
        for batch in self.mAlarmBatches:
            if batch.mFlags & FLAG_WAKE_FROM_IDLE == 0:
                continue
            for i in range(len(batch)):
                a = batch.get(i)
                if a.flags & FLAG_WAKE_FROM_IDLE !=0:
                    return a
        return None

    # 将alarm插入至合适的batch中
    def insertAndBatchAlarm(self, alarm):
        whichBatch = self.attemptCoalesce(alarm.getWhenElapsed(),alarm.getMaxWhenElapsed()) if (alarm.flags & FLAG_STANDALONE != 0) else -1
        if whichBatch < 0:
            self.addBatch(self.mAlarmBatches, Batch(alarm))
        else:
            batch = self.mAlarmBatches[whichBatch]
            if batch.add(alarm):
                self.mAlarmBatches.pop(whichBatch)
                self.addBatch(self.mAlarmBatches,batch)

    # 在alarmStore队列中加入新的Batch
    def addBatch(self, list, newBatch):
        if len(list) == 0:
            list.append(newBatch)
        else:
            index = self.binarySearch(list, newBatch,0,len(list)-1)
            list.insert(index, newBatch)

    # 二分查找
    def binarySearch(self, list, newBatch, l, r):
        if r >= l:
            mid = int(l + (r - l) / 2)
            if list[mid].mStart > newBatch.mStart:
                return self.binarySearch(list, newBatch, l, mid - 1, )
            else:
                return self.binarySearch(list, newBatch, mid + 1, r)
        else:
            return r

    # 返回对应的batch索引，-1表示未找到
    def attemptCoalesce(self, whenElapsed, maxWhen):
        n = len(self.mAlarmBatches)
        for i in range(n):
            b = self.mAlarmBatches[i]
            if b.canHold(whenElapsed, maxWhen):
                return i

        return -1

    # 去除当前时间触发的alarm
    def removePendingAlarms(self,nowElapsed):
        deliveryNum = 0
        while len(self.mAlarmBatches)>0:
            batch = self.mAlarmBatches[0]
            if batch.mStart > nowElapsed:
                break
            self.mAlarmBatches.pop(0)
            deliveryNum += 1
        return deliveryNum



    def updateAlarmDeliveries(self,fun):
        changed = False
        for b in self.mAlarmBatches:
            for i in range(len(b)):
                # 匿名函数，由调用者定义函数方法
                changed |= fun(b[i])
        if changed:
            self.rebatchAllAlarms()
        return changed

    def rebatchAllAlarms(self):
        oldBatches = self.mAlarmBatches
        self.mAlarmBatches = None
        for batch in oldBatches:
            for i in range(len(batch)):
                self.insertAndBatchAlarm(batch[i])

class Batch:
    mAlarms = []

    # 新加入一个alarm时调用
    def __init__(self, seed):
        self.mStart = seed.getWhenElapsed()
        self.mEnd = seed.getMaxWhenElapsed()
        self.mAlarms.append(seed)

    def size(self):
        return len(self.mAlarms)

    def get(self, index):
        return self.mAlarms[index]

    def canHold(self, whenElapsed, maxWhen):
        return (self.mEnd >= whenElapsed) and (self.mStart <= maxWhen)

    def add(self, alarm):
        # 是否改变batch
        newStart = False
        index = self.binarySearch(self.mAlarms,alarm,0,len(self.mAlarms)-1)
        self.mAlarms.insert(index,alarm)
        # if alarm.getWhenElapsed() > self.mStart:
        if alarm.getWhenElapsed() > self.mStart:
            self.mStart = alarm.getWhenElapsed()
            newStart = True
        if alarm.getMaxWhenElapsed() < self.mEnd:
            self.mEnd = alarm.getMaxWhenElapsed()
        return newStart

    def binarySearch(self, mAlarms, alarm, l, r):
        if r >= l:
            mid = int(l + (r - l) / 2)
            if mAlarms[mid].getWhenElapsed() > alarm.getWhenElapsed():
                return self.binarySearch(mAlarms, alarm, l, mid - 1, )
            else:
                return self.binarySearch(mAlarms, alarm, mid + 1, r)
        else:
            return r



# 测试用
if __name__ == '__main__':
    alarmstores = BatchingAlarmStore()
    alarm = Alarm()
    alarmstores.add(alarm)
