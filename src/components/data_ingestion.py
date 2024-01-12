import os 
import sys 
from src.exception import CustomException
from src.logger import logging
import pandas as pd	
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.database.youtube_api.youtube_api import YoutubeAPI
import time 
from src.database.database import Database 


# --------------------------------

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
from src.utils import json_to_dataframe , extract_channel_information

@dataclass 
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    youtube_data_path: str=os.path.join('artifacts',"youtube_data.csv")
    raw_data_path: str=os.path.join('notebook\\data',"data.csv")
    api_data_path: str=os.path.join('notebook\\data',"api_data.csv")

class DataIngestion:
    # db = None
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        # self.db = Database(database_name)
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method , component")
        try:
            
            df = pd.read_csv("notebook\data\merged_data_youtube.csv" )
            logging.info("READ the dataset as the dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)

            df.to_csv(self.ingestion_config.raw_data_path , index=False , header=True)
            df.to_csv(self.ingestion_config.youtube_data_path , index=False , header=True)

           
            return (
                self.ingestion_config.raw_data_path,
                self.ingestion_config.youtube_data_path)

                    
    

        except Exception as e:

            raise CustomException(e,sys)
        



    def initiate_youtube_data_ingestion(self):

        try:

            logging.info("Starting Youtube Data Ingestion")

            df = pd.read_csv("notebook\data\merged_data_youtube.csv", engine='python')
            logging.info("READ the dataset as the dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.youtube_data_path), exist_ok = True)


            
            df.to_csv(self.ingestion_config.raw_data_path , index=False , header=True)
            df.to_csv(self.ingestion_config.youtube_data_path , index=False , header=True)

           
            return (
                self.ingestion_config.raw_data_path,
                self.ingestion_config.youtube_data_path)

                    

        except Exception as e:
            raise CustomException(e,sys)




        
    def create_dataset_api(self,query ,database_name, collection_name_store , collection_name ):
        #  Here We will call the get_channel_details method from YoutubeAPI = Pandas drtaframe 
        #  and we will save it as a csv file in artifacts folder and the data side will be done
        
          
        try:  
            # api = YoutubeAPI(api_key='AIzaSyATYkThBen84s6upBXF4cut_9sZ_FbPgbM') 
            api_ =  YoutubeAPI(api_key='AIzaSyB7eJGSt8grsTW7TaoorfN_9o81SDF5rvU')
            # Do the First API call function to get list of channel_ids 
            # api.get_all_videos(query ,database_name, collection_name_store)

            # logging.info(" get all Videos API call 1 function to get list of channel_ids is successful")

            # Create the database instance to be able to get the data from the database
            db = Database(database_name=database_name)

            logging.info(f" Successfully connect to a {database_name} database")

            # Retrieve the data from the database created via the  db1 instance
            json_data = db.get_data(collection_name_store)

            logging.info("Data Retrieval from the database1 is successful ")

            #  Call the json_to_dataframe function in order to transform the json data from mongo database into dataframe
            channels_id = json_to_dataframe(json_data)


            logging.info(" JSON from the database1 is successfully transformed into dataframe")

            #  Extract the channel_ids Column into a list of ids , to be able to use in the upcoming API Call 
            channels_id = channels_id['channel_id'].tolist()

            #  Remove the duplicates from the channel_ids 

            channels_id = list(set(channels_id))

            logging.info(" channels_id List is successfully created ")


            api_.get_channel_details(channels_id, database_name , collection_name )
                

            # Create the 1st inctance of the Database where we will store the first api call of getting channel_ids 's list



            logging.info(" The Data insertion from youtube API2 was successful")



            # Retrieve the data from the database created via the  db instance
            json_data = db.get_data( collection_name)

            logging.info(f"Data Retrieval from the {collection_name} is successful ")

            #  Call the json_to_dataframe function in order to transform the json data from mongo database into dataframe
            dataframe = extract_channel_information(json_data)

            dataframe.to_csv(self.ingestion_config.api_data_path,index = False , header=True)


        except Exception as e:
            raise CustomException(e,sys)
        return self.ingestion_config.api_data_path
    


if __name__ == "__main__":
    obj = DataIngestion()
    
    data_path = obj.initiate_youtube_data_ingestion()

    # print("Data Path:", data_path)

    data_transformation = DataTransformation()

    train_data , test_data = data_transformation.initiate_youtube_data_transformation(data_path[1])

    print( "train_data", train_data)
    print("Test data ",test_data) 
    
    model_trainer = ModelTrainer()

    model_trainer.model_trainer(train_data, test_data)

# #  This code is for Data Collection from the Youtube API
#     query= ['Artificial Intelligence','Deep Learning','machine Learning','LLM']

#     regionCode = ['US','CN','IN','BR','GB','RU','FR','DE','JP','CA','AU','KR','IT','ES','MX','ID','NL','SA','CH','TR']


#     api_data = obj.create_dataset_api(query=query , database_name='end2end-ml', collection_name='second_api', collection_name_store='channel_ids')



    # data_transformation = DataTransformation()

    # train_arr , test_arr,_ = data_transformation.initiate_youtube_data_transformation(train_data ,test_data)

    # model_trainer = ModelTrainer()

    # print(model_trainer.initiate_model_trainer(train_arr , test_arr))


