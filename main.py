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
        print("[q] Enter q to quit.")

        choice = input("\nWhat would you like to do? ")

        if choice == '1':
            process = CrawlerProcess()
            process.crawl(SpiderOne)
            process.start()

        elif choice == '2':
            airplane_name = input("Please enter airplane name:")
            extract(airplane_name)

        elif choice == '3':
            first_airplane_name = input("Please enter first Airplane name:")
            second_airplane_name = input("Please enter second Airplane name:")
            compare_airplanes(first_airplane_name, second_airplane_name)

            pass
        elif choice == 'q':
            pass
        else:
            print("\nI don't understand that choice, please try again.\n")

    # Print a message that we are all finished.
    print("Thanks again, bye now.")
