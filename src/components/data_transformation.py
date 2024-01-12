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


    def get_data_transformer_object(self):
        '''
        This Function is responsible for Data transformation ,
         
        returns the DataTransformation object'''

        try:
            numerical_features = ["writing score", "reading score"]
            categorical_features = ["gender", "race/ethnicity","parental level of education",
                                    "lunch", "test preparation course"]
            


            num_pipeline = Pipeline(

                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler(with_mean=False)),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy="most_frequent")),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False)),
                    ]
            )


            logging.info(f"Numerical Columns: {numerical_features}")
            logging.info(f"Categorical Columns: {categorical_features}")


            """
            Create a ColumnTransformer object and combine the numerical and categorical pipelines
            """
            prerocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_features),
                    ("cat_pipeline",cat_pipeline, categorical_features)
                    ],

            )
            return prerocessor


        except Exception as e:
            raise CustomException(e,sys)
        


    def get_youtube_data_transformer_object(self):

        '''
        This Function is responsible for Data transformation ,
         
        returns the DataTransformation object'''

        try:
            pass





        except Exception as e:
            raise CustomException(e,sys)







        
    def initiate_data_transformation(self, train_path, test_path):
        """
            This function is responsible for reading the training and test data, applying the preprocessing object, and saving the transformed data
        """
        try:
            """
                Read the training and test data from CSV files
            """
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read the Training data and Test data completed ")
            logging.info(" Obtaining preprocessing object")

            preprocess_obj = self.get_data_transformer_object()
            target_column_name ="math score" 
            numerical_features = ["writing score", "reading score"]


            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]


            logging.info(f"Applying preprocessing object on training data dataframe and testing dataframe ")

            input_feature_train_arr = preprocess_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocess_obj.transform(input_feature_test_df)


            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr= np.c_[input_feature_test_arr, np.array(target_feature_test_df)]


            logging.info(f"Saved Preprocessing object .")



            save_object(

            file_path = self.data_transformation_config.preprocessor_obj_file_path,
            obj = preprocess_obj

            )


            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:

            raise CustomException(e,sys)
        



        
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
        