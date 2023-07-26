from dotenv import load_dotenv #pip install python-dotenv
import ldclient
from ldclient.config import Config
import json
import names
import os
import random
import time
import uuid
from utils.create_context import *


'''
Get environment variables
'''
load_dotenv()

SDK_KEY = os.environ.get('SDK_KEY')
FLAG_NAME = os.environ.get('FLAG_NAME')
METRIC_NAME = os.environ.get('METRIC_NAME')
NUMBER_OF_EVENTS = os.environ.get('NUMBER_OF_EVENTS')
VAR_1_DONATION_AVERAGE = int(os.environ.get('VAR_1_DONATION_AVERAGE'))
VAR_2_DONATION_AVERAGE = int(os.environ.get('VAR_2_DONATION_AVERAGE'))

'''
Initialize the LaunchDarkly SDK
'''
ldclient.set_config(Config(SDK_KEY))


'''
Construct and return a random user
'''
def create_contexts():
    num_contexts = int(NUMBER_OF_EVENTS)
    contexts_array = []
    for i in range(num_contexts):
        context = create_multi_context()
        json.dumps(contexts_array.append(context))
        with open('data/contexts.json', 'w') as f:
            f.write(str(contexts_array))


'''
Determine a donation amount for variation 1
'''
def var_1_amount():
    low = VAR_1_DONATION_AVERAGE - 5
    high = VAR_1_DONATION_AVERAGE + 5
    amount = random.randint(low, high)
    return amount

'''
Determine a donation amount for variation 1
'''
def var_2_amount():
    low = VAR_2_DONATION_AVERAGE - 7
    high = VAR_2_DONATION_AVERAGE + 7
    amount = random.randint(low, high)
    return amount

'''
Evaluate the flags for randomly generated users, and make the track() calls to LaunchDarkly
'''
def callLD():
    create_contexts()
    data = json.load(open("data/contexts.json"))
    variation_1 = {
            "buttonvalue": "signup",
            "imagename": "1.jpg"
        }
    j = 1

    for i in data:

        flag_variation = ldclient.get().variation(FLAG_NAME, i, False)

        if flag_variation == variation_1:
            print("Executing " + str(flag_variation) + ": " + str(j) + "/" + NUMBER_OF_EVENTS)
            ldclient.get().track(f"{METRIC_NAME}", i, metric_value=var_1_amount())

        else:
            print("Executing " + str(flag_variation) + ": " + str(j) + "/" + NUMBER_OF_EVENTS)
            ldclient.get().track(f"{METRIC_NAME}", i, metric_value=var_2_amount())

        j += 1
'''
Execute!
'''
callLD()


'''
Responsibly close the LD Client
'''
ldclient.get().flush()
ldclient.get().close()