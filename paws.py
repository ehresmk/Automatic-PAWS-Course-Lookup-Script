#
# CSC 360 Project 1
# Email & Web Scraping with Python
# Kevin Ehresman
# Mark Boutros
# 10/14/19
#

from selenium import webdriver
import datetime
import time
import sys
from selenium.webdriver.common.keys import Keys
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

#replace username/password with yours
#Do not share your credential with anyone!!!
ACCOUNTS = {
    "user":"pass"
}

URL = 'https://paws.tcnj.edu/'
# login webpage
LOGIN_INI = 'https://paws.tcnj.edu/psp/paws/?cmd=login&languageCd=ENG&'
# after login webpage
# you need to change this URL. The current one is for faculty.
# URL not changed because it was the same one I got
LOGIN_URL = 'https://paws.tcnj.edu/psp/paws/EMPLOYEE/SA/h/?tab=DEFAULT'
StartingTime = '2019-08-16 10:07:10'

def searchCourse(driver, user, programName, courseN):
    # wait for paws page to load
    time.sleep(2)
    
    #Finds the student center link and then clicks it
    Student_Center = driver.find_element_by_xpath('//*[text()="Student Center"]')
    time.sleep(2)
    Student_Center.click()
    
    #Switches the frame in order to find the Search link
    time.sleep(2)
    frame = driver.find_element_by_xpath("//iframe[@name='TargetContent']")
    driver.switch_to.frame(frame)
    #Finds the search link and then clicks it
    search = driver.find_element_by_partial_link_text("Search")
    time.sleep(2)
    search.click()
    time.sleep(2)
    
    #Resets and then sets the frame
    driver.switch_to.default_content()
    frame = driver.find_element_by_xpath("//iframe[@name='TargetContent']")
    driver.switch_to.frame(frame)
    #Sets the semester to the current one
    semester = driver.find_element_by_xpath('//select[@id = "CLASS_SRCH_WRK2_STRM$35$"]//option[@value="1198"]')
    time.sleep(2)
    semester.click()
    time.sleep(2)
    
    #Finds the subject dropdown box and sets the class subject from the command line
    subject = driver.find_element_by_xpath('//select[@id = "SSR_CLSRCH_WRK_SUBJECT_SRCH$0"]//option[@value="'+programName.upper()+'"]')
    time.sleep(2)
    subject.click()
    time.sleep(2)
    #Finds the textbox for the class number and inputs the class number from command line
    number = driver.find_element_by_xpath('//*[@id = "SSR_CLSRCH_WRK_CATALOG_NBR$1"]')
    number.send_keys(courseN)
    time.sleep(2)
    
    #Sets open classes checkbox
    check = driver.find_element_by_xpath('//*[@id = "SSR_CLSRCH_WRK_SSR_OPEN_ONLY$3"]')
    check.click()
    time.sleep(2)
    #Finds the career dropdown and sets it to "Undergraduate"
    career = driver.find_element_by_xpath('//select[@id = "SSR_CLSRCH_WRK_ACAD_CAREER$2"]//option[@value="UGRD"]')
    time.sleep(1)
    career.click()
    time.sleep(2)
    
    #Finds the Search button then clicks it
    class_search = driver.find_element_by_xpath('//*[@id = "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"]')
    time.sleep(2)
    class_search.click()
    time.sleep(2)
    
    #Gets number of found sections
    try:
        sections = driver.find_element_by_xpath('//div[@id="win0divSSR_CLSRSLT_WRK_GROUPBOX1"]//td[@class="PSGROUPBOXLABEL"]')
        sections = sections.text[:sections.text.find(" ")]
    except:
        print("================No Matches===============")
        return 0
    
    #Sets data into Beautiful Soup
    data = BeautifulSoup(driver.page_source)
    table = data.findChildren("table", id="ACE_$ICField$4$$0")
    
    #Loops through and prints Open Sections
    print("\n================Open Sections===================\n")
    for i in range (int(sections)):
        
        #Parses data for status
        class_status = str(table[0].findChildren("div", id="win0divDERIVED_CLSRCH_SSR_STATUS_LONG${}".format(i)))
        #class_status = str(class_status)
        temp_hold = class_status[class_status.find("alt")+5:]
        class_status = temp_hold[0:temp_hold.find("\"")]
        
        if(class_status == "Open"):
            #Parses data for Class Number
            class_number = str(table[0].findChildren("a", id="MTG_CLASS_NBR${}".format(i)))
            #class_number = str(class_number)
            class_number = (class_number[class_number.find(">")+1:len(class_number)-5])
        
            #Parses data for class Times
            class_time = str(table[0].findChildren("span", id="MTG_DAYTIME${}".format(i)))
            #class_time = str(class_time)
            class_time = class_time[class_time.find(">")+1:class_time.find("</span>")]
            class_time = class_time.replace("<br/>", "")
            
        
            #Parses data for Instructor
            class_instr = str(table[0].findChildren("span", id="MTG_INSTR${}".format(i)))
            #class_instr = str(class_instr)
            class_instr = class_instr.replace("</span>", "")
            class_instr = (class_instr[class_instr.find(">")+1:class_instr.find("<br/>")])
            
            print(class_number)
            print(class_time)
            print(class_instr)

            print("\n")
            
    #Loops through and prints Closed Sections
    print("\n================Closed Sections===================\n")
    for i in range (int(sections)):
          #Parses data for status
        class_status = table[0].findChildren("div", id="win0divDERIVED_CLSRCH_SSR_STATUS_LONG${}".format(i))
        class_status = str(class_status)
        temp_hold = class_status[class_status.find("alt")+5:]
        class_status = temp_hold[0:temp_hold.find("\"")]
        
        if(class_status == "Closed"):
            
            #Parses data for Class Number
            class_number = table[0].findChildren("a", id="MTG_CLASS_NBR${}".format(i))
            class_number = str(class_number)
            class_number = (class_number[class_number.find(">")+1:len(class_number)-5])
        
            #Parses data for class Times
            class_time = table[0].findChildren("span", id="MTG_DAYTIME${}".format(i))
            class_time = str(class_time)
            class_time = class_time[class_time.find(">")+1:class_time.find("</span>")]
            class_time = class_time.replace("<br/>", "")
            
        
            #Parses data for Instructor
            class_instr = table[0].findChildren("span", id="MTG_INSTR${}".format(i))
            class_instr = str(class_instr)
            class_instr = class_instr.replace("</span>", "")
            class_instr = (class_instr[class_instr.find(">")+1:class_instr.find("<br/>")])
            
            print(class_number)
            print(class_time)
            print(class_instr)

            print("\n")
        

    
    
    
