import sys, traceback, socket, random, string, signal
from time import sleep, time

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

def main(run_time_parameters):
  
  try:
    print('**** Starting loop ****\n')
    print('Configured values for load test')

    # Print configuration parameters
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

    #Dictionary of performance stats for run.
    run_stats = {'length_of_time':{'text':'Run Time: %s seconds','value':time()},
                'logs_sent':{'text':'Total Logs Generate: %s','value':0},
                'avg_logs_per_second':{'text':'Average Logs per Second: %s','value':0}}
    
    while count < run_time:

      messages_sent_this_second = 0
      elapsed_time = 0
      start_time = time()

      #Set an alarm for 1 second
      signal.alarm(1)
      stop = False

      while messages_sent_this_second < number_of_logs_per_second and stop == False:
        #Try to exececute code within 1 second time limit
        try:
    
          chars = "".join( [random.choice(string.ascii_letters ) for i in range(length_of_log)] )
          log = 'Info:' + chars + '\n'

          tcp_connection.sendall(log.encode())

          messages_sent_this_second += 1

          run_stats['logs_sent']['value'] += 1

          elapsed_time = time() - start_time
        
        #Failed to execute code in one second. 
        except TimeoutException:
          #Set stop to True to insure we go to next loop.
          stop = True
          continue

      # Reset alarm to 0 seconds
      signal.alarm(0)

      print('Loop: %s, Sent %s messages in %s seconds' %(count, messages_sent_this_second, elapsed_time))

      count += 1
      
      
      sleep(1)

    print('')
    print('Done with loop')
  
  # Handle user exiting program   
  except KeyboardInterrupt:
    print("\n**** User Stopped Load Tester ****\n")


  # Handle missing required input - number_of_logs_per_second or length_of_log
  except IndexError:
    print("\n**** Error: required input not provided ****\n")
    
    if len(sys.argv) < 3:
      print('Please run script via: \n python3 load_test.py <number_of_logs_per_second> <length_of_log> \n')

    print_run_stats(run_stats)
  
  # General exception handling
  except Exception:
    print("Error: unhandled exception \n")
    traceback.print_exc(file=sys.stdout)

    print_run_stats(run_stats)
      
  
  print("**** Exiting Load Tester ****")

  print_run_stats(run_stats)

  sys.exit(0)


# Function to print run stats to consule
def print_run_stats(run_stats):

  print('')

  for key in run_stats:
    
    if key == 'length_of_time':
      value = time() - run_stats[key]['value']

    elif key == 'avg_logs_per_second':
      run_time = time() - run_stats['length_of_time']['value']

      total_logs = run_stats['logs_sent']['value']

      value = total_logs/run_time

    else:
      value = run_stats[key]['value']

    text_to_print = run_stats[key]['text'] %value
    
    print(text_to_print)

  print('')


# Function to get input paramters 
def get_run_time_parameters():

  # Default run_time_parameters to use if no user inputs
  run_time_parameters = {'logs_per_second':{'value':10,'discription':'Number of logs to generate per second. If "max" is entered the program will produce as many logs as possible in 1 second.'},
                        'log_length':{'value':20,'discription':'Number of random characters to generate per log'},
                        'run_time':{'value':60,'discription':'Run time of program if not stopped by user'},
                        'port':{'value':10518,'discription':'Port that datadog is listening for logs on https://docs.datadoghq.com/logs/log_collection/?tab=streamlogsfromtcpudp#stream-logs-through-tcp-udp'}}

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
          # If the user specifies max for for logs per second. We set the value to an extreamly large number so that the execution time will take more 
          # than 1 second to complete.
          if key == 'logs_per_second':
            if item.find('max') != -1:
              run_time_parameters[key]['value'] = 10000000000000000000000
            else:
              pass
          else:
            pass

        

  return run_time_parameters

# Help function 
def help(run_time_parameters):

  for item in sys.argv:

    index_of_key  = item.find('help')

    if index_of_key != -1:
      print('\n\n\n*** Help for load_test.py ***\n')

      print('This script requires runs on python 3.7 or later\n')

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

  signal.signal(signal.SIGALRM, timeout_handler)

  print('Running Load Tester\n')

  main(run_time_parameters)
