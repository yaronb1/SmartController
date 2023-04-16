import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import subprocess
import pyautogui
import cv2
import os
import sys



'''
used to control spotify online. not in use currently
'''
class SpotifyController():
    #initialiser gets username and password(default is my new google accoun)
    #sets the driver
    def __init__(self, username="yaronbarlevytest@gmail.com",
                       password= "y>2=8!Z(ut>F" ):

        options = webdriver.ChromeOptions()
        options.add_argument(r"--user-data-dir=/home/yaron/.config/google-chrome/")  # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
        options.add_argument(r'--profile-directory=Profile 1')  # e.g. Profile 3
        self.driver = webdriver.Chrome(options=options)

    def open_spotify(self, maxWindow=True, login=False):

        try:
            self.driver.get("https://open.spotify.com/collection/playlists")

        except:
            print("cannot find page")

        if login:
            # login button
            try:
                login = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a/tp-yt-paper-button"))
                )
            except:
                print("cannot find login button")
                self.driver.get("https://www.youtube.com/")

            else:
                login.click()
                print("login clicked")

                # email
                try:
                    user = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")))

                except:
                    print("cannot fint username input")
                    self.driver.get("https://www.youtube.com/")
                else:
                    user.send_keys(self.username)
                    user.send_keys(Keys.RETURN)
                    # password
                    try:
                        passW = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")))
                    except:
                        print('cannot find password input')
                        self.driver.get("https://www.youtube.com/")
                    else:
                        time.sleep(1)
                        passW.send_keys(self.password)
                        passW.send_keys(Keys.RETURN)

        # if maxWindow:
        #     self.driver.maximize_window()
        # else:
        #     try:
        #         self.driver.set_window_size(640, 720)
        #     except:
        #         print("cannot set size")

class Spotify():

    def open_spotify(self):
        data = 'spotify --uri=spotify:playlist:7rzCMMNPBKD5heuFg8zaeU'
        cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        #
        #


        #works on youtube from pycharm or from cmd line for spot and you
        #but not frompycharm for spot
        #cmd = subprocess.call(("playerctl", "play-pause"))
        #cmd = subprocess.call(("playerctl", "--player=spotify", "play-pause"))

        #os.system('playerctl play-pause')

        #doesnt work from cmd or pycharm or on youtube
        #pyautogui.press('playpause')

    def remote(self):
        #cmd = subprocess.call(("playerctl", "--player=spotify", "play-pause"))
        pyautogui.press('space')



if __name__ =="__main__":

    s= Spotify()
    s.remote()




