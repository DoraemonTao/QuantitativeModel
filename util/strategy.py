from util.Constant import *
from alarm.AlarmManager import *
from alarm.Alarm import Alarm


# 延长alarm的周期
def delivery_time_delay(tasks, ratio=1, WINDOW_LENGTH_ENLARGE=False):
    if WINDOW_LENGTH_ENLARGE:
        for task in tasks:
            if isinstance(task, Alarm):
                if task.repeatInterval != 0 and task.repeatInterval > task.windowLength:
                    if task.mMaxWhenElapsed < task.mWhenElapsed + task.repeatInterval * DELAY_PERCENTAGE:
                        task.mMaxWhenElapsed = task.mWhenElapsed + task.repeatInterval * DELAY_PERCENTAGE
                if task.windowLength != 0:
                    if task.mMaxWhenElapsed < task.getWhenElapsed() + task.windowLength * ratio:
                        task.mMaxWhenElapsed = task.getWhenElapsed() + task.windowLength * ratio
