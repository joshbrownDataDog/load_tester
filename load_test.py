import sys, traceback, socket
from time import sleep
import random
import string

def main(run_time_parameters):
  
  try:
    print('**** Starting loop ****\n')
    print('Configured values for load test')
    for item in run_time_parameters:
      print('\n' + item)
      print(run_time_parameters[item])
    print('')

    number_of_logs_per_second = run_time_parameters['logs_per_second']['value']
    length_of_log = run_time_parameters['log_length']['value']
    run_time = run_time_parameters['run_time']['value']

    host = socket.gethostbyname(socket.gethostname())
    

    port = run_time_parameters['port']['value']

    tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_connection.connect((host, port))

    count = 0

    while count < run_time:
      print('Loop: %s' %count)

      messages_sent_this_second = 0

      while messages_sent_this_second <= number_of_logs_per_second:
        chars = "".join( [random.choice(string.ascii_letters ) for i in range(length_of_log)] )
        log = 'info:' + chars + '\n'

        tcp_connection.sendall(log.encode())

        messages_sent_this_second += 1

      count += 1
      
      
      sleep(1)

    print('')
    print('Done with loop')
  
  # Handle user exiting program   
  except KeyboardInterrupt:
    print("User Stopped Load Tester \n")

  # Handle missing required input - number_of_logs_per_second or length_of_log
  except IndexError:
    print("\n**** Error: required input not provided ****\n")
    
    if len(sys.argv) < 3:
      print('Please run script via: \n python3 load_test.py <number_of_logs_per_second> <length_of_log> \n')
  
  # General exception handling
  except Exception:
    print("Error: unhandled exception \n")
    traceback.print_exc(file=sys.stdout)
      
  
  print("**** Exiting Load Tester ****")

  sys.exit(0)

# Function to get input paramters 
def get_run_time_parameters():

  # Default run_time_parameters to use if no user inputs
  run_time_parameters = {'logs_per_second':{'value':10,'discription':'Number of logs to generate per second'},
                        'log_length':{'value':20,'discription':'Number of random characters to generate per log'},
                        'run_time':{'value':60,'discription':'Run time of program if not stopped by user'},
                        'port':{'value':6263,'discription':'Port that datadog is listening for logs on https://docs.datadoghq.com/logs/log_collection/?tab=streamlogsfromtcpudp#stream-logs-through-tcp-udp'}}

  # Check to see if user asked for help                    
  help(run_time_parameters)

  for key in run_time_parameters:

    # Look at all items in sys.argv, all of the variables passed into script when run using: python3 load_test.py <number_of_logs_per_second> <length_of_log>
    for item in sys.argv:

      index_of_key = item.find(key)

      # If key is in item, attempt to get inputed value and update the run_time_parameters
      if index_of_key != -1:
        try:
          index_of_colon = item.find(':') + 1
          run_time_parameters[key]['value'] = int(item[index_of_colon:])
        except:
          pass
        

  return run_time_parameters

# Help function 
def help(run_time_parameters):

  for item in sys.argv:

    index_of_key  = item.find('help')

    if index_of_key != -1:
      print('\n\n\n*** Help for load_test.py ***\n')

      print('This script requires runs on python 3.6 or later\n')

      run_script_text = "Run script via: python3 load_test.py "

      for key in run_time_parameters:
        run_script_text = run_script_text + key + ':<' + key + '> '

      print(run_script_text + '\n')

      for key in run_time_parameters:
        print('\n' + key + ': ' + run_time_parameters[key]['discription'])
        print('Default Value: ' + str(run_time_parameters[key]['value']))
      
      print('\n\n\n')

      sys.exit(0)


# Initializaiton function
if __name__ == "__main__":
  run_time_parameters = get_run_time_parameters()

  print('Running Load Tester\n')

  main(run_time_parameters)
