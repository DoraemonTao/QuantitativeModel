from job.JobStore import JobStore
from util import SystemTime
class JobSchedulerService:
    def __init__(self):
        self.mDeliveryNum = 0
        self.mJobs = JobStore()

    # 得到总交付数
    def getDeliveryNum(self):
        return self.mDeliveryNum

    # job加入时的调度函数
    def schedule(self,j):
        self.setTime(j)
        self.startTackingJobLocked(j)

    # 交付满足约束条件的alarm
    def deliveryJob(self):
        self.mDeliveryNum += self.isReadyToBeExecutedLocked(SystemTime.getCurrentTime())

    # job任务跟踪
    def startTackingJobLocked(self,jobStatus):
        update = self.mJobs.add(jobStatus)

    # 将满足条件的job触发
    def isReadyToBeExecutedLocked(self,time):
        delivery_num = 0
        alljobs = self.mJobs.mJobSet.getAllJobs()
        for job in alljobs:
            # 满足时间约束
            if job.completedJobTimeElapsd > time:
                self.mJobs.remove(job)
                delivery_num += 1
        return delivery_num
