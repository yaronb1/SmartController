# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:12:13 2021

@author: yaron
"""
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import cv2
#from autopy import mouse 

#import pyautogui

class netflixController():
    #initialiser gets username and password(default is my ornas account)
    #sets the driver
    def __init__(self, username="orna.farzalla06@gmail.com",
                       password= "polanski" ):
        self.username= username
        self.password= password
        self.driver = webdriver.Chrome()
        
    #opens netflix and signs in with the username and password 
    #provided with the initialiser
    def openNetflix(self, maxWindow = True):

        try:self.driver.get("https://www.netflix.com/il-en/login")
        except: print ("cannot find page")

        #login button
        # try:
        #      login = WebDriverWait(self.driver, 1).until(
        #          EC.element_to_be_clickable((By.CSS_SELECTOR, "#id_userLoginId"))
        #          )
        # except: print ("cannot find login button")
        # else:
        # #     login.click()
        # #     print("login clicked")
            
             #email
        try:    user = WebDriverWait(self.driver, 2).until(
                          EC.presence_of_element_located((By.CSS_SELECTOR, "#id_userLoginId")))

        except: print("cannot fint username input")
        else:
                 user.send_keys(self.username)
                 user.send_keys(Keys.TAB)
                #password
                 try:        passW = WebDriverWait(self.driver, 2).until(
                     EC.presence_of_element_located((By.CSS_SELECTOR, "#id_password")))
                 except: print('cannot find password input')
                 else:

                     passW.send_keys(self.password)
                     passW.send_keys(Keys.RETURN)
                     # time.sleep(1)
                     
                     # try:        profile = WebDriverWait(self.driver, 2).until(
                     # #EC.presence_of_element_located((By.TAG_NAME, "html")))
                     # EC.presence_of_element_located((By.TAG_NAME,"html")))
                     # except: print("cannot click on user")
                     # else: 
                     #     print("selected")
                         
                     #     for i in range(6):
                     #         profile.send_keys(Keys.TAB)
                        
                     #     time.sleep(1)
                     #     try:        bod = WebDriverWait(self.driver, 2).until(
                     # #EC.presence_of_element_located((By.TAG_NAME, "html")))
                     #     EC.presence_of_element_located((By.CSS_SELECTOR,"body")))
                     #     except: print("no body")
                     #     else: 
                     #         print("enter")
                     #         bod.send_keys(Keys.ENTER)
        if maxWindow:self.driver.maximize_window()
        time.sleep(2)
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(self.driver.find_element_by_tag_name('html'), 330,350).click().perform()




    #scrolls down
    def scroll(self):
        try:
            WebDriverWait(self.driver, 0).until(
                EC.presence_of_element_located((By.TAG_NAME, "html"))
                ).send_keys(Keys.PAGE_DOWN)
            
        except: print("cannot scroll")
        else: print("scrolled")

        
        
    def getScreen(self, width,height):
        self.driver.save_screenshot('a.png')
        screen = cv2.imread('a.png')
        screen = cv2.resize(screen,(width,height))
        return screen
    
    def posClick(self, x,y):
        # # actions = ActionChains(self.driver)
        # # actions.move_to_element_with_offset(self.driver.find_element_by_tag_name('html'), x,y).click().perform()
        # #except Exception as e: print(e) 
        # try: bod= WebDriverWait(self.driver,2).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        # except:print("elemnet not found")
        # else:
        #     print(bod.location)
        #     print(bod.size)
        #     print('elemnet found')
        #     print(x)
        #     print(y)
        #     #bod.click()
        #     actions = ActionChains(self.driver)
        #     #actions.move_to_element_with_offset(bod,100,100).perform()
        #     actions.move_to_element(bod).perform()
        #     actions.move_by_offset(x,y).click().perform()
        #     print("clicked")
        # self.driver.switch_to.window(self.driver.current_window_handle)
        self.driver.switch_to.window(self.driver.current_window_handle)
        self.driver.maximize_window()
        # mouse.move(x,y)
        # mouse.click()
        # pyautogui.click(x,y)
        print("click")
        
            
    def waitForPageToLoad(self,width,height, TO=10):
        #WebDriverWait(self.driver,TO).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#movie_player > div.html5-video-container > video")))
        
        # try:WebDriverWait(self.driver,TO).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#movie_player > div.html5-video-container > video")))
        # except: return    
        # else:
            try:WebDriverWait(self.driver,TO).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                
            #self.driver.implicitly_wait(25)
            except: return
            else:
                time.sleep(1)
                
                print("loaded")
                return self.getScreen(width, height)
            
    def play(self):
        print('play')
    
    def ping(self):
        return self.driver.current_url
        

def main():
    nf = netflixController()
    nf.openNetflix()
    time.sleep(15)

    nf.posClick(500,500)
    print ("done")
    # try:user = WebDriverWait(nf.driver, 2).until(
    #                       EC.presence_of_element_located((By.TAG_NAME, "html")))
    # except: print ('no page found')
    # else: print ("page found")
    
    # # actions = ActionChains(nf.driver)
    # # actions.move_to_element_with_offset(nf.driver.find_element_by_xpath("/html/body"), 1,1).click().perform()
    
    # try: bod= WebDriverWait(nf.driver,2).until(EC.presence_of_element_located((By.XPATH, "/html")))
    # except:print("elemnet not found")
    # else:
    #     print('elemnet found')
    #     #bod.click()
    #     actions = ActionChains(nf.driver)
    #     actions.move_to_element_with_offset(bod,100,100).click().perform()
    #     #actions.move_to_element(bod)
    #     #actions.move_by_offset(19,10).click().perform()
        
if __name__ == "__main__":
    main()        