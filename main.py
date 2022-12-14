import csv
import time

import ray
import scrapy
from scrapy.crawler import CrawlerProcess

from logic.data_extractor import *
from vinf_airplanes.vinf_airplanes.spiders.spider_one import SpiderOne

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import pandas as pd
import pyspark
from pyspark.sql import SparkSession

if __name__ == "__main__":

    print("\nWelcome to the nature center. What would you like to do?")

    choice = ''

    while choice != 'q':
        print("\n[1] Enter 1 to initialize SipderOne and donwload data.")
        print("[2] Enter 2 test data")
        print("[3] Enter 3 to compare speed of two airplanes")
        print("[4] Enter 4 to extract data from every file to .csv")
        print("[6] Enter 6 to extract data from every file to .csv with RAY cluster")
        print("[7] Enter 7 to SPARK search from .CSV file")
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

            rootdir = "data2/"
            start_time = time.time()

            csv_file = open("final_result_sequential.csv", "w", encoding="UTF-8")
            field_names = ['File_name', 'airplane_title', 'max_speed_kmph', 'error', 'range_km']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()

            for root, dirs, files in os.walk(rootdir):
                for file in files:
                    print(file)

                    data_dict = single_extract(file)
                    print(data_dict)

                    writer.writerows([data_dict])

                    # if data_dict["error"] != 1:
                    # csv_file.write("%s\n" % data_dict)

            csv_file.close()
            print("--- %s seconds ---" % (time.time() - start_time))




        # elif choice == '5':
        #    rootdir = "data/"
        #
        #    ray.init(address='auto', _node_ip_address='192.168.1.18')
        #    # ray.init(address="ray://192.168.1.27:10001")
        #    start_time = time.time()
        #
        #    futures = [ray_extract.remote(file) for file in os.listdir("data/")]
        #    data = ray.get(futures)
        #
        #    ray_csv_file = open("result_ray.csv", "a", encoding="UTF-8")
        #    for item in data:
        #        ray_csv_file.write("%s\n" % item)
        #
        #    ray_csv_file.close()
        #    ray.shutdown()
        #
        #    print("--- %s seconds ---" % (time.time() - start_time))

        elif choice == '6':
            rootdir = "data/"

            runtime_env = {"working_dir": "./", "excludes": ["/data/"]}
            ray.init(address='auto', _node_ip_address='192.168.1.18', runtime_env=runtime_env)

            # ray.init(address="ray://192.168.1.27:10001")
            chunk_size = int(input("Input number of Cores:"))
            start_time = time.time()

            file_list = []
            for file in os.listdir(rootdir):
                file_list.append(file)

            # file_list_first_half = file_list[:len(file_list) // 2]
            # file_list_second_half = file_list[len(file_list) // 2:]

            # Rozloženie listu súborov na viaceré rovnako veľké listy (napr. 1 na 2 listy)
            chunked_list = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]

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

            # ray_csv_file = open("result_ray.csv", "a", encoding="UTF-8")

            ray_csv_file = open("final_result_ray.csv", "a", encoding="UTF-8")
            field_names = ['File_name', 'airplane_title', 'max_speed_kmph', 'error']
            writer = csv.DictWriter(ray_csv_file, fieldnames=field_names)
            writer.writeheader()

            for item in data:
                writer.writerows(item)
                # ray_csv_file.write("%s\n" % item)
            print("--- %s seconds ---" % (time.time() - start_time))
            ray_csv_file.close()
            ray.shutdown()

        elif choice == '7':

            df = pd.read_csv("final_result_ray.csv")
            # print(df.head(5))

            spark = SparkSession.builder.appName('Practise').getOrCreate()

            # df_spark =  spark.read.csv('result_sequential.csv')
            df_spark = spark.read.option('header', 'true').csv('final_result_sequential.csv')
            # print(df_spark.head(5))

            choice2 = ''
            while choice2 != 'q':
                column = input(
                    "Choose column name from ['File_name', 'airplane_title', 'max_speed_kmph', 'error','range_km']:")

                if column == "File_name":
                    searched_item = input("Input searched item:")

                    df_spark.filter(df_spark.File_name == f"{searched_item}").show()
                elif column == "airplane_title":
                    searched_item = input("Input searched item:")
                    df_list_column_airplane_title = [data[0] for data in df_spark.select('range_km').collect()]
                    searched_item_fuzzy = fuzzy_name_function(df_list_column_airplane_title, searched_item)

                    df_spark.filter(df_spark.airplane_title == f"{searched_item_fuzzy}").show()
                elif column == "max_speed_kmph":
                    searched_item = input("Input searched item:")
                    df_list_column_max_speed_kmph = [data[0] for data in df_spark.select('range_km').collect()]
                    searched_item_fuzzy = fuzzy_name_function(df_list_column_max_speed_kmph, searched_item)

                    df_spark.filter(df_spark.max_speed_kmph == f"{searched_item_fuzzy}").show()
                elif column == "range_km":
                    searched_item = input("Input searched item:")

                    df_list_column_range_km = [data[0] for data in df_spark.select('range_km').collect()]
                    searched_item_fuzzy = fuzzy_name_function(df_list_column_range_km, searched_item)

                    df_spark.filter(df_spark.range_km == f"{searched_item_fuzzy}").show()

                choice2 = input("would you like to find another, q to stop ?:")

        elif choice == 'q':
            pass
        else:
            print("\nI don't understand that choice, please try again.\n")

    # Print a message that we are all finished.
    print("Thanks again, bye now.")
