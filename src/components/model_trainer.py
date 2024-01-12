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

    def initiate_model_trainer(self,train_arr, test_arr):
        try:
            logging.info("Split training & testing input data")

            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1], 
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]

            ) 

            models = {
                "Random Forest" : RandomForestRegressor(),
                "Decision Tree" : DecisionTreeRegressor(),
                "Gradient Boosting" : GradientBoostingRegressor(),
                "Linear Regression" : LinearRegression(),
                "K_Neighbors Regressor" : KNeighborsRegressor(),
                "XGBRegressor" : XGBRegressor(),
                "CatBoosting Regressor" : CatBoostRegressor(verbose=False),
                "AdaBoost Regressor" : AdaBoostRegressor(),

            }

            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "K_Neighbors Regressor":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }






            model_report:dict= evaluate_model(X_train=X_train , y_train=y_train,X_test=X_test,y_test = y_test , models = models , param = params)

            # Best Model score from model_report dictionary

            best_model_score = max(sorted(model_report.values()))

            # Get the Name of the best model score from model_report dictionary 

            best_model_name = list(model_report.keys())[ list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException('No best model score found ')

            logging.info(f"Best model score found on both Training and Test dataset ")


           
            # Use the preprocessor object to transform new data
            # preprocessor_obj = pickle.load('artifacts\preprocessor.pkl')
            # new_data = ...
            # preprocessed_data = preprocessor.transform(new_data)


            save_object(
                file_path= self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square   
        except Exception as e:
            raise CustomException(e,sys)


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



