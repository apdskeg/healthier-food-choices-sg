# -*- coding: utf-8 -*-
"""
Healthier Food Choices for Psych (APD Lab)
Date of the script: Apr 25, 2019
"""

import time, os, copy, threading
from datetime import datetime
from dateutil.relativedelta import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


def available(day,fileFormat):
    if len([ff for ff in os.listdir('%s/Messages/Day %02d' %(path,day)) if ff.endswith(fileFormat)]) != 0: return True
    else: return False

def get_names(ff):
    return [name.strip() for name in open('%s/%s' %(path,ff))]

def get_online_names(ff):
    return [name.strip() for name in open('%s%s' %(path,ff))]

def get_text(day):
    if available(day,'txt'):
        return [line.strip() for line in open('%s/Messages/Day %02d/TextDay%02d.txt' %(path,day,day))]

def get_image(day,condition):
    if available(day,'jpg'):
        return '%s/Messages/Day %02d/%s-Day%02d.jpg' %(path,day,condition,day)

def get_driver():
    '''
    Load driver, specify driver as global var
    Load WhatsApp Web and ask for QR code
    '''
    driver = webdriver.Chrome(executable_path = './chromedriver')
    driver.get('https://web.whatsapp.com/')

    return driver

def daycheck(day):
    if os.path.isdir('%s/Messages/Day %02d' %(path,day)): return True
    else: return False


def send_stuff(condition,name,day):
    global timelogger
    try:
        whatsapp_name=name[4:] 
        search = driver.find_element_by_class_name('_2MSJr')
        search.send_keys(whatsapp_name)
        time.sleep(2)
        findname = driver.find_element_by_xpath('//div[contains(@style,"translateY(72px)")]')
        findname.click()
        user = driver.find_element_by_class_name('_2S1VP')
        user.click()
        print ('searching by "%s"'%whatsapp_name)
        action = None
        timestamp = '-'.join(map(str,list(time.localtime())[:3]))+' '+':'.join(map(str,list(time.localtime())[3:6]))
        if daycheck(day):
            message = get_text(day)
            if message is not None:
                for line in message:
                    ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).send_keys(line).perform()
                user.send_keys(Keys.RETURN)
                driver.find_element_by_class_name('C28xL').click()
                print (message)
                print ('text MSM sent to %s -- day %s ' %(name,day))
                action = '[%s] Sent %s TextDay%02d.txt, day %s\n\n'%(timestamp, name[:4], day, day)
            else:
                print ('no text on this day', day)


            # send image
            image = get_image(day,condition)
            if image is not None:
                exists = os.path.isfile(image)
                print (image)

                if exists:
                    findattach = driver.find_element_by_xpath('//div[@title="Attach"]')
                    findattach.click()
                    findimage = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                    findimage.send_keys(image)
                    time.sleep(3)
                    send = driver.find_element_by_xpath('//div[@class="_3hV1n yavlE"]')
                    send.click()
                    time.sleep(5)
                    driver.find_element_by_class_name('C28xL').click()
                print ('image MSM sent to %s -- day %s ' %(name,day))
                action = '[%s] Sent %s %s, day %s\n\n'%(timestamp,image[53:], name[:4], day)
            else:
                print ('no image on this day', day)
        else:
            print ('no action for %s'%name)
            action='[%s] Sent %s nth, day %s\n\n'%(timestamp,name,day)
        if action is not None:
            timelogger.write(action)
        else:
            pass
        timelogger.flush()

    except WebDriverException as e:
        print ('error', e)
        print ('Message not sent to', name)
    finally:
        print ('finish day for participant')
        driver.find_element_by_class_name('C28xL').click()


def one_day_run():
    # run until satisfied:
    # 1. no more new participants during the study
    # 2. all participants reach 31 days of study
    # also, when any participant reach 31 days, stop sending to that person.

    def update_list(currentList,previous_list):
        return previous_list + [item for item in currentList if item not in previous_list]

    currentList   = get_online_names('names.txt')
    previous_list = get_names('names_next.txt')
    participants  = update_list(currentList,previous_list)

    fo = open('%s/names_next.txt' %path,'w')
    starttime = time.time()
    for id in participants:
        # id = 'condition1_name001_day1'
        condition = id[:id.index('_name')]
        name = id[id.index('_name')+1:id.index('_day')]
        day  = int(id[id.index('_day')+4:])

        if day <= period_of_study:
            send_stuff(condition,name,day)
            #update the name_list
            new_id = id.replace('day%02d' %day,'day%02d' %(day+1))
            fo.write('%s \n' %new_id)
        else:
            # will not send to those that completed 31 days
            pass

        os.system("sed -i '/%s/d' ./names.txt" %id) # linux
    endtime = time.time()
    totaltime = endtime - starttime
    print ('Time taken to cycle through the script %s s'%totaltime)
    fo.close()
    return previous_list, currentList



def main():
    global path
    global period_of_study
    global driver
    global timelogger
    path = os.getcwd()
    period_of_study = 31 # in days
    #static_time = time.time()
    seconds_in_day = 86400 # number of seconds in 1 day = 24*60*60 = 86400

    continue_run = True
    while continue_run:
        for day in range(period_of_study): ##edit here - set infinitely large number != period of study
            starttime = time.time()
            print ('day', day+1)
            previous_list, currentList = one_day_run()
            print (previous_list, currentList)
            endtime = time.time()
            sleeptime = seconds_in_day -(endtime-starttime)
            # stop_check
            if len(previous_list) == 0 and len(currentList) == 0:
                continue_run = False
                print ('stop the script on this day')
                menu_logout = driver.find_element_by_xpath('//*[@id="side"]/header/div[2]/div/span/div[3]/div')
                menu_logout.click()
                time.sleep(2)
                logout = driver.find_element_by_xpath('//div[@title="Log out"]')
                logout.click()
                driver.close()
                timelogger.close()
                break
            time.sleep(sleeptime)



timelogger = open('./timelogger.txt','a')
timelogger.write('Healthier Food Choices for Psych (APD Lab) Participants Data Log\n')
driver=get_driver() 
now = datetime.now()
run_at = now + relativedelta(days=+1, hour = 7, minute = 0, second = 0) 
delay = (run_at - now).total_seconds()
threading.Timer(delay, main).start()
