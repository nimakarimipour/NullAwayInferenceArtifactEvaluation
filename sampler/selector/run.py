import os
import json
import subprocess
from subprocess import Popen, PIPE

# Run with Python2

GIT_RESET = " && git reset --hard && git checkout {} && "
START = "https://github.com/nimakarimipour/"

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


outfilename = "errors.json"
# outfilename = "test.json"
with open('../projects.json') as f:
    projects = json.load(f)
    for project in projects['projects']:
        print("WORKING ON: " + str(project['name']))
        current_errors = json.load(open(outfilename))
        new_errors = []
        project['active'] = True
        if project['active']:
            command = "cd /Users/nima/Developer/ArtifactEvaluation/NullAwayFixer/Projects/" + project['path'] + "/" + GIT_RESET.format(project['branch']) +  project['build']
            print("Command: " + command)
            res = subprocess.Popen(command + " > /dev/null && echo done", shell=True, stderr=PIPE)
            out, err = res.communicate()
            errors = str(err).split("\n")
            errors.pop()
            for i in range(0, len(errors)):
                disp = {}
                if("error: [NullAway]" in errors[i]):
                    line = errors[i]
                    error_url = line[0:line.index("error: [NullAway]")]
                    error_url = error_url[:-2]
                    error_link = START + project['root'] + "/blob/{}".format(project['branch']) + error_url[error_url.index(project['path']) + len(project['path']):]
                    error_link = error_link.replace(".java:", ".java#L")
                    disp['url'] = error_link
                    disp['message'] = line[line.index("error: [NullAway]") + len("error: [NullAway]"):]
                    disp['position'] = errors[i+1].strip()
                    new_errors.append(disp)
                    i += 2
                else:
                    i += 1
            final_out = {}
            final_out['size'] = len(new_errors)
            final_out['errors'] = new_errors
            current_errors['PROJECTS'][project['name']] = final_out
            with open(outfilename, 'w') as outfile:
                json.dump(current_errors, outfile)
                outfile.flush()
                outfile.close()