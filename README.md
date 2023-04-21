# Waive Targeted Alma Fines
Script to waive fines in Alma by Fine ID/User ID to waive only the fines you want

This is a down and dirty script but waives with targeted precision.

Script is set by default to do the Waive operation with a reason of "Other" and prompts the person running the script for a comment to add to the waived fine. (Comment will be the same for all fines in the batch.) 

# You will need:
- Report from Alma Analytics of active fines and fees that include Fine/Fee ID, User ID, and Remaining Fine amount, exported to Excel (and with the first two rows removed)
- (I enclose my IDs and amounts in ""s to make sure the IDs don't get cut off as long numbers. The script removes the ""s and strips white space from the amount.)
- API Key from the ExLibris Developers Network for Fulfillment and Users (Read/Write)
- If you're not in North America, you will need the API server address for your region
