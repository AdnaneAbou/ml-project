from googleapiclient.discovery import build
import requests
# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python


#  github

import time
from googleapiclient.discovery import build
import pandas as pd 
from IPython.display import JSON
from src.database.database import Database
import sys 
from src.exception import CustomException
from src.logger import logging
from src.utils import json_to_dataframe , chunk_list

class YoutubeAPI:

    def __init__(self, api_key):

        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)


    



    def get_all_videos(self,query, database_name , collection_name ):


        
        try:    
            db = Database(database_name=database_name)
            logging.info(f" Successfully connected to mongodb database {database_name}")

            regionCode = ['US','CN','IN','BR','GB','RU','FR','DE','JP','CA','AU','KR','IT','ES','MX','ID','NL','SA','CH','TR']
            i = 1 
            next_page_token = None

            for s in range(len(regionCode)-1):

                while True:

                    
                    

                    request = self.youtube.search().list(
                                part='snippet',
                                q=",".join(query),
                                maxResults=50,  # Adjust as needed
                                order='date',
                                pageToken=next_page_token,
                                regionCode=regionCode[s]
                            )
                    response = request.execute()

                    print(f"I am in the {i} th iteration in {regionCode[s]}")
                    i += 1
                    time.sleep(1)

                    next_page_token = response.get('nextPageToken')

                    db.insert_data(collection_name = collection_name ,data = response)
                    if not next_page_token:
                        break
                    


                    

            logging.info(" The Data insertion from youtube API1 was successful")


                
            db.close_connection()

        except Exception as e:
            raise CustomException(e,sys)
        return None
    


    def get_channel_details(self , channels_id:list ,database_name , collection_name ):
        try:    
            chunk_size = 50
            db = Database(database_name=database_name)
            logging.info(f" Successfully connected to mongodb collection{collection_name}")

            channel_id_chunks = list(chunk_list(channels_id, chunk_size))
            next_page_token = None
            i = 1
            
            for chunk in channel_id_chunks:
                
                while True:
                    request = self.youtube.channels().list(
                        part="snippet,contentDetails,statistics",
                        id=','.join(chunk),
                        maxResults=50,  
                        pageToken=next_page_token,
                    )
                    response = request.execute()

                    print(f"I am in the {i} th iteration in the second API call")
                    i += 1
                    time.sleep(1)
                    #  Insert the ouput into the database
                    db.insert_data(collection_name = collection_name ,data = response)

                    next_page_token = response.get('nextPageToken')
                    if not next_page_token:
                        break

                


                    


            logging.info(" The Data insertion from youtube API2 was successful")
            db.close_connection()
        except Exception as e:
            raise CustomException(e,sys)
        return None
    