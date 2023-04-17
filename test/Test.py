import setup, unittest
from Homepage import Homepage
import json, jsonschema
import pandas as pd
import os
import requests
from genson import SchemaBuilder
import numpy as np

docpath = os.path.abspath(os.curdir) + "\docs"
driver = setup.driversetup()

class Test(unittest.TestCase):
    def __init__(self):
        super().__init__()

    #verify Home page title
    def verifyHomeTitle(self):
        driver.get("https://reqres.in/")
        self.assertEqual(driver.title, "Reqres - A hosted REST-API ready to respond to your AJAX requests", "Title does not match")

    #verify list of EndPoints
    def verifyLoEndpoints(self):
        homepage = Homepage(driver)

        explitext= ["LIST USERS", "SINGLE USER", "SINGLE USER NOT FOUND", "LIST <RESOURCE>", "SINGLE <RESOURCE>", "SINGLE <RESOURCE> NOT FOUND",
                        "CREATE", "UPDATE", "UPDATE","DELETE","REGISTER - SUCCESSFUL", 
                        "REGISTER - UNSUCCESSFUL", "LOGIN - SUCCESSFUL", "LOGIN - UNSUCCESSFUL", "DELAYED RESPONSE"]
        Match = True

        for i,els in enumerate(homepage.endpain):
            if (els.text==explitext[i]):
                continue
            else:
                Match = False
                break

        self.assertEqual(Match,True, msg="List of API is fully or partially not displayed")
        
    #verify Sample Request and Response for list user
    def verifyListUserHomepage(self):

        homepage = Homepage(driver)
        
        homepage.listuser.click()
        self.assertEqual(homepage.reqbox.text, "Request\n/api/users?page=2")
        self.assertEqual(homepage.resbox.text, "Response\n200")
        
        # verify sample response when home page load
        
        sample_response = homepage.sampleresponse.text
        jresponse = json.loads(sample_response)
        
        jfile = open(docpath + "\listuser_sample.json")
        jsample = json.load(jfile)
        
        self.assertEqual(jresponse,jsample)
    
    #verify sample request and response for get user
    def verifyGetUserHomepage(self):
        homepage = Homepage(driver)
        
        homepage.getuser.click()
        self.assertEqual(homepage.reqbox.text, "Request\n/api/users/2")
        self.assertEqual(homepage.resbox.text, "Response\n200")
    
    # verifySchema and response code for getUSER API request
    def verifyGetUserAPI(self):
        homepage =Homepage(driver)

        headers = {"Content-Type": 'application/json'}
        response = requests.request("GET", "https://reqres.in/api/users/3",headers=headers)
        jresponse = response.json()
        
        #generate schema from sample
        
        docpath = os.path.abspath(os.curdir) + "\docs"
        jfile = open(docpath + "\getuser_sample.json")
        jsample = json.load(jfile)
        builder = SchemaBuilder()
        builder.add_object(jsample)
        
        jsonschema.validate(jresponse, builder.to_schema())

    # verify report
    def verifyExcelrepo(self):
        ifile = pd.read_csv(docpath + "\InstrumentDetails.csv")
        pfile = pd.read_csv(docpath + "\PositionDetails.csv")
        ifile.rename(columns={"ID":"InstrumentID"},inplace=True)
        pfile.rename(columns={"ID":"PositionID"},inplace=True)
        prepo = pd.read_csv(docpath + "\PositionReport.csv")

        # Position ID belongs to ID in position deails
        temp = prepo[prepo["PositionID"].isin(pfile["PositionID"])]
        if (prepo.size > temp.size):
            print("Unknown position id exists in the report")
        
        # ISIN belongs to ISIN in instrument details
        temp = prepo[prepo["ISIN"].isin(ifile["ISIN"])]
        if (prepo.size > temp.size):
            print("Unknown ISIN exists in the report")
        
        # ISIN in report file match with ISIN from instrument file for the Position ID
    
        iIDpInstID = pfile.merge(ifile, how='left')
        iIDpInstID["Total_Price"] = iIDpInstID["Quantity"]*iIDpInstID["Unit Price"]
        test_repo = prepo.merge(iIDpInstID,on=["PositionID"],how='left')

        if(test_repo["ISIN_x"].equals(test_repo["ISIN_y"])):
            print("ISIN correct")
        else:
            print("ISIN not matched")
        
        # Total price = qty from position file * price from instrument file
        # print(test_repo.columns.to_list)

        if((test_repo["Total Price"]).equals(test_repo["Quantity"]*test_repo["Unit Price"])):
            print("Total price/Open position correct")
        else:
            print("Total Price calculation does not match")