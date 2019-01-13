
from settings import TIME_ROOT, MONTH, TODAY, LABELS, TIME_FORMAT
import os
import logging
import datetime
import xlsxwriter
logger = logging.getLogger(__name__)

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

class TicketSystemPublisher(object):

    def __init__(self, **kw):
        super(TicketSystemPublisher, self).__init__(self, **kw)

    def publish(self):
        pass

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
