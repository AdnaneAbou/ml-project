import sys
import os 
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler , MinMaxScaler
from sklearn.model_selection import train_test_split


from src.exception import CustomException
from src.logger import logging


from src.utils import save_object



#  ---------- ----------------

@dataclass
class DataTransformationConfig:
    """
    DataTransformationConfig is responsible for defining the file path for the preprocessing object
    """

    # preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")
    train_data_path: str=os.path.join('artifacts',"youtube_train.csv")
    test_data_path: str=os.path.join('artifacts',"youtube_test.csv")

    



class DataTransformation:

    
    def __init__(self):
        """
        This class is responsible for creating the preprocessing object and applying it to the training and test data
        """
        self.data_transformation_config = DataTransformationConfig()



        
    def initiate_youtube_data_transformation(self, data_path):
        """
            This function is responsible for reading the youtube data, applying the Necessarcy processing and split it into Train and Test 
        """

        try:
            data = pd.read_csv(data_path , engine='python')

            #  Creating new Features , length of tilte & description


            data['len_title'] = data['channel_title'].str.len()
            data['desc_len'] = data['description'].str.len()
            columns_to_convert =  ["views","likes","dislikes"]

            for column in columns_to_convert:
                data[column] = pd.to_numeric(data[column], errors='coerce')

            logging.info("views, likesdislikes Columns converted successfully ")

            data_clean = data.drop(['description','title','channel_title','tags','publish_time','thumbnail_link','video_id','trending_date','comments_disabled','ratings_disabled','video_error_or_removed'], axis=1)
            
            # Fill Missing Values
            
            data_clean.fillna(data_clean.median(), inplace=True)

            #  Drop Duplicates

            data_clean = data_clean.drop_duplicates()

            logging.info("Filling missing values and duplicate values")

            #  Log Transformation

            features = ['category_id','views','likes','dislikes','comment_count','desc_len','len_title']
            df_pre = data_clean.copy()
            for var in features:
                df_pre['log_'+var]= (data_clean[var]+1).apply(np.log)

            logging.info("Log transformation done succcessfully")

            #  Normalization 
                
            for var in features:
                # df_pre['std_'+var]= MinMaxScaler().fit_transform(df_pre[var].clean.reshape(len(df_pre), 1))
                df_pre['std_'+var]= MinMaxScaler().fit_transform(df_pre[var].values.reshape(-1, 1))
            

            
            logging.info("Normalization done successfully & Train Test Data Initiated ")


            #  Split the data into training and test for the features and target variable 


            train_set , test_set = train_test_split(df_pre , test_size=0.2 , random_state=42)

            train_set.to_csv(self.data_transformation_config.train_data_path,index = False , header=True)
            test_set.to_csv(self.data_transformation_config.test_data_path,index = False , header=True)

            
            logging.info("Ingestion of the Data Completed successfully ")
            
            return (
                self.data_transformation_config.train_data_path,
                self.data_transformation_config.test_data_path)


        

        except Exception as e:

            raise CustomException(e,sys)
        