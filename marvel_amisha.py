#importing required libraries

from gettext import install
import requests
import pandas as pd
import sys


#activity 2 and 3
def marvel_characters(nameStartWith, API_key=None, hash_key=None, ts=1):
    # raising exceptions when API key and hash key are not passed
    if (API_key==None):
        raise Exception ('API_key not specified')
    elif (hash_key==None):
        raise Exception ('hash_key not specified')
    limit = 300 
     #requested result limit for container

    #dynamic url call with the specified parameters
    dynamic_url = "http://gateway.marvel.com/v1/public/characters?nameStartsWith=" + nameStartWith + "&limit=" + str(limit) + "&ts=" + str(ts) + "&apikey=" + API_key + "&hash=" + hash_key
    response = requests.get(dynamic_url)
    

    #we get json response from the API call

    #storing the resonse in marvel_ous_output
    marvel_ous_output = response.json()
    if (marvel_ous_output['code'] == 200):
        # 'code' == 200 because code response of 200 from http means success
        #generating df from json
        #defining the structure of df
        df_amisha = pd.DataFrame(columns=['id', 'name', 'comics', 'series', 'stories', 'events'])
        if (marvel_ous_output['data']['count'] > 0):
            for character in marvel_ous_output['data']['results']:
                #defining the dictionaries structure to be stored in df
                dict = {'id': int(character['id']), 'name': character['name'], 'comics': int(character['comics']['available']), 'series': int(character['series']['available']), 'stories': int(character['stories']['available']),  'events': int(character['events']['available'])}
                temp_df = pd.DataFrame(dict, index=[0])
                #adding all the dictionaries to df
                df_amisha = pd.concat([df_amisha, temp_df], ignore_index=True)
            return df_amisha
        else: 
            return "No characters found"
    else:
        raise Exception (marvel_ous_output['code'] + ': ' + marvel_ous_output['message'])


#Activity 4
#filtering df on given conditions
def filter_characters(df_amisha, df_col, condition):
    # condition to be passed in terms of x
    return df_amisha.loc[df_amisha[df_col].apply(eval('lambda x: ' + condition))]


#Activity 5 
#if __name__ == “main”: is used to execute some code only if the file was run directly, and not imported.
if __name__ == '__main__':
	#sys.srgv is a lst of command line arguments
    if (len(sys.argv) > 1):
        df_amisha = marvel_characters(sys.argv[1], sys.argv[2], sys.argv[3])
        if (isinstance(df_amisha, pd.DataFrame)):
            if (len(sys.argv) >= 6):
                print(filter_characters(df_amisha, sys.argv[4], sys.argv[5]))
            else:
                print(df_amisha)
        else:
            print(df_amisha)