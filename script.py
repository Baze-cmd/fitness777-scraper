import time
import requests
import json
import os

#URL for the POST request
URL = "https://fitness777.mk/validate.php"
#check for IDs from 0 up to maxID
maxID = 1000
#variables to help finish the program sooner when there has been alot of consecutive invalid IDs
maxNumOfConsecutiveNULLs = 100
numOfConsecutiveNULLs = 0
#number of seconds between each post request,
#the lower it is the faster the program will finish
pauseTimeInterval = 1.0
# Path to your CSV file (it is in the same directory as the script)
csv_file_path = os.getcwd() + "\\data.csv"

# Header for the CSV file
header = "ID,Display Name,Expiration Date,Remaining Days,Credits\n"
try:
    # Check if the file exists
    if not os.path.isfile(csv_file_path):
        # If the file doesn't exist, create it and write the header
        with open(csv_file_path, 'w') as file:
            file.write(header)
        print(f"CSV file '{csv_file_path}' created with headers.")
    else:
        print(f"CSV file '{csv_file_path}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

#variable to keep track of the number of Users saved
totalNumOfUsers = 0
for i in range(maxID):
    #progress
    if (i % 6 == 0):
        formatedN = float("{:.3f}".format(i/maxID))*100
        print(f"Progress: {formatedN}% ({i}/{maxID})")
    # check if we are on a long period of not found users
    if (numOfConsecutiveNULLs > maxNumOfConsecutiveNULLs):
        print(f"Exceded maxNumOfConsecutiveNULLs: {maxNumOfConsecutiveNULLs}")
        print(f"Progress: 100.0%")
        # print statistics
        print(f"Script finished with a total num of users found: {totalNumOfUsers}")
        exit(0)
    # sleep timer
    time.sleep(pauseTimeInterval)

    # construct the data for the id
    idNum = str(i)
    payload = {'username': idNum}

    # get the data for the user with ID i
    r = requests.post(URL, data=payload)
    # decode the data and store it in local variables
    decoded_content = r.content.decode('unicode-escape')
    json_data = json.loads(decoded_content)
    status = json_data['status']
    # check if the entered user is valid
    if (status != "found"):
        numOfConsecutiveNULLs += 1
        continue
    else:
        numOfConsecutiveNULLs = 0
    display_name = json_data['displayName']
    exp_date = json_data['expDate']
    remaining_days = json_data['remainingDays']
    creds = json_data['credits']
    # Format the data as a comma-separated string
    data_to_append = (f"{idNum},{display_name},{exp_date},"
                      f"{remaining_days},{creds}\n")
    # Append data to the CSV file
    try:
        with open(csv_file_path, mode='a', encoding='utf-8') as file:
            # Write the data to the file
            file.write(data_to_append)
            totalNumOfUsers+=1
    except Exception as e:
        print("Did not write to csv file")
        print(f"An error occurred: {e}")
print(f"Progress: 100.0%")
#print statistics
print(f"Script finished with a total num of users found: {totalNumOfUsers}")

