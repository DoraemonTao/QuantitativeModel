class JobStatus:
    def __init__(self,
                 callingUid,
                 sourcePackageName,
                 sourceUserId,
                 standbyBucket,
                 tag,
                 earliestRunTimeElapsedMillis,
                 latestRunTimeElapsedMillis,
                 lastSuccessfulRunTime,
                 lastFailedRunTime,
                 completedJobTimeElapsd,
                 isPeriodic,
                 isPersisted,
                 intervalMills,
                 flexMills
                 ):

        self.callingUid = callingUid
        self.standbyBucket = standbyBucket

        self.sourceUserId = sourceUserId
        self.sourceTag = tag

        self.earliestRunTimeElapsedMillis = earliestRunTimeElapsedMillis
        self.latestRunTimeElapsedMillis = latestRunTimeElapsedMillis
        self.mOriginalLatestRunTimeElapsedMillis = latestRunTimeElapsedMillis
        self.sourcePackageName = sourcePackageName

        self.mLastSuccessfulRunTime = lastSuccessfulRunTime
        self.mLastFailedRunTime = lastFailedRunTime
        self.completedJobTimeElapsd = completedJobTimeElapsd

        self.isPeriodic = isPeriodic
        self.isPersisted = isPersisted
        self.intervalMills = intervalMills
        self.flexMills = flexMills
        # self.flags = flags
