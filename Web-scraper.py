import selenium
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
import json
import keyboard

def main(y):
    global data_list,driver
    data_dic = {}
    url = f"https... url --> eportfolio/{y}/profiles"
    driver.get(url)
    
    #imputs passwword only at the start
    password(y)
    
    #check if rate limited
    rated(y,BeautifulSoup(driver.page_source, 'html.parser'))
    
    #initialises the data dictionary, getting the names year levels and classes
    data_dic = classs(year(name(y,data_dic,BeautifulSoup(driver.page_source, 'html.parser')),BeautifulSoup(driver.page_source, 'html.parser')),BeautifulSoup(driver.page_source, 'html.parser'))

    #if data dictionary exists, append the data to the list
    if len(data_dic) != 0: 
        data_list.append(data_dic)

def saving(data_list):
    with open('eportfolio_data3.json', 'w') as json_file:
        json.dump(data_list, json_file, indent=4)

def start_file(json_file):
    os.system(f'start "" "{json_file}"')

def password(y):
    #if on the first iteration, imput password or pass
    if y==1:
        time.sleep(2)
        keyboard.press('l');time.sleep(.05);keyboard.press('w');time.sleep(.05);keyboard.press('a');time.sleep(.05);keyboard.press('l');time.sleep(.05);keyboard.press('0');keyboard.press('1');time.sleep(2);keyboard.press('tab')
        time.sleep(.5)
        Yep = "Enter binary of password"
        z = [Yep[i:i+8] for i in range(0, len(Yep), 8)]
        bn = ''.join(chr(int(c, 2)) for c in z)
        keyboard.write(bn)
        keyboard.press_and_release('enter')

def rated(y, soup):
    #check if we have been rate limited
    global driver
    while True:
        try:
            rate = soup.find('div', attrs={'id': 'message'})
            if rate.find('h2').text == "You have been rate limited":
                url = f'https... url --> eportfolio/{y}/profiles'#eportfolio profiles = student/teacher
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
            else:
                break   
        except:
            break

def name(y,data_dic,soup):
    global driver
    #gets name
    try:
        name = soup.find('div', class_='wrap')
        namename = name.find('h1').text
        data_dic['number'] = y
        data_dic['name'] = namename
    except:
        try:
            #if we couldn't get the name, go to the user search
            url = f"https... url --> /search/user/{y}"#search user = parent 
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            while True:
                #keep reloading until not rate limited (we are brute forcing it instead of waiting for a timer to ensure min time)
                try:
                    rate = soup.find('div', attrs={'id': 'message'})
                    if rate.find('h2').text == "You have been rate limited":
                        url = f'https... url --> /search/user/{y}'
                        driver.get(url)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                except:
                    #whennot rate limited get the page source from the non rated page, then continute with the code (break)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    parentname = soup.find('div', class_="actions-small-0 row")
                    pname = parentname.find('h1').text
                    data_dic['number'] = y
                    data_dic['name'] = pname
                    break
            try:
                #find the teacher codes
                tr = soup.findAll('dd', class_="small-12 medium-9")
                for i in tr:
                    if len(i.text) == 3:
                        data_dic['Teacher Code'] = i.text
            
                for j in range(len(tr)):
                    #this is where the teacher codes are
                    if tr[j].text == "Brighton":
                        data_dic['Type'] = tr[j-1].text
            except:
                pass

        except:
            pass
    return data_dic

def year(data_dic,soup):
    #gets year level for student
    try:
        year = soup.find('p', class_='meta').text
        year = year.split(',')[0]
        year = year.strip()
        #only if it doesn't say Unfortunately (meaning no year level, maybe teacher or parent)
        if year != "Unfortunately":
            data_dic['Year Level'] = year
    except:
        pass
    return data_dic

def classs(data_dic,soup):
    #get classes for stuednts and teachers 
    IB = False
    VCE = False
    VCE_IB = False
    try:
        #geta all subjects
        all_classes = soup.find_all('div', class_='small-12 island')
        student_subjects = []

        for z in all_classes:
            h = z.find('h2', class_='subheader')
            if h and h.text.strip() == 'My Subjects':
                all_classh3 = z.find_all('h3')
                
                for j in all_classh3:
                    subject = j.text.strip()
                    student_subjects.append(subject)
                
            for subject in student_subjects:
                if subject.startswith("12IB") or subject.startswith("11IB"):
                    #detemrning if this student is an ib or vce student or neither...
                    IB = True
                    break

                elif subject.startswith("VCE"):
                    VCE = True
                    break
                else:
                    VCE_IB = True

        if IB == True:
            data_dic['IB or VCE'] = "IB"
        elif VCE == True:
            data_dic['IB or VCE'] = "VCE"
        elif VCE_IB == True:
            data_dic['IB or VCE'] = "N/A"
        
        if len(student_subjects) != 0:
            #only append if found classes
            data_dic['Subjects'] = student_subjects
    except:
        pass

    return data_dic

def qu():
    global driver
    driver.quit() 

if __name__ == "__main__":
    data_list = []
    json_file = 'eportfolio_data3.json'
    driver = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    for y in range(1, 14_000):
        main(y)
    saving(data_list)
    start_file(json_file)
    qu()
