import os
import time
import shutil
import re

while True:
	fileName = os.listdir("static/uploads/")
	fileLol = [i.split() for i in fileName]
	numbor = 0
        if len(fileLol) > 0:
            for x in range(len(fileLol)):
                    testAge = time.time()
                    tehFile = fileLol[numbor]
                    tehFile = str(tehFile).translate(None, "[']")
            if len(tehFile.split("-")) == 2:
                if testAge-float(tehFileList[1]) >= 900:
                    shutil.rmtree("static/uploads/"+tehFile)
                    print ("Deleted session "+tehFile+"!")
            if len(tehFile.split("-")) == 3:
                if testAge-float(tehFileList[1]) >= 86400:
                    shutil.rmtree("static/uploads/"+tehFile)
                    print ("Deleted session "+tehFile+"!")
                    numbor += 1
