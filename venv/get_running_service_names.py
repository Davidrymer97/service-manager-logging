import subprocess
import os
import json

out = subprocess.Popen(['sm', '-s'],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)

lines = str(out.communicate()).split("\\n")
relevant_lines = lines[5:len(lines) - 2]


def get_name_from_line(line):
    return line.split("|")[1].strip()


def get_service_names():
    return filter(lambda x: x != 'MONGO', map(get_name_from_line, relevant_lines))


def get_location_name(sm_name):
    workspace_path = os.environ['WORKSPACE']

    sm_config_json_path = workspace_path + "/service-manager-config/services.json"

    with open(sm_config_json_path) as json_file:
        data = json.load(json_file)
        try:
            return data[sm_name]["location"][1:]
        except:
            print("location not found for service " + sm_name)


def get_location_names(sm_names):
    return map(get_location_name, sm_names)
