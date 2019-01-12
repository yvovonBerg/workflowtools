import os
import sys
import json
import getpass


def append_project(name, path):
    PROJECTS = "C:\Users\{}\AppData\Roaming\Code\User\projects.json".format(
        getpass.getuser()
    )
    if not os.path.exists(PROJECTS):
        return

    project_data = []
    with open(PROJECTS, 'r') as project_file:
        try:
            project_data = json.load(project_file)
        except ValueError:
            pass
    project_data.append({
        "name": name,
        "rootPath": path,
        "paths": [],
        "group": "",
        "enabled": True
    })
    with open(PROJECTS, 'w') as project_file:
        project_file.write(
            json.dumps(
                project_data, indent=4
            )
        )

if __name__ == "__main__":
    name = sys.argv[1]
    path = sys.argv[2]
    append_project(name, path)