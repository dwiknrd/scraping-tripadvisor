import sys
import csv #This package lets us save data to a csv file
from selenium import webdriver #The Selenium package we'll need
import time
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/Users/macbook/Documents/chromedriver', options=options)

# default path to file to store data
path_to_file = "universal_studios.csv"

# default number of scraped pages
from_page = 6
num_page = 206
# Open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)
# csvWriter.writerow(['reviewer', 'rating', 'written_date', 'title', 'review_text', 'branch'])
print('disini1')

# change the value inside the range to save more or less reviews
for i in range(from_page, num_page):
    print(f'halaman ke-{i+1}')

    # default tripadvisor website
    # url = f'https://www.tripadvisor.com/Attraction_Review-g34515-d102432-Reviews-or{i}0-Universal_Studios_Florida-Orlando_Florida.html'
    url = f"https://www.tripadvisor.com/Attraction_Review-g294264-d2439664-Reviews-or{i}0-Universal_Studios_Singapore-Sentosa_Island.html"
    # url = f"https://www.tripadvisor.com/Attraction_Review-g298566-d320976-Reviews-or{i}0-Universal_Studios_Japan-Osaka_Osaka_Prefecture_Kinki.html"
    # if you pass the inputs in the command line
    if (len(sys.argv) == 4):
        path_to_file = sys.argv[1]
        num_page = int(sys.argv[2])
        url = sys.argv[3]

    # Import the webdriver
    driver.get(url)
    # expand the review 
    time.sleep(5)
    element = driver.find_element_by_xpath("(//span[contains(@class, 'DrjyGw-P _1l3JzGX1')])")
    driver.execute_script("arguments[0].click();", element)

    first_container = driver.find_element_by_xpath(".//div[@class='_1c8_1ITO']")
    container = first_container.find_elements_by_xpath("./*")

    # print(container[10].get_attribute('innerHTML'))
    # print(len(container))

    for j in range(len(container)-1):
        reviewer = container[j].find_element_by_xpath(".//a[@class='_7c6GgQ6n _37QDe3gr WullykOU _3WoyIIcL']").text
        # visit_date = container[j].find_element_by_xpath(".//div[@class='_3JxPDYSx']").text
        rating = container[j].find_element_by_class_name('zWXXYhVR').get_attribute("title").split(" ")[0]
        written_date = container[j].find_element_by_xpath(".//div[contains(@class, 'DrjyGw-P _26S7gyB4 _1z-B2F-n _1dimhEoy')]").text.replace("Written", "")
        # reviewer_location = container[j].find_element_by_xpath(".//div[@class='DrjyGw-P _26S7gyB4 NGv7A1lw _2yS548m8 _2cnjB3re _1TAWSgm1 _1Z1zA2gh _2-K8UW3T _1dimhEoy']").text
        title = container[j].find_element_by_xpath(".//span[@class='_2tsgCuqy']").text
        text_review = container[j].find_element_by_xpath(".//div[@class='DrjyGw-P _26S7gyB4 _2nPM5Opx']")
        review_text = text_review.find_element_by_xpath(".//span[@class='_2tsgCuqy']").text.replace("\n", " ")
        # branch = "Universal Studios Florida"
        branch = "Universal Studios Singapore"
        # branch = "Universal Studios Japan"
        
        csvWriter.writerow((reviewer,
                            rating,
                            written_date,
                            title,
                            review_text,
                            branch)) 
    print('disini5')

driver.close()