# Funtion to login
def login(user,pwd, programName, courseN):
    driver = webdriver.Chrome()
    driver.get(URL)
    LoginStat = False
    while True:
        time.sleep(0.05)
        if LOGIN_INI == driver.current_url:
           print("Opening...")
           break
    try:
        loginForm = driver.find_element_by_xpath('//*[@id="userid"]')
        #longinForm.click()
        loginForm.send_keys(user)
        #time.sleep(1)
        print('send username')
        passwordForm = driver.find_element_by_xpath('//*[@id="pwd"]')
        passwordForm.click()
        passwordForm.send_keys(pwd)
        submit = driver.find_element_by_xpath('//*[@name="submit"]')
        submit.click()
        print(user + " login in process...")
    except:
        print(user + " input error")

    while True:
        time.sleep(0.05)
        if LOGIN_URL == driver.current_url :
           print(user + " login succeed")
           break
               #time.sleep(5)
    searchCourse(driver, user, programName, courseN)

if __name__ == "__main__":
    # username & passwords
    data = ACCOUNTS
    # argument sys.argv[1] is discipline name, such as CSC, MAT, BIO, csc, bio ...
    # argument sys.argv[2] is course number, such as 220, 230, 250, 360
    
    # build threads
    threads = []
    for account, pwd in data.items():
        t = Thread(target=login,args=(account,pwd, sys.argv[1], sys.argv[2]))
        threads.append(t)
    for thr in threads:
        time.sleep(0.05)
        thr.start()

