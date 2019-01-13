
from settings import TIME_ROOT, MONTH, TODAY, LABELS
import os
import logging
import datetime
import xlsxwriter
logger = logging.getLogger(__name__)

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

        row = 0
        col = 0

        for item in self.data[LABELS]:
            worksheet.write(row, col, str(item['label']))
            worksheet.write(row, col + 1, str(item['work_items']))
            row += 1

        workbook.close()
        logger.info("Published spreadsheet data: {}".format(new_report))
        # with open(new_report, 'w') as report:
        #     report.writelines(str(self.data))
