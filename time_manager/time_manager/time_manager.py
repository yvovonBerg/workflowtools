import os
import sys
import json
import datetime
import uuid
import argparse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

import publisher
from settings import MONTH, TODAY, NOW, TIME_ROOT, LABELS, LAST_STOPPED, ACTIVE_TASK


class TimeManager(object):
    def __init__(self, time_file=None):
        self.time_data_file = time_file or os.path.join(
            TIME_ROOT, 'timelogs', MONTH, '{}.json'.format(TODAY)
        )
        self.time_data = {LABELS: [], ACTIVE_TASK: "", LAST_STOPPED: ""}
        self._read_task_data()

    def _setup_files(self):
        root_folder = os.path.dirname(self.time_data_file)
        if not os.path.exists(root_folder):
            os.makedirs(root_folder)

    def _read_task_data(self):
        self._setup_files()
        if not os.path.exists(self.time_data_file):
            self._write_task_data()

        with open(self.time_data_file, 'r') as time_file:
            try:
                self.time_data = json.load(time_file)
            except ValueError:
                print "Invalid json file: {}".format(time_file)

    def _write_task_data(self):
        with open(self.time_data_file, 'w') as time_file:
            time_file.write(json.dumps(self.time_data, indent=4))

    def _clear_active_tasks(self):
        self.time_data[ACTIVE_TASK] = ""

    @property
    def labels(self):
        if LABELS not in self.time_data.keys():
            return []

        return self.time_data[LABELS]

    def get_active_task(self, include_labels=False):
        """
            Get the current running tasks.
            return: string
        """

        if ACTIVE_TASK not in self.time_data.keys():
            return ""

        active_item = self.time_data[ACTIVE_TASK]
        if not include_labels:
            return active_item

        for label in self.labels:
            if label['id'] == active_item:
                return label

        return ""

    def start_new_task(self, label, task_type='default', ticket=None):
        """
            Starts a brand new tasks. Stops all active tasks first.
            This will also clear the last stopped cache to 
            prevent > 1 task in progress.
        """

        # stopping current tasks
        self.stop_all_tasks()

        # clearing last_stopped cache
        self.time_data[LAST_STOPPED] = ""

        task_id = str(uuid.uuid4())
        new_work_entry = {'start_time': NOW, 'stop_time': ''}
        self.time_data[LABELS].append({
            'label': label,
            'work_items': [new_work_entry],
            'type': task_type,
            'ticket': ticket,
            'id': task_id
        })
        self.time_data[ACTIVE_TASK] = task_id
        self._write_task_data()

    def stop_task(self, task_id):
        new_labels = []
        stopped = False
        for label in self.labels:
            new_label = label
            new_work_entries = []
            if task_id != label['id']:
                new_labels.append(new_label)
                continue

            # found task to stop
            logger.info('Stopping {} {}'.format(task_id, label['label']))

            current_work_items = new_label['work_items']
            for w in current_work_items:
                new_work_entry = w

                # add time to item that has no stop time yet
                if w['stop_time'] == '':
                    new_work_entry['stop_time'] = NOW
                new_work_entries.append(new_work_entry)

            self.time_data[ACTIVE_TASK] = ""
            self.time_data[LAST_STOPPED] = task_id
            stopped = True
            if new_work_entries:
                new_label['work_items'] = new_work_entries
            new_labels.append(new_label)

        if not stopped:
            logger.error("Cannot find task with id: {}".format(task_id))
            return

        self.time_data[LABELS] = new_labels
        self._write_task_data()

    def stop_all_tasks(self):
        if not self.labels or not self.get_active_task():
            return

        self.stop_task(task_id=self.get_active_task())

        self._clear_active_tasks()
        self._write_task_data()

    def remove_all_tasks(self):
        self._clear_active_tasks()
        self.time_data[LABELS] = []
        self.time_data[LAST_STOPPED] = ""
        self._write_task_data()

    def resume_last_stopped(self):
        if not self.time_data[LAST_STOPPED]:
            return

        if not self.labels:
            return

        last_stopped = self.time_data[LAST_STOPPED]
        new_labels = []
        for label in self.labels:
            new_work_entries = label['work_items']
            if label['id'] == last_stopped:
                new_work_entries.append({'start_time': NOW, 'stop_time': ''})

            label['work_items'] = new_work_entries
            new_labels.append(label)

        self.time_data[LAST_STOPPED] = ""
        self.time_data[ACTIVE_TASK] = last_stopped
        self._write_task_data()

def are_you_sure(args):
    if not args.silent:
        sure = raw_input("Are you sure: [Y/n] ") or "y"
        if sure != "y":
            return False

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--stop', help='Stop all tasks', action='store_true'
    )
    parser.add_argument(
        '-d', '--removeall', help='Remove all tasks', action='store_true')
    parser.add_argument('-n', '--label', help='Add task')
    parser.add_argument('-t', '--type', help='Add task type')
    parser.add_argument('-ti', '--ticket', help='Add ticket')
    parser.add_argument(
        '-p', '--publish', help='Publish (defaults to today, see --fimefile)',
         action="store_true"
    )
    parser.add_argument(
        '-tf', '--timefile', help='Path to time file'
    )
    
    parser.add_argument(
        '-q', '--silent', help='Silent say Yes to all questions', action="store_true"
    )    
    parser.add_argument(
        '-at',
        '--activetask',
        help='Return activate tasks',
        action="store_true"
    )
    parser.add_argument(
        '-l', '--list', help='Return all tasks', action="store_true")
    parser.add_argument(
        '-spp', '--spreadsheetpublishonly', help='Only do spreadsheet publish', action="store_true")
    parser.add_argument(
        '-r',
        '--resume',
        help='Continue last stopped task',
        action="store_true"
    )

    args = parser.parse_args()
    tm = TimeManager(time_file=args.timefile)

    if args.publish:
        logger.info('Publishing data')
        if not are_you_sure(args): return
        tm.stop_all_tasks()
        pdf = publisher.SpreadsheetPublisher(data=tm.time_data)
        pdf.publish()

        if not args.spreadsheetpublishonly:
            jira = publisher.TicketJiraPublisher(data=tm.time_data)
            jira.publish()

            youtrack = publisher.TicketYoutrackPublisher(data=tm.time_data)
            youtrack.publish()
        return

    if args.stop:
        logger.info('stopping active task')
        tm.stop_all_tasks()
        return

    if args.removeall:
        logger.info('About to removing all tasks')
        if not are_you_sure(args): return
        logger.info('Removing all tasks')
        tm.remove_all_tasks()
        return

    if args.activetask:
        data = tm.get_active_task(include_labels=True)
        if not data:
            logger.info('No active tasks')
            return 
        logger.info('LABEL:{} | {}'.format(data['label'], data['id']))
        return

    if args.list:
        data = tm.labels
        for d in data:
            logger.info('LABEL:{} | {}'.format(d['label'], d['id']))
        return

    if args.resume:
        logger.info('Resume last stopped task')
        tm.resume_last_stopped()
        logger.info('Active task: {}'.format(tm.get_active_task(
            include_labels=True)['label'])
        )
        return

    if args.label:
        logger.info('Creating new task')
        tm.start_new_task(
            label=args.label, task_type=args.type,
            ticket=args.ticket
        )


if __name__ == "__main__":
    main()
