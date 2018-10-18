# Project Title

Load Tester is a python script for testing the volume of logs that can be sent to a datadog agent via tcp. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

Ensure [Python 3.7 or later](https://realpython.com/installing-python/) is installed on your machine.

Git the project from github.

	git clone https://github.com/joshbrownDataDog/load_tester.git

Check that the project is install correctly by running in ~/.load_tester 
	
	python3 load_test.py help

If sucsseful you should see

	*** Help for load_test.py ***

	This script requires runs on python 3.7 or later.......

You will now need to insure your datadog agent is properly configured to accept logs via tcp. [This article](https://docs.datadoghq.com/logs/log_collection/?tab=streamlogsfromtcpudp#stream-logs-through-tcp-udp) provides instructions on doing so.

Once the agent is configured, you can run the load tester via:

	python3 load_test.py

This will run the tester with default values of 10 logs per second, 20 random characters per log, for 60 seconds, and send the logs to port 6263.

You can set any of these value via:

	python3 load_test.py key1:<value1> key2:<value2>




## Authors

***Josh Brown**



