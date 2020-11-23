## ACP controle times

That's "controle" with an 'e', because it's French, although "control" is also accepted. Controls are points where a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must arrive at the location.   

The algorithm for calculating controle times is described here (https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information is given here (https://rusa.org/pages/rulesForRiders). The description is ambiguous, but the examples help. Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly.  

We are essentially replacing the calculator here (https://rusa.org/octime_acp.html). We can also use that calculator to clarify requirements and develop test data.  

## OVERVIEW:

More in depth instructions and information provided above.

The ACP calculator uses the rules outlined above to automatically populate the open and close times for brevets of 200, 300, 400, 600, and 1000 km. 

We populate these times based on the entries provided in the km and miles columns and calculate the times one the server side, then update the webpage with AJAX.

If the provided control distance is too far out of range (less than zero or greater than 1200) or too long for the given brevet, an invalid date and an error message will appear accordingly.

The page will also auto update every open and close time if you change the date, time, or brevet distance, and display any errors that might arise due to the change. 


## INFO

Author: Max Hopkins

email: mhopkin3@uoregon.edu
