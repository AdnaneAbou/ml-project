import sys
import os 
from dataclasses import dataclass


import pandas as pd
from catboost import CatBoostRegressor
from sklearn.ensemble import (
        AdaBoostRegressor,  
        GradientBoostingRegressor,
        RandomForestRegressor) 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging 
from src.utils import save_object, evaluate_model
import pickle


#  ----------------------------------------------------------------

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()


    def model_trainer(self , train_data, test_data):

        try:

            

            logging.info("Model trainer started ")

            train_data_csv = pd.read_csv(str(train_data))
            test_data_csv = pd.read_csv(str(test_data)) 

            xtrain = train_data_csv[['std_category_id','std_likes','std_dislikes','std_comment_count','std_desc_len','std_len_title']] 
            ytrain = train_data_csv['std_views']
            xtest = test_data_csv[['std_category_id','std_likes','std_dislikes','std_comment_count','std_desc_len','std_len_title']] 
            ytest = test_data_csv['std_views']


            logging.info("reading training and testing as dataframes and splitting is done successfully")

            # xtrain , xtest , ytrain  , ytest = (
            #     train_data_csv[:,:-1], 
            #     train_data_csv[:,-1],
            #     test_data_csv[:,:-1],
            #     test_data_csv[:,-1]
            # ) 

            dt = DecisionTreeRegressor()
            dt.fit(xtrain, ytrain)

            logging.info("The Model trained successfully")

            
            
            save_object(
                file_path= self.model_trainer_config.trained_model_file_path,
                obj = dt
            )



            logging.info("Model saved as pickle file ")

            predictions = dt.predict(xtest)

            r2 = r2_score(ytest,predictions)

            return r2
           


        

            
        except Exception as e:
            raise CustomException(e,sys)




