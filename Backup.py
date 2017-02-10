# Backup to the Cloud
# Program 2
# Author: Tyler Hilde
# Date: 2/9/17
# A simple program that uses boto3 to make API calls to AWS S3 cloud storage to backup a local directory.
# User chooses a bucket and a local directory to backup to the bucket

import boto3
import os
import sys

s3 = boto3.resource("s3")
client = boto3.client('s3')
buckets = s3.buckets.all()

print("Welcome to Backup Progam 2")
print("Available buckets:")

for bucket in buckets:
	print(bucket.name)

#Check if bucketName exists
bucketExists = False
while not bucketExists: 
    bucketName = input("Enter the name of the bucket to backup to:")    

    for bucket in buckets:       
        if bucketName == bucket.name:
            bucketExists = True
            break  
    if not bucketExists:
        print("Bucket: " + bucketName + " does not exist. Try again.")
       
#Check if path exists
pathExists = False
while not pathExists:
    fullPath = input("Enter full path of directory to backup (ex: C:\Documents\School): ")    
    pathExists = os.path.exists(fullPath);
    if not pathExists:
        print("Error - Bad path: " , fullPath)
    

print("----------------------- WARNING!!! -----------------------")
print("This will overwrite any existing backup of this directory.")
continueFlag = input("To continue enter y, or any key to quit: ")
if continueFlag != 'y':
    sys.exit()

print("Starting backup...")
bucket = s3.Bucket(bucketName)

#Strip any backslash off the end of path if user enters incorrectly IE C:\Directory\ -> C:\Directory
fullPath = fullPath.rstrip('\\') 

#Get the last directory to be working directory
topDirList = fullPath.rsplit('\\', 1)
topDir = topDirList[-1]

#Walk over directory, updating as walk over subdirectories
for root, dirs, files in os.walk(fullPath): 
    curTopDir = root.split(topDir,1)[1]     
    curPath = topDir + root.split(topDir,1)[1] #split at the keyword topDir to get path
    fixedCurPath = curPath.replace("\\", "/") #replace the backslash with slash   
    
    #Create all directories and subdirectorties, empty or not
    for index in range(len(dirs)):
        if len(dirs) > 0:                     
            curDirPath = topDir + curTopDir + '/' + dirs[index]
            fixedCurDirPath = curDirPath.replace("\\", "/") #replace the backslash with slash           
            
            bucket.put_object(                
                Bucket=bucketName,
                Body='',
                Key=(fixedCurDirPath + '/')
                )  
              
    #Upload files into current directory            
    for index in range(len(files)):
        if len(files) > 0:             
            filePath = fullPath + curTopDir + "\\" + files[index]            
            client.upload_file(filePath, bucketName, (fixedCurPath +'/' + files[index]))
           
           
print("Backup finished.")            
print('')

viewDir = input("View updated " + bucketName + " bucket? Enter y or any key to quit:")
if viewDir != 'y':
    sys.exit()

print("-----------------------")
print(bucketName, " directory: ")  
#Print out the current bucket
for key in bucket.objects.all():
	print(key.key)
print("-----------------------")

anyKey = input("Press any key to exit.")
sys.exit()

