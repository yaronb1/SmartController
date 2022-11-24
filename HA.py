# -*- coding: utf-8 -*-
"""
Created on Tue May  4 20:07:35 2021

@author: yaron
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class HAController():
    #privide username and password to the initailiser(default is my acoount)
    def __init__(self, username="yaron",
                       password= "Cheryl123?" ):
        self.username= username
        self.password= password
        self.driver = webdriver.Chrome()
        
    #opens HA script screen
    #signs in with the username and password from the initialiser
    def openHA(self):
        try:self.driver.get("http://homeassistant.local:8123/developer-tools/service")
        except: print("cannot reach Home assistant")
        try:
            u = WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > ha-authorize"))
                )
        except: print ("HA not found")
        else:
 #           print ("waiting...")
             time.sleep(1)

             u.send_keys(self.username)
# print("usernamed typed")
             time.sleep(1)
             u.send_keys(Keys.TAB)
# print("move to password")
             time.sleep(1)
             u.send_keys(self.password)
# print("password typed")
             time.sleep(1)
             u.send_keys(Keys.TAB)
# print("move to enter")
             time.sleep(1)
             u.send_keys(Keys.ENTER)
             
             time.sleep(5)
             try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > div > mwc-button")'
                                        ).click()

             except: print ("cannot reach yaml mode")
             self.driver.maximize_window()

             
             
#print("enter pressed")




        
        
        
    # #clicks the relevant script for the lamp and counch
    # def all_off(self):
    #     try: self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-config > ha-config-script > ha-script-picker").shadowRoot.querySelector("#entity_id").shadowRoot.querySelector("hass-tabs-subpage > ha-data-table").shadowRoot.querySelector("div > div > div.mdc-data-table__content.scroller.ha-scrollbar > div:nth-child(4) > div:nth-child(1) > mwc-icon-button").shadowRoot.querySelector("button"))'
    #                                     ).click()
    #     # try: 
    #     #     button.click()
    #     except: print ("cannot click button")
    
    
    def all_off(self):
        s = 'service: script.all_off'
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except: print("cannot grab service box")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
        


    def couch(self):
        s = 'service: script.toggle_couch'
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except: print("call service button not clicked")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
        
        
    def AC_off(self):
        s = 'service: script.ac_off'
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except: print("call service button not clicked")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
        
    def AC_on(self):
        s = 'service: script.ac_on_20_c'
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")')
        except:print("cannot get service box")                            
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
      
    def lamp_open(self):
        s = 'service: script.toggle_openlamp'
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except:print("cannot grab service box")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
            
        

        
    def colorBulb(self,colourMode="RGB", R=0, G=0, B=0,  r= 0, alpha=0, brightness= 100):
        
        
        if colourMode=="HS":
            #s = 'service: light.turn_on\ndata:\n\trgb_color:\n\t\t- 255\n\t\t- 0 \n\t\t- 0\n\tdevice_id: b318f723dd9accaab5caab0c46cbc4b5  '
            s = 'service: light.turn_on\ndata:\n\ths_color:\n\t\t- ' + str(alpha) + '\n\t\t- ' + str(r) + '\n\tdevice_id: b318f723dd9accaab5caab0c46cbc4b5  '
  
        elif colourMode == "RGB":
            s = 'service: light.turn_on\ndata:\n\trgb_color:\n\t\t- ' + str(R) + '\n\t\t- ' + str(G) + '\n\t\t- ' +str(B) + '\n\tdevice_id: b318f723dd9accaab5caab0c46cbc4b5  '
        
        
        elif colourMode == "brightness":
            s = 'service: Light.turn_on\ndata:\n\tbrightness_pct: ' + str(brightness) + '\n\tdevice_id: b318f723dd9accaab5caab0c46cbc4b5'
        
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except:print("cannot grab service box")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
            
    def ledRecognise(self, mode):
        s=''
        if mode == 'on':
            s = 'service: script.red'
            
        if mode == 'off':
            s = 'service: script.led_off'
            
        if mode == 'kill':
            s = 'service: script.white'
        
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except:print("cannot grab service box")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
            
    def ledHome(self, mode):
        s=''
        if mode == 'on':
            s = 'service: script.house_on'
            
        if mode == 'off':
            s = 'service: script.hpuse_off'
            
        
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except:print("cannot grab service box")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
        
    def ledYoutube(self, mode):
        s=''
        if mode == 'on':
            s = 'service: script.youtube_on'
            
        if mode == 'off':
            s = 'service: script.youtube_off'
            
        
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except:print("cannot grab service box")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
            
            
    def ledNetflix(self, mode):
        s=''
        if mode == 'on':
            s = 'service: script.1632297671149'
            
        if mode == 'off':
            s = 'service: script.netflix_off'
            
        
        try:service = self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.content > ha-yaml-editor").shadowRoot.querySelector("ha-code-editor").shadowRoot.querySelector("div > div.cm-scroller > div.cm-content")'
                                        )
        except:print("cannot grab service box")
        else:
            service.clear()
            service.send_keys(s)
            try:self.driver.execute_script('return document.querySelector("body > home-assistant").shadowRoot.querySelector("home-assistant-main").shadowRoot.querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-developer-tools").shadowRoot.querySelector("ha-app-layout > developer-tools-router > developer-tools-service").shadowRoot.querySelector("div.button-row > div > mwc-button")'
                                                 ).click()
            except: print("call service button not clicked")
            
    def ping(self):
        return self.driver.current_url
            
        
        
        
def main():
        HA = HAController()
        HA.openHA()
        time.sleep(5)
        # HA.lamp_open()
        # HA.couch()
        # time.sleep(3)
        
        # HA.all_off()
        
        # time.sleep(2)
        
        HA.ledRecognise('on')
        

        

if __name__ == "__main__":
    main()