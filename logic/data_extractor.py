import os
import re

import ray
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def fuzzy_name_function(input_list, searched_item):
    """
        This function is used for approximating a word or a string by calculating _ratio of approximation
        for example words :  hello1 and hello11 should be approximatly 0.90 close (1.0 - would be exact match)


        @:param range_ratio: is a number calculeted by fuzz library from two input strings
        @:param ratio_list: list which stores all tupels of range_tuple
        @:param item_name: extracting from the list of tuples best match by max() function

        :returns item_name[0]: returns the first index of the tuple, which is the name string

    """
    ratio_list = []
    for item in input_list:
        range_ratio = fuzz.ratio(item, searched_item)
        range_tuple = (item, range_ratio)
        ratio_list.append(range_tuple)

    item_name = max(ratio_list, key=lambda tup: tup[1])

    return item_name[0]

def single_extract(file):
    '''
    This function extracts data from a file based on regular expression searching through whole file.
    If there is a match it will save the searched expression to data{} dictionary

    :param file: is the name of the input file we are goint to extract from
    :return: data: is a dictionary of extracted data
    '''

    data = {}
    kmph = 0
    different_kmph = 0


    seareched_file = open(f'data/{file}', "r", encoding="UTF-8")

    opened_file = seareched_file.read()

    # Regular expression for title
    title_regex = re.compile('<title>(.+)<\/title>')

    title = re.findall(title_regex, opened_file)

    # Regular expression for finding maximum airplane speed
    max_speed_regex = re.compile('<li><b>Maximum speed:<\/b> (.*)<\/li>')

    max_speed_answer = re.findall(max_speed_regex, opened_file)

    # If clause with Regexe's in case there is no "Maximum speed". So trying to find it different way
    if max_speed_answer:
        kmph = re.findall("([0-9]+)&#160;km\/h", max_speed_answer[0])
        mph = re.findall("([0-9]+)&#160;mph", max_speed_answer[0])

    # If clause with Regexe's in case there is no "Maximum speed". So trying to find it different way
    if not max_speed_answer:
        new_max_speed = re.findall(r"max. (.+)km\/h", opened_file)
        if new_max_speed:
            if "&#160;" in new_max_speed[0]:
                striped_max_speed = new_max_speed[0].replace("&#160;", "")

                different_kmph = striped_max_speed

    # filling up the dictionary with data, IF clauses here ensure if it can be filled up
    if kmph != 0 and kmph != []:
        data = {
            "File_name": file,
            "airplane_title": title,
            "max_speed_kmph": max(kmph),
            "error": 0
        }

    elif different_kmph != 0:
        data = {
            "File_name": file,
            "airplane_title": title,
            "max_speed_kmph": different_kmph,
            "error": 0
        }
    else:
        data = {
            "File_name": file,
            "airplane_title": title,
            "error": 1
        }

    seareched_file.close()

    # Regular expression for finding the flight range of the airplane
    range_km_regex = re.findall("<b>Range:<\/b>(.+?)(?=&#160;)", opened_file)

    # Tyding up the found range, if it even exists.
    if range_km_regex:
        range_km_regex[0] = range_km_regex[0].strip()
        range_km_regex[0] = range_km_regex[0].replace(",", "")
        data["range_km"] = range_km_regex[0]
    elif not range_km_regex:
        range_km_regex = re.findall("([0-9]*,[0-9]*)&#160;km", opened_file)

        if range_km_regex != []:
            for i, item in enumerate(range_km_regex):
                range_km_regex[i] = range_km_regex[i].replace(",", "") # getting rid of comma in case finding numbers like 1,200 km
            max_range = max(range_km_regex)

            data["range_km"] = max_range

    else:
        data["range_km"] = None


    return data


# This function is the first iteration of code, it uses fuzzy searching by airplane names
def smart_extract(input_airplane_name):
    """
    This function was first during the semester while we were working on this project.
    However, its purpose is still to extract desired data from a html file.

    @:param input_airplane_name: Is the name of airplane in string form
    :return: data: dict{} of extracted data from files
    """
    data = {}
    kmph = 0
    different_kmph = 0


    rootdir = "data/"

    file_list = []

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            file_ratio = fuzz.ratio(file, input_airplane_name)
            name_ratio_tuple = (file, file_ratio)
            file_list.append(name_ratio_tuple)

    max_file = max(file_list, key=lambda tup: tup[1])
    print("toto je max_file:")
    print(max_file)


    seareched_file = open(f'data/{max_file[0]}', "r", encoding="UTF-8")

    opened_file = seareched_file.read()

    # Regular expression for title
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
            "File_name": max_file,
            "airplane_title": title,
            "max_speed_kmph": max(kmph),
            "error": 0
        }

    elif different_kmph != 0:
        data = {
            "File_name": max_file,
            "airplane_title": title,
            "max_speed_kmph": different_kmph,
            "error": 0
        }
    else:
        data = {
            "File_name": max_file,
            "airplane_title": title,
            "error": 1
        }

    seareched_file.close()
    return data


def compare_airplanes(airplane_1, airplane_2):
    """
    Comparing two airplanes based on their values extracted from smart_extract()

    param airplane_1: string, name of airplane
    :param airplane_2: string, name of airplane
    :return:
    """
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


@ray.remote
def search_through_files(file_list):
    """
    This function is a @ray.remote decorated function meaning that RAY will be handling
    the functionality and calculations.



    @:param file_list: list of saved files of type  .html
    :return: dataset: list of data extracted from single_extract()
    """
    dataset = []

    for file in file_list:
        dataset.append(single_extract(file))

    return dataset
