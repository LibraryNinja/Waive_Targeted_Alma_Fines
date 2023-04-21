import requests
import pandas as pd
from datetime import datetime

#Set up dictionary for reporting purposes
dict = {}
dict['userid'] = []
dict['fineid'] = []
dict['amountwaived'] = []
dict['requesturl'] = []
dict['responsecode'] = []

#Gets current date for output filename
today = datetime.today()

#Set up default things for base URL and bib API key
alma_base = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1'
headers = {"Accept": "application/xml"}


#Users and Fines R/W API key
fineapi = '[ENTER USERS AND FINES API KEY (RW) HERE]'


#Parameters specific to fine-waiving projects:
user_id_type = "all_unique"
op = "waive"
reason = "OTHER"


#Pull in Excel file with fines to waive
inputname = input('Data Input Filename without extension: ')
source = pd.read_excel(inputname + '.xlsx')

#Asks for a note to include as the "comment" for the transaction in Alma and converts spaces to "%20"
rawcommentinput = input("Transaction waiving note: ")
commentinput = rawcommentinput.replace(' ', "%20")

#Displays the comment with HTML encoding
print(f'Comment will be added as: {commentinput}')

#Take the user primary ID, remaining amount, and fine fee ID columns from the input data and make that a list in Python as Strings (so they don't get cut off for being long numbers)
userpids_raw = source['User Primary Identifier'].astype(str)
amounts_raw = source['Remaining Amount'].astype(str)
finefeeids_raw = source['Fine Fee Id'].astype(str)

#Remove extra precautionary ""s and strips whitespace
userpids = ([s.replace('"', '') for s in userpids_raw])
finefeeids = ([t.replace('"', '') for t in finefeeids_raw])
amounts_ws = ([y.replace('"', '') for y in amounts_raw])
amounts = ([w.strip() for w in amounts_ws])

#Optional: Check that everything imported correctly
print(userpids)
print(amounts)
print(finefeeids)


#Run the requests, looping through input and putting results into dictionary for reporting purposes
for i, finefeeid in enumerate(finefeeids, 0):
    userpid = userpids[i]
    dict['userid'].append(userpid)
    
    amount = amounts[i]
    dict['amountwaived'].append(amount)
    
    finefeeid = finefeeids[i]
    dict['fineid'].append(finefeeid)
    
    #Courtesy print to let you know where you are in the process
    print(f"Processing {finefeeid}, entry # {str(i+1)} of {str(len(finefeeids))}")

    #The actual API request
    r = requests.post(f'{alma_base}/users/{userpid}/fees/{finefeeid}?user_id_type={user_id_type}&op={op}&amount={amount}&reason={reason}&comment={commentinput}&apikey={fineapi}', headers=headers)
    
    #These are for reporting the URL used and the end result
    requesturl = r.url
    dict['requesturl'].append(requesturl)
    
    statuscode = r.reason
    dict['responsecode'].append(statuscode)
    print(f'Status: {statuscode}')
        
   

#Converts Dictionary to Dataframe
df = pd.DataFrame(dict)

df.head()

#Save Dataframe to Excel
df.to_excel(f"fine_waive_results_{today:%m%d%Y}.xlsx", index=None)