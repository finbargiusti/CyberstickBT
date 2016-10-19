import os
import time
import shutil
import re

while True:
	fileName = os.listdir("static/uploads/")
	fileLol = [i.split() for i in fileName]
	timez = len(fileLol)
	numbor = 0
	for x in range(timez):
		testAge = time.time()
		tehFile = fileLol[numbor]
		tehFile = str(tehFile).translate(None, "[']")
		tehFileList = tehFile.split("-")
        if len(tehFileList) == 2:
            if testAge-float(tehFileList[1]) >= 900:
                shutil.rmtree("static/uploads/"+tehFile)
                print ("Deleted session "+tehFile+"!")
        if len(tehFileList) == 3:
            if testAge-float(tehFileList[1]) >= 86400:
                shutil.rmtree("static/uploads/"+tehFile)
                print ("Deleted session "+tehFile+"!")
		numbor += 1
			
