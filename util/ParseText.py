import re
from alarm.Alarm import *
from job.JobStatus import *
from util.Constant import *


class ParseText:
    def __init__(self, lines):
        self.lines = lines
        self.mAlarmStore = []
        self.mJobStore = []

    def parse(self):
        # 相应段的Flag标志位
        alarmContentFlag = False
        jobContentFlag = False

        for line in self.lines:
            if line == "\n":
                alarmContentFlag = False
                jobContentFlag = False
            # judge arrive alarm paragraph
            line = line.lstrip()
            if not alarmContentFlag and not jobContentFlag:
                alarmContentFlag = re.search("Delivery alarm :.*",line)
                if alarmContentFlag:
                    continue
            # judge arrive job paragraph
            if not jobContentFlag:
                jobContentFlag = re.search("Recently delivery jobs:.*", line)
                if jobContentFlag:
                    continue

            # parse alarm info
            # alarm paragraph
            if alarmContentFlag:
                policyWhenElapsed = []
                attribute = line.split(',')
                uid = int(attribute[0])
                type = int(attribute[1])
                when = int(attribute[2])
                requestedWhenElapsed = int(attribute[3])
                maxWhenElapsed = int(attribute[4])
                elapsedRealtime = int(attribute[5])
                enqueueTime = int(attribute[6])
                windowLength = int(attribute[7])
                repeatInterval = int(attribute[8])
                flags = int(attribute[9])
                pkg = attribute[10]
                policyWhenElapsed.append(None if attribute[11] == '/' else int(attribute[11]))
                policyWhenElapsed.append(None if attribute[12] == '/' else int(attribute[12]))
                policyWhenElapsed.append(None if attribute[13] == '/' else int(attribute[13]))
                mAlarm = Alarm(uid,type, when, requestedWhenElapsed, maxWhenElapsed, enqueueTime, elapsedRealtime,
                               windowLength, repeatInterval, flags, pkg,
                               policyWhenElapsed[0], policyWhenElapsed[1])
                self.mAlarmStore.append(mAlarm)
            # parse job info
            # job paragraph
            if jobContentFlag:
                attribute = line.strip().split(',')
                callingUid = int(attribute[0])
                sourcePackageName = attribute[1]
                sourceUserId = int(attribute[2])
                standbyBucket = int(attribute[3])
                tag = attribute[4]
                earliestRunTimeElapsedMillis = int(attribute[5])
                latestRunTimeElapsedMills = int(attribute[6])
                lastSuccessfulRunTime = int(attribute[7])
                lastFailedRunTime = int(attribute[8])
                completedJobTimeElapsd = int(attribute[9])
                isPeriodic = bool(attribute[10])
                isPersisted = bool(attribute[11])
                intervalMills = int(attribute[12])
                flexMills = int(attribute[13])
                mJob = JobStatus(callingUid, sourcePackageName, sourceUserId, standbyBucket,
                                 tag, earliestRunTimeElapsedMillis, latestRunTimeElapsedMills,
                                 lastSuccessfulRunTime, lastFailedRunTime, completedJobTimeElapsd, isPeriodic,
                                 isPersisted, intervalMills, flexMills)
                self.mJobStore.append(mJob)

    def get_alarm_store(self):
        return self.mAlarmStore

    def get_job_store(self):
        return self.mJobStore
