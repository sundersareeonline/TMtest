from selenium.webdriver.common.by import By
from selenium import webdriver
import setup

#driver = setup.driversetup()

class Homepage(object):

    def __init__(self,driver):
        super().__init__()
        self.driver = driver
        self.endpain = driver.find_elements(By.XPATH,"//div[@class='endpoints']/ul/li")
        self.reqbox = driver.find_element(By.XPATH, "//p[@class='request-title']")
        self.resbox = driver.find_element(By.XPATH, "//p[@class='response-title']")
        self.sampleresponse = driver.find_element(By.XPATH, "//pre[@data-key='output-response']")
        self.listuser = self.endpain[0]
        self.getuser = self.endpain[1]

    #def endpoints(self):
    #    ele_endpoints = driver.find_elements(By.XPATH,"//div[@class='endpoints']/ul/li")
    #    return ele_endpoints

    """ def endpoints(self):
        return self.endpain
    
    def reqbox(self,driver):
       reqbox = driver.find_element(By.XPATH, "//p[@class='request-title']")
       return reqbox
    
    def resbox(self,driver):
        resbox = driver.find_element(By.XPATH, "//p[@class='response-title']")
        return resbox
    
    def sampleresponse(self,driver):
        samres = driver.find_element(By.XPATH, "//pre[@data-key='output-response']")
        return samres

    def listuser(self,driver):
        ele_endpoints = Homepage.endpoints(self)
        return ele_endpoints
    
    def listuser(self,driver):
        ele_endpoints = Homepage.endpoints(self)
        return ele_endpoints """