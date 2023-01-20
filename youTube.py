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

class youTubeController():
    #initialiser gets username and password(default is my new google accoun)
    #sets the driver
    def __init__(self, username="yaronbarlevytest@gmail.com",
                       password= "y>2=8!Z(ut>F" ):
        self.username= username
        self.password= password
        self.driver = webdriver.Chrome()

        options = webdriver.ChromeOptions()
        options.add_argument("~/.config/google-chrome/Profile1")
        self.driver = webdriver.Chrome(options=options)
        self.UI =[]
        
    #opens youstube and signs in with the username and password 
    #provided with the initialiser
    def openYoutube(self, maxWindow = True,login=False):

        try:self.driver.get("https://www.youtube.com/")
        except: print ("cannot find page")


        if login:
            #login button
            try:
                login = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a/tp-yt-paper-button"))
                    )
            except:
                print ("cannot find login button")
                self.driver.get("https://www.youtube.com/")

            else:
                login.click()
                print("login clicked")

                #email
                try:    user = WebDriverWait(self.driver, 2).until(
                             EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")))

                except:
                    print("cannot fint username input")
                    self.driver.get("https://www.youtube.com/")
                else:
                    user.send_keys(self.username)
                    user.send_keys(Keys.RETURN)
                    #password
                    try:        passW = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")))
                    except:
                        print('cannot find password input')
                        self.driver.get("https://www.youtube.com/")
                    else:
                        time.sleep(1)
                        passW.send_keys(self.password)
                        passW.send_keys(Keys.RETURN)
                    
        if maxWindow:self.driver.maximize_window()
        else:
            try:
                self.driver.set_window_size(640, 720)
            except:
                print("cannot set size")

    # #click voice search button
    # # we need to check how to give it permisiions
    # def voiceSearch(self):
    #
    #     try:
    #         WebDriverWait(self.driver, 0).until(
    #             EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/div/ytd-button-renderer/a/yt-icon-button/button/yt-icon"))
    #             ).click()
    #
    #     except Exception as e:
    #         print(e)

    #scrolls down
    def scroll(self):
        try:
            WebDriverWait(self.driver, 0).until(
                EC.presence_of_element_located((By.TAG_NAME, "html"))
                ).send_keys(Keys.PAGE_DOWN)
        except: print("cannot scroll")
      
    #clicks next video button on an open video
    def nextSong(self):
        try:
            WebDriverWait(self.driver, 1).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-next-button.ytp-button"))
             ).click()
            
        except: print("next song error")



    #gets a list of all the videos on the page
    #selects the first one
    def select(self,*args):
        # try:videos = self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a')
        # except Exception as e:print(e)
        # else:
            #try: ActionChains(self.driver).move_to_element(videos).click(videos).perform()

            #except:
                try:
                    videos = self.driver.find_elements(By.ID, 'img')
                    videos[0].click()
                except Exception as e: print(e)
        
    def play(self):
        try:
            WebDriverWait(self.driver, 1).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button"))
             ).click()
            
        except: print("cannot click")
        
    def getScreen(self, width,height):
        self.driver.save_screenshot('a.png')
        screen = cv2.imread('a.png')
        screen = cv2.resize(screen,(width,height))

        try:self.UI = cv2.resize(self.UI, (width, height))
        except: print('no youtube media buttons')
        else:screen= cv2.bitwise_or(screen,self.UI)
        return screen
    
    def posClick(self, x,y):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(self.driver.find_element_by_tag_name('html'), x,y).click().perform()
        #actions.move_to_element_with_offset(self.driver.find_elements(by=By.TAG_NAME,value='html'),x,y).click().perform()
            
            
    def waitForPageToLoad(self,width=0,height=0, TO=1):
        #WebDriverWait(self.driver,TO).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#movie_player > div.html5-video-container > video")))
        
        try:WebDriverWait(self.driver,TO).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#movie_player > div.html5-video-container > video")))
        except: return    
        else:
            try:WebDriverWait(self.driver,TO).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                
            #self.driver.implicitly_wait(25)
            except: return
            else:
                time.sleep(1)
                
                print("loaded")
                return self.getScreen(width, height)
            
    def ping(self):
        return self.driver.current_url


    #send the txt keys to the search bar and searches
    def search(self, txt):
        try:
            element = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input"))
            )
            element.send_keys(str(txt))
            element.submit()
        except:
            print("next song error")

    #full screen by pressing f on the html page
    def full_screen(self):

        try:
            element = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html"))
            )
            element.send_keys('f')

        except Exception as e:
            print(e)

        
if __name__=="__main__":

    import Speech
    yt = youTubeController()

    #
    # cv2.waitKey(0)
    #
    yt.openYoutube()



    txt = Speech.listen()

    yt.search(txt)

    yt.waitForPageToLoad()
    yt.select()

    yt.waitForPageToLoad()
    yt.full_screen()

