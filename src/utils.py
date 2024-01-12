import os 
import sys

import numpy as np
import pandas as pd
import dill # TO CHECK THIS
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
import pymongo 



def save_object(file_path, obj):

    """ Saves a Python object to a file using pickle.

    Parameters:
    - file_path (str): The path where the object will be saved.
    - obj (object): The Python object to be saved.

    Raises:
    - CustomException: If there is an error during the save process. """

    try:

        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:

            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    

def evaluate_model(X_train, y_train, X_test ,y_test,  models , param ):
    """
    Evaluates machine learning models using GridSearchCV.

    Parameters:
    - X_train (array-like): Training input data.
    - y_train (array-like): Training target values.
    - X_test (array-like): Testing input data.
    - y_test (array-like): Testing target values.
    - models (dict): Dictionary containing machine learning models.
    - param (dict): Dictionary containing parameter grids for models.

    Returns:
    - dict: Dictionary containing model names and their corresponding R2 scores on the test set.

    Raises:
    - CustomException: If there is an error during the evaluation process.
    """


    try:

        report = {}


        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]
            


            gs = GridSearchCV(model, para,cv=3)
            gs.fit(X_train, y_train)

            


            model.set_params(**gs.best_params_)

            model.fit(X_train, y_train)


            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score




        return report

    except Exception as e:
        raise CustomException(e,sys)
    

def load_object(file_path):

    """
    Loads a Python object from a file using pickle.

    Parameters:
    - file_path (str): The path from which to load the object.

    Returns:
    - object: The loaded Python object.

    Raises:
    - CustomException: If there is an error during the load process.
    """

    try:
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)
    




def json_to_dataframe(json_data):
    """
    Converts JSON data containing information about YouTube videos into a Pandas DataFrame.

    Parameters:
    - json_data (list): A list containing JSON data retrieved from the YouTube API.

    Returns:
    - pd.DataFrame: A Pandas DataFrame containing relevant information about each video.
    """

    all_data = []

    for item in json_data:
        for video_item in item.get('items', []):
            video_info = {
                # 'video_id': video_item['id']['videoId'],
                'published_at': video_item['snippet']['publishedAt'],
                'channel_id': video_item['snippet']['channelId'],
                'title': video_item['snippet']['title'],
                'description': video_item['snippet']['description'],
                'thumbnail_url': video_item['snippet']['thumbnails']['default']['url'],
                'channel_title': video_item['snippet']['channelTitle'],
                'live_broadcast_content': video_item['snippet']['liveBroadcastContent'],
                'publish_time': video_item['snippet']['publishTime']
            }
            all_data.append(video_info)


    # Create a DataFrame from the extracted data
    df = pd.DataFrame(all_data)

    return df




def extract_channel_information(json_data):
    """
        Extract more information from the provided JSON data.

        Parameters:
        - json_data: The JSON data representing channel information.

        Returns:
        - A list of dictionaries containing extracted information for each channel.
        """
    result = []
    
    for item in json_data:
        channels = item.get('items', [])
        for channel in channels:
            channel_info = {}
            
            # Extract channel information
            channel_info['channel_id'] = channel['id']
            channel_info['channel_title'] = channel['snippet']['title']
            channel_info['description'] = channel['snippet']['description']
            channel_info['custom_url'] = channel['snippet'].get('customUrl', '')
            channel_info['published_at'] = channel['snippet']['publishedAt']
            channel_info['thumbnails_default'] = channel['snippet']['thumbnails']['default']['url']
            channel_info['thumbnails_medium'] = channel['snippet']['thumbnails']['medium']['url']
            channel_info['thumbnails_high'] = channel['snippet']['thumbnails']['high']['url']
            channel_info['country'] = channel['snippet'].get('country', '')
            
            # Extract content details
            content_details = channel.get('contentDetails', {})
            channel_info['uploads_playlist'] = content_details['relatedPlaylists']['uploads']
            
            # Extract statistics
            statistics = channel.get('statistics', {})
            channel_info['view_count'] = statistics.get('viewCount', '')
            channel_info['subscriber_count'] = statistics.get('subscriberCount', '')
            channel_info['hidden_subscriber_count'] = statistics.get('hiddenSubscriberCount', False)
            channel_info['video_count'] = statistics.get('videoCount', '')
            
            result.append(channel_info)
    
    # Create DataFrame
    df = pd.DataFrame(result)
    
    return df









def dataframe_to_csv(dataframe, file_path, index=False):
    """
    Save a Pandas DataFrame to a CSV file.

    Parameters:
    - dataframe: Pandas DataFrame to be saved.
    - file_path: File path where the CSV file will be saved.
    - index: Whether to include the index in the CSV file (default is False).
    - encoding: Encoding to be used for the CSV file (default is 'utf-8').
    """
    dataframe.to_csv(file_path, index=index)
    print(f"DataFrame saved to {file_path}")





def chunk_list(original_list, chunk_size):
    """Split a list into chunks of a specified size."""
    for i in range(0, len(original_list), chunk_size):
        yield original_list[i:i + chunk_size]

