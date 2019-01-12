import os
import sys
import json
import getpass


class VSCodeSettings(object):

    def __init__(
        self,
        root_path
    ):
        self.root_path = os.path.join(root_path, '.vscode', 'settings.json')
        self.project_data = {}
        self._read_settings()
    
    def _read_settings(self):
        if not os.path.exists(self.root_path):
            print "Cannot find: {}".format(self.root_path)
            return

        with open(self.root_path, 'r') as project_file:
            try:
                self.project_data = json.load(project_file)
            except ValueError:
                print "Invalid json data: {}".format(self.root_path)
                return

    @property
    def environment(self):
        if not self.project_data:
            return
        
        if not 'python.pythonPath' in self.project_data.keys():
            return 
        
        return self.project_data['python.pythonPath']

if __name__ == "__main__":
    path = sys.argv[1]
    vscodesettings = VSCodeSettings(root_path=path)
    print vscodesettings.environment