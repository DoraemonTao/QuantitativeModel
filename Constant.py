# AlarmManager中的配置属性


# type类别
RTC_WAKEUP = 0
RTC = 1
ELAPSED_REALTIME_WAKEUP = 2
ELAPSED_REALTIME = 3

# 必要的时间
INTERVAL_FIFTEEN_MINUTES = 15 * 60 * 1000
INTERVAL_HALF_HOUR = 2 * INTERVAL_FIFTEEN_MINUTES
INTERVAL_HOUR = 2 * INTERVAL_HALF_HOUR
INTERVAL_HALF_DAY = 12*INTERVAL_HOUR
INTERVAL_DAY = 2*INTERVAL_HALF_DAY




# alarm的最小时间间隔
MIN_INTERVAL = 60*1000

MIN_FUTURITY = 5*1000

MAX_INTERVAL = 365*INTERVAL_DAY


if __name__ == '__main__':
    print(FLAG_IDLE_UNTIL)