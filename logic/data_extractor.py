import os
import re

import ray
from fuzzywuzzy import fuzz
from fuzzywuzzy import process



def single_extract(file):
    data = {}
    kmph = 0
    different_kmph = 0

    # if regex.match(file):

    seareched_file = open(f'data/{file}', "r", encoding="UTF-8")

    opened_file = seareched_file.read()

    # Regular expressions
    title_regex = re.compile('<title>(.+)<\/title>')

    title = re.findall(title_regex, opened_file)
    max_speed_regex = re.compile('<li><b>Maximum speed:<\/b> (.*)<\/li>')

    max_speed_answer = re.findall(max_speed_regex, opened_file)

    if max_speed_answer:
        kmph = re.findall("([0-9]+)&#160;km\/h", max_speed_answer[0])
        mph = re.findall("([0-9]+)&#160;mph", max_speed_answer[0])

    if not max_speed_answer:
        new_max_speed = re.findall(r"max. (.+)km\/h", opened_file)
        if new_max_speed:
            if "&#160;" in new_max_speed[0]:
                striped_max_speed = new_max_speed[0].replace("&#160;", "")

                different_kmph = striped_max_speed

    if kmph != 0 and kmph != []:
        data = {
            "airplane_title": title,
            "max_speed_kmph": max(kmph),
            "error": 0
        }

    elif different_kmph != 0:
        data = {
            "airplane_title": title,
            "max_speed_kmph": different_kmph,
            "error": 0
        }
    else:
        data = {
            "airplane_title": title,
            "error": 1
        }

    seareched_file.close()

    return data

@ray.remote
def ray_extract(file):
    data = {}
    kmph = 0
    different_kmph = 0

    # if regex.match(file):

    seareched_file = open(f'data/{file}', "r", encoding="UTF-8")

    opened_file = seareched_file.read()

    # Regular expressions
    title_regex = re.compile('<title>(.+)<\/title>')

    title = re.findall(title_regex, opened_file)
    max_speed_regex = re.compile('<li><b>Maximum speed:<\/b> (.*)<\/li>')

    max_speed_answer = re.findall(max_speed_regex, opened_file)

    if max_speed_answer:
        kmph = re.findall("([0-9]+)&#160;km\/h", max_speed_answer[0])
        mph = re.findall("([0-9]+)&#160;mph", max_speed_answer[0])

    if not max_speed_answer:
        new_max_speed = re.findall(r"max. (.+)km\/h", opened_file)
        if new_max_speed:
            if "&#160;" in new_max_speed[0]:
                striped_max_speed = new_max_speed[0].replace("&#160;", "")

                different_kmph = striped_max_speed

    if kmph != 0 and kmph != []:
        data = {
            "airplane_title": title,
            "max_speed_kmph": max(kmph),
            "error": 0
        }

    elif different_kmph != 0:
        data = {
            "airplane_title": title,
            "max_speed_kmph": different_kmph,
            "error": 0
        }
    else:
        data = {
            "airplane_title": title,
            "error": 1
        }

    seareched_file.close()

    return data



def smart_extract(input_airplane_name):
    data = {}
    kmph = 0
    different_kmph = 0

    # '([0-9]+)-(.+)_([0-9]+)-([0-9]+)(.html$)|([0-9]+)-((.+)_*)([0-9]+)(.html$)'

    rootdir = "data/"
    # regex = re.compile(f'(.*zip$)|(.*rar$)|(.*r01$)')
    regex = re.compile(f'([0-9]+)-{input_airplane_name}(.html$)')

    file_list = []

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            file_ratio = fuzz.ratio(file, input_airplane_name)
            name_ratio_tuple = (file, file_ratio)
            file_list.append(name_ratio_tuple)

    max_file = max(file_list, key=lambda tup: tup[1])
    print("toto je max_file:")
    print(max_file)

    # if regex.match(file):

    seareched_file = open(f'data/{max_file[0]}', "r", encoding="UTF-8")

    opened_file = seareched_file.read()

    # Regular expressions
    title_regex = re.compile('<title>(.+)<\/title>')

    title = re.findall(title_regex, opened_file)
    max_speed_regex = re.compile('<li><b>Maximum speed:<\/b> (.*)<\/li>')

    max_speed_answer = re.findall(max_speed_regex, opened_file)

    if max_speed_answer:
        print(max_speed_answer)
        kmph = re.findall("([0-9]+)&#160;km\/h", max_speed_answer[0])

        mph = re.findall("([0-9]+)&#160;mph", max_speed_answer[0])

    if not max_speed_answer:
        new_max_speed = re.findall(r"max. (.+)km\/h", opened_file)
        if new_max_speed:
            if "&#160;" in new_max_speed[0]:
                striped_max_speed = new_max_speed[0].replace("&#160;", "")

                different_kmph = striped_max_speed

    if kmph != 0 and kmph != []:
        data = {
            "airplane_title": title,
            "max_speed_kmph": max(kmph),
            "error": 0
        }

    elif different_kmph != 0:
        data = {
            "airplane_title": title,
            "max_speed_kmph": different_kmph,
            "error": 0
        }
    else:
        data = {
            "airplane_title": title,
            "error": 1
        }

    seareched_file.close()
    return data


def compare_airplanes(airplane_1, airplane_2):
    a1_data = smart_extract(airplane_1)
    a2_data = smart_extract(airplane_2)

    a1_title = a1_data["airplane_title"]
    a2_title = a2_data["airplane_title"]

    if a1_data["error"] == 1:
        print(f"Sorry, error occured ! \n For {a1_title} there could not be found maximum aircraft speed")

    if a2_data["error"] == 1:
        print(f"Sorry, error occured ! \n For {a2_title} there could not be found maximum aircraft speed")

    if a1_data["error"] == 0 and a2_data["error"] == 0:

        a1_speed = a1_data['max_speed_kmph']
        a2_speed = a2_data['max_speed_kmph']

        if a1_speed > a2_speed:

            print(f"Airplane 1: {a1_title}")
            print(f"Airplaine 1 speed: {a1_speed} km/h")
            print("\n")
            print(f"Airplane 2: {a2_title}")
            print(f"Airplaine 2 speed: {a2_speed} km/h")

            print(f"Airplane {a1_title} is faster than {a2_title} by {int(a1_speed) - int(a2_speed)} km/h ")
            print(f"Airplane {a1_title} WON")
        elif a1_speed < a2_speed:

            print(f"Airplane 1: {a1_title}")
            print(f"Airplaine 1 speed: {a1_speed} km/h")
            print("\n")
            print(f"Airplane 2: {a2_title}")
            print(f"Airplaine 2 speed: {a2_speed} km/h")

            print(f"Airplane {a2_title} is faster than {a1_title} by {int(a2_speed) - int(a1_speed)} km/h ")
            print(f"Airplane {a2_title} WON")
        elif a1_speed == a2_speed:
            print(f"Airplane 1: {a1_title}")
            print(f"Airplaine 1 speed: {a1_speed} km/h")
            print("\n")
            print(f"Airplane 2: {a2_title}")
            print(f"Airplaine 2 speed: {a2_speed} km/h")

            print("Wow ? Max air speeds are identical.")
