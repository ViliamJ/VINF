import csv
import time

import ray
import scrapy
from scrapy.crawler import CrawlerProcess

from logic.data_extractor import *
from vinf_airplanes.vinf_airplanes.spiders.spider_one import SpiderOne

from fuzzywuzzy import fuzz
from fuzzywuzzy import process




if __name__ == "__main__":

    print("\nWelcome to the nature center. What would you like to do?")

    choice = ''

    while choice != 'q':
        print("\n[1] Enter 1 to initialize SipderOne and donwload data.")
        print("[2] Enter 2 test data")
        print("[3] Enter 3 to compare speed of two airplanes")
        print("[4] Enter 4 to extract data from every file to .csv")
        print("[q] Enter q to quit.")

        choice = input("\nWhat would you like to do? ")

        if choice == '1':
            process = CrawlerProcess()
            process.crawl(SpiderOne)
            process.start()

        elif choice == '2':
            airplane_name = input("Please enter airplane name:")
            data = smart_extract(airplane_name)
            print(data)

        elif choice == '3':
            first_airplane_name = input("Please enter first Airplane name:")
            second_airplane_name = input("Please enter second Airplane name:")
            compare_airplanes(first_airplane_name, second_airplane_name)


        elif choice == '4':

            rootdir = "data/"
            start_time = time.time()

            for root, dirs, files in os.walk(rootdir):
                for file in files:
                    print(file)
                    data_dict = single_extract(file)
                    if data_dict["error"] != 1:
                        csv_file = open("result.csv", "a", encoding="UTF-8")

                        for key in data_dict.keys():
                            csv_file.write("%s,%s" % (key, data_dict[key]))

                        csv_file.close()
            print("--- %s seconds ---" % (time.time() - start_time))

        elif choice == '5':
            rootdir = "data/"

            ray.init(address='auto', _node_ip_address='192.168.1.18')
            # ray.init(address="ray://192.168.1.27:10001")
            start_time = time.time()

            futures = [ray_extract.remote(file) for file in os.listdir("data/")]
            data = ray.get(futures)

            ray_csv_file = open("result_ray.csv", "a", encoding="UTF-8")
            for item in data:
                ray_csv_file.write("%s\n" % item)

            ray_csv_file.close()
            ray.shutdown()

            print("--- %s seconds ---" % (time.time() - start_time))

        elif choice == '6':
            rootdir = "data/"

            ray.init(address='auto', _node_ip_address='192.168.1.18')

            # ray.init(address="ray://192.168.1.27:10001")
            start_time = time.time()

            file_list = []
            for file in os.listdir("data/"):
                file_list.append(file)

            file_list_first_half = file_list[:len(file_list) // 2]
            file_list_second_half = file_list[len(file_list) // 2:]

            chunk_size = int(input("Input number of Cores:"))
            chunked_list = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]



            # data = ray.get(test.remote(file_list))

            ray_functions_ids = []

            # result_ids.append(search_through_files.remote(file_list_first_half))
            # result_ids.append(search_through_files.remote(file_list_second_half))

            for list_chunk in chunked_list:
                ray_functions_ids.append(search_through_files.remote(list_chunk))

            print("something is happening")
            # Wait for the tasks to complete and retrieve the results.
            # With at least 4 cores, this will take 1 second.
            data = ray.get(ray_functions_ids)
            print("something is happening again")

            ray_csv_file = open("result_ray_test.csv", "a", encoding="UTF-8")
            for item in data:
                ray_csv_file.write("%s\n" % item)

            ray_csv_file.close()
            ray.shutdown()

            print("--- %s seconds ---" % (time.time() - start_time))
        elif choice == 'q':
            pass
        else:
            print("\nI don't understand that choice, please try again.\n")

    # Print a message that we are all finished.
    print("Thanks again, bye now.")
