bathroom_sensor.squirrel is the Electric Imp device code, to be deployed to the Imp.

bathroomserver.py is a minimal Python 2.7 server and app hybrid that acts as the receiver for the Imp's updates, and as the app server for the users. 

Deploy the system by running bathroomserver.py in an internet accessible location, and then pointing Electric Imp HTTP requests to the /opened and /closed paths on that server. The script is hardwired to run on port 15567. Change that if you want, possibly to the default port 80 for HTTP.