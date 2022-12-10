import sys

import numpy as np

from alarm.AlarmManager import *
from alarm.BatchingAlarmStore import BatchingAlarmStore


# 应用不同策略下的alarm对齐次数
from util.bs_csv import  hc_query_plus_prime, get_uid_hardware_time_set


class OptiBatchedAlarmStore(BatchingAlarmStore):

    def getNextDeliveryTime(self):
        if len(self.mAlarmBatches):
            return self.mAlarmBatches[0].mEnd

    def getNextWakeupDeliveryTime(self):
        for b in self.mAlarmBatches:
            if b.hasWakeups():
                return b.mEnd

    def removePendingAlarms(self, nowElapsed):
        deliveryNum = 0
        wakeupNum = 0
        hardware_usages_num = 0
        while len(self.mAlarmBatches) > 0:
            batch = self.mAlarmBatches[0]
            if batch.mEnd > nowElapsed:
                break
            if batch.hasWakeups():
                wakeupNum += 1
            if batch.hardware_set is not None:
                hardware_usages_num += len(batch.hardware_set)
            self.mAlarmBatches.pop(0)
            deliveryNum += 1
        return deliveryNum, wakeupNum, hardware_usages_num

     # 返回对应的batch索引，-1表示未找到
    def attemptCoalesce(self, whenElapsed, maxWhen,uid):
        if (not self.TIME_OVERLAP_PRIORITY) and (not self.HARDWARE_SET_PRIORITY):
            n = len(self.mAlarmBatches)
            for i in range(n):
                b = self.mAlarmBatches[i]
                if (b.mFlags & FLAG_STANDALONE == 0) and b.canHold(whenElapsed, maxWhen):
                    return i
            return -1
        else:
            n = len(self.mAlarmBatches)
            batch_priority = []
            for i in range(n):
                priority = 0
                b = self.mAlarmBatches[i]
                if (b.mFlags & FLAG_STANDALONE == 0) and b.canHold(whenElapsed, maxWhen):
                    priority = self.get_priority(b,whenElapsed,maxWhen,uid)
                else:
                    priority = sys.maxsize
                batch_priority.append(priority)
            min_priority = min(batch_priority)
            if min_priority == sys.maxsize:
                return -1
            return batch_priority.index(min_priority)


    # 找到合适的batch，并将执行时间设置为jobTime
    def setSuitableBatch(self,job):
        whichBatch = self.attemptCoalesce(job.completedJobTimeElapsd, job.completedJobTimeElapsd,job.callingUid)
        if whichBatch < 0:
            return False
        else:
            batch = self.mAlarmBatches[whichBatch]
            if batch.setExactTime(job.completedJobTimeElapsd):
                for hardware in get_uid_hardware_time_set().get(job.callingUid, []).copy():
                    if hardware[0] not in batch.hardware_set:
                        batch.hardware_set[hardware[0]] = hardware[1]
                    else:
                        if hardware[1] > batch.hardware_set[hardware[0]]:
                            batch.hardware_set[hardware[0]] = hardware[1]
                self.mAlarmBatches.pop(whichBatch)
                self.addBatch(self.mAlarmBatches, batch)
                return True

    def get_priority(self,b,whenElapsed,maxWhen,uid):
        priority = 0
        # config
        overlap_step = 3
        hardware_step = 3

        # 时间重复率
        # 若窗口间隔等于0 则直接返回合适的batch
        if self.TIME_OVERLAP_PRIORITY:
            overlap = self.get_overlap(b, whenElapsed, maxWhen)
            overlap_thresholds = np.linspace(1, 0, overlap_step)
            if b.hasWakeups():
                i = 1
                for threshold in overlap_thresholds:
                    if overlap >= threshold:
                        priority += i
                        break
                    i = i+hardware_step
            else:
                i = hardware_step*overlap_step + 1
                for threshold in overlap_thresholds:
                    if overlap >= threshold:
                        priority += i
                        break
                    i = i + hardware_step
        # 硬件优先级
        if self.HARDWARE_SET_PRIORITY:
            i = 1
            hardware_similarity = hc_query_plus_prime(get_uid_hardware_time_set().get(uid,[]).copy(),b.hardware_set)
            hardware_thresholds = np.linspace(1, 0, hardware_step)
            for threshold in hardware_thresholds:
                if hardware_similarity >= threshold:
                    priority += i
                    break
                i = i+1
        return priority

    # 得到overlap
    def get_overlap(self,b,whenElapsed,maxWhen):
        if whenElapsed != maxWhen:
            if whenElapsed < b.mStart:
                if maxWhen < b.mEnd:
                    overlap = (maxWhen - b.mStart) / (b.mEnd - b.mStart)
                else:
                    overlap = (b.mEnd - b.mStart) / (b.mEnd - b.mStart)
            else:
                if maxWhen < b.mEnd:
                    overlap = (maxWhen - whenElapsed) / (b.mEnd - b.mStart)
                else:
                    overlap = (b.mEnd - whenElapsed) / (b.mEnd - b.mStart)
        else:
            overlap = 0
        return overlap
