
from settings import TIME_ROOT, MONTH, TODAY, LABELS, TIME_FORMAT
from settings import API_JIRA_SECRET
import os
import logging
import datetime
import xlsxwriter
logger = logging.getLogger(__name__)
from jira import JIRA


def get_elapsed_time(work_items):
    out = 0
    for w in work_items:
        start_time = w['start_time']
        if not start_time:
            continue

        stop_time = w['stop_time']
        start_time = datetime.datetime.strptime(start_time, TIME_FORMAT)
        stop_time = datetime.datetime.strptime(stop_time, TIME_FORMAT)
        c = stop_time - start_time
        diff = divmod(c.days * 86400 + c.seconds, 60)
        out += diff[0]
    return out

def open_secret(file):
    """"
    .txt file with:
    1. host
    2. user
    3. password
    """""
    with open(file, 'r') as secret_file:
        return [s.replace("\n", "") for s in secret_file.readlines()]

class TicketJiraPublisher(object):

    def __init__(self, data):
        self.data = data
        self.live = True
        if not os.path.exists(API_JIRA_SECRET):
            logger.critical("Cannot find: {}".format(API_JIRA_SECRET))
            self.live = False
            return

        secret_data = open_secret(API_JIRA_SECRET)
        self.jira = JIRA(
            secret_data[0], 
            auth=(secret_data[1], secret_data[2])
        )

    def get_work_entries(self, issue):
        return issue.fields.worklog.worklogs

    def is_unique(self, work_entries, start_time):
        if not work_entries:
            return True
        for w in work_entries:
            friendly_time = str(w.started).replace("T", " ").split(".")[0]
            if friendly_time == str(start_time):
                return False
        return True

    def publish(self):

        if not self.live:
            return

        for item in self.data[LABELS]:
            if item["type"] != "jira": continue
            if not item["ticket"]: continue

            # when the work entry was started for the first time
            created = item['work_items'][0]['start_time']
            start_time = datetime.datetime.strptime(created, TIME_FORMAT)

            # total elapsed time on this ticket
            elapsed_time = get_elapsed_time(item['work_items'])
            try:
                jira_issue_object = self.jira.issue(item["ticket"])
            except:
                logger.warning("Cannot fetch: {}".format(item["ticket"]))
                continue

            work_entries = self.get_work_entries(issue=jira_issue_object)

            if not self.is_unique(
                work_entries=work_entries, start_time=start_time
                ):
                logger.warning(
                    "Skipping: {} start time: {} already exist".format(
                    item["ticket"],
                    start_time
                    )
                )
                continue

            if elapsed_time == 0: 
                logger.warning("Skipping") 
                continue

            time_spent = "{}m".format(elapsed_time)
            self.jira.add_worklog(
                issue=item["ticket"],
                timeSpent=time_spent, 
                comment=item["label"],
                started=start_time
            ) 
            logger.info(
                "New worklog {} task: {} elapsed time: {}m".format(
                item["ticket"],
                item["label"],
                elapsed_time
            ))

class SpreadsheetPublisher(object):

    def __init__(self, data):

        self.data = data

    def publish(self):
        new_report = os.path.join(
            TIME_ROOT, 'reports', MONTH, 'report_{}.xlsx'.format(TODAY)
        )
        folder = os.path.dirname(new_report)
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(new_report)
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 0, 50)  
        worksheet.set_column(1, 0, 15)
        worksheet.set_column(2, 0, 15)
        worksheet.set_column(3, 0, 40)

        row = 0
        col = 0
        headers = ['subtask', 'ticket', 'elapsed time (minutes)', 'time created']
        for h in headers:
            worksheet.write(row, col, h)
            col+=1

        row = 1
        col = 0

        for item in self.data[LABELS]:
            elapsed_time = get_elapsed_time(item['work_items'])
            created = item['work_items'][0]['start_time']
            worksheet.write(row, col, str(item['label']))
            worksheet.write(row, col + 1, str(item['ticket']))
            worksheet.write(row, col + 2, elapsed_time)
            worksheet.write(row, col + 3, created)
            row += 1

        workbook.close()
        logger.info("Published spreadsheet data: {}".format(new_report))
