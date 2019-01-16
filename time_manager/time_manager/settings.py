import datetime, os

TIME_ROOT = "D:/time"
ACTIVE_TASK = 'active_task'
LAST_STOPPED = 'last_stopped'
LABELS = 'labels'

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
NOW = datetime.datetime.now().strftime(TIME_FORMAT)
TODAY = datetime.datetime.today().strftime("%Y-%m-%d")
MONTH = datetime.datetime.today().strftime("%Y-%m")
API_JIRA_SECRET = os.path.join(
    TIME_ROOT, 'configs', 'jira.txt'
)
