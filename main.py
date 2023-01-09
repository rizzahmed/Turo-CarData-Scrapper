from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time
import datetime
import csv

print("\nExecuting Script...")

# Class
class Procedure:
    def __init__(self, driver):
        self.driver = driver
        
    def process_data(self, areaFile, filterFile):
        pass


# ----------------- FUNCTIONS -----------------
def convert24(str1):
	if str1[-2:] == "AM" and str1[:2] == "12":
		return "00" + str1[2:-2]
	elif str1[-2:] == "AM":
		return str1[:-2]

	elif str1[-2:] == "PM" and str1[:2] == "12":
		return str1[:-2]
	else:
		return str(int(str1[:2]) + 12) + str1[2:8]

def removeCharachters(List, removables, replaceFrom, replaceWith):
    filteredList = []
    for str in List:
        for i in removables:
            str = str.replace(i,"")
        # filteredList.append(str.replace(" ",'%2C%20'))
        filteredList.append(str.replace(replaceFrom,replaceWith))
    return filteredList

def dataScrapper(obj):
    # for i in range(1,r+1):
    obj.get("www.google.com")

def generateCSV():
    pass
    
# Data Gathering Process
areas = ''
URLS = []
try:
    # Reading Area
    with open('area.txt') as a:
        areas = a.readlines()
        if len(areas) >=1:
            areas = removeCharachters(areas, [",","\n"]," ",'%2C%20')
            # print(areas)
            # Reading Filters and BUilding URL
            with open('filter.txt') as f:
                filters = f.readlines()
                if len(filters) == 4:
                    timee = []
                    for f in filters:
                        timeIndex = f.find(":")  
                        data = f[timeIndex+1:].strip()
                        if "-" in data:
                            timee.append(data.replace("-","%2F")) #01%2F13%2F2023
                        elif " " in data or ":" in data:
                            if "PM" in data:
                                data = convert24(data).replace("PM","").strip()
                                timee.append(data.replace(":","%3A"))
                            elif "AM" in data:
                                data = convert24(data).replace("AM","").strip()
                                timee.append(data.replace(":","%3A"))
                    # Filtered Time
                    # print(timee)

                    # Creating URL
                    for a in areas:
                        URLS.append(f'https://turo.com/us/en/search?delivery=false&deliveryLocationType=googlePlace&endDate={timee[2]}&endTime={timee[3]}&location={a}&locationType=ADDRESS&startDate={timee[0]}&startTime={timee[1]}') 
                    
                    print("URL Created")
                    print(URLS)
                else:
                    print("Enter time properly")
        else:
            print("area.txt file can't be empty")    
except Exception as e: print(e)

# Chrome Operation Process
try:
    # Chrome Driver Path ↓
    exe_path = r"D:\MyData\Selenium Driver\chromedriver_win32\chromedriver.exe"
    opt = Options()
    opt.add_experimental_option("detach", True) #to keep browser open after operations
    browser = webdriver.Chrome(executable_path=exe_path,options=opt) #,chrome_options=opt) 
    wait=WebDriverWait(browser,25)
    browser.maximize_window()
    time.sleep(2)
except Exception as e:
    print(e)
    browser.quit()


# Iterating URL List to Fetch Data
data = {}
area_data = {}
car_detailes = {}
areas = removeCharachters(areas, [",","\n"],'%2C%20',' ') 
grid_view = False
list_view = False
grid_numberOfCars = ''
list_numberOfCars = ''

for index, url in enumerate(URLS):
    try:
        browser.get(url)
        print("\nWAIT FOR A MOMENT")
        try:
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div')))
            element = browser.find_element(By.XPATH, '//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div').text
            # print(element)
            print("Grid View")
            grid_view = True
            grid_numberOfCars = int(input("Number of Cars you want to scrape: "))
            if grid_numberOfCars <=5:
                for i in range(1,grid_numberOfCars+1):
                    # print(i)
                    #Name
                    res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div[1]/div/div[{i}]/div/div/a/div[1]/div[2]/div[1]').text
                    car_detailes["Name"] = res

                    #Rate
                    try:
                        res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div[1]/div/div[{i}]/div/div/a/div[2]/div/div[2]/span[2]').text
                        car_detailes["Rate"] = res
                    except:
                        res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div[1]/div/div[{i}]/div/div/a/div[2]/div/div/span').text
                        car_detailes["Rate"] = res

                    #Trip
                    res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div[1]/div/div[{i}]/div/div/a/div[1]/div[2]/div[2]/div/div/p').text
                    car_detailes["Trip"] = res
                    
                    #URL
                    res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div[1]/div/div[{i}]/div/div/a')
                    car_detailes["URL"] = res.get_attribute('href')

                    area_data[i] = car_detailes.copy() #if not copy it will overwrite
            else:
                print("Large data...\n")
                browser.execute_script("window.scrollTo(0, 200);")
                time.sleep(2)
        except:
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div/p[1]')))
            element = browser.find_element(By.XPATH, '//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div/p[1]').text
            # print(element)
            print("List View")
            list_view = True
            list_numberOfCars = int(input("Number of Cars you want to scrape: "))
            if list_numberOfCars <=2:
                for i in range(1,list_numberOfCars+1):
                    # print(i)
                    #Name
                    res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/a/div/div[2]/div[1]/div[1]/div').text
                    car_detailes["Name"] = res

                    #Rate
                    try:
                        res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/a/div/div[2]/div[2]/div/div/span[2]').text
                        car_detailes["Rate"] = res
                    except:
                        res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/a/div/div[2]/div[2]/div/div/span').text
                        car_detailes["Rate"] = res

                    #Trip
                    res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/a/div/div[2]/div[1]/div[2]/div/div/p').text
                    car_detailes["Trip"] = res
                    
                    #URL
                    res = browser.find_element(By.XPATH, f'//*[@id="pageContainer-content"]/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/a')
                    car_detailes["URL"] = res.get_attribute('href')

                    area_data[i] = car_detailes.copy() #if not copy it will overwrite
            else:
                print("large data")
                browser.execute_script("window.scrollTo(0, 200);")
                time.sleep(2)

        data[areas[index]] = area_data.copy()

    except Exception as e: print(e)

print("\n")
print(data)
print("\n")



row = ["Name","Rate Per Day","Trip","URL Link"]

# open the file in the write mode
with open('data.csv', 'w') as f:

    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow(row)

    for area in areas:
        areaName = area.split()
        writer.writerow(areaName)
        if grid_view:
            for i in range(1,grid_numberOfCars+1):
                
                ls = list(data[area][i].values())
                writer.writerow(ls)
        elif list_view:
            for i in range(1,list_numberOfCars+1):
                
                ls = list(data[area][i].values())
                writer.writerow(ls)     

print("Code Finished")