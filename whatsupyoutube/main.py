import os
import pprint
import urllib
from os.path import dirname, join

import pandas as pd
import requests
from dotenv import load_dotenv


# Defining pretty print variable
pp = pprint.PrettyPrinter(indent=4)


class MissingEnvironmentVariable(Exception):
    pass

# Function to get the environment variables
def get_env_var(var_name: str) -> str | Exception:
    try:
        return os.environ[var_name]
    except KeyError:
        raise MissingEnvironmentVariable(f"{var_name} does not exist")

# Function to normalize the json from the api call and create a dataframe
def create_df(search_results) -> pd.DataFrame:
    df_array = [pd.DataFrame(pd.json_normalize(x)) for x in search_results]
    return pd.concat(df_array)


def main() -> None:
    load_dotenv()



    # Defining API Key and Channel ID variables
    api_key = get_env_var("API_Key")
    channel_id = get_env_var("Channel_Id")
    

    # Base url and Search specific components that together construct the url needed to call from the Search API - https://developers.google.com/youtube/v3/docs/search
    base_url = "https://www.googleapis.com/youtube/v3"
    search_url = (
        f"search?key={api_key}"
        f"&channelId={channel_id}"
        f"&part=snippet,id&order=date&maxResults=50"
        
    )

    # Constructing Search url by combining base_url and search_url variables
    request_url = f"{base_url}/{search_url}"


    # Defining the variable that holds the json response of the Search url
    search_response = requests.get(request_url).json()


    # Indexing through the Search api call to the items key as it contains the data we're looking for
    search_snippet = search_response["items"]
    

    # Utilizing the create_df function that will normalize the json in the items key and creates a DataFrame from it
    search_df = create_df(search_snippet)


    # Defining the variable that holds the json response of the Search url
    search_response = requests.get(request_url).json()


    # Indexing through the Search api call to the items key as it contains the data we're looking for
    search_snippet = search_response["items"]


    # Utilizing the create_df function that will normalize the json in the items key and creates a DataFrame from it
    search_df = create_df(search_snippet)
    

    # Grabbing the next page token from the nextPageToken key from the top of the Search api call
    next_page_token = search_response['nextPageToken']
    

    # Constructing the URL needed to loop through all pages of the Search api call
    next_search_url = (
        f"search?key={api_key}"
        f"&channelId={channel_id}"
        f"&part=snippet,id&order=date&maxResults=50"
        f"&pageToken={next_page_token}"
        
    )

    next_search_response = f"{base_url}/{next_search_url}"
    next_page_search = requests.get(next_search_response)

    # Creating the while loop that will loop through all pages of the Search api call
    """while next_page_token is not None:
        next_page_search = next_search_url"""
         

    # Creating an empty list to store the video ids retrieved from the Search api call
    video_ids = []
  
    # Loops through the items key in the Search api call to create a list of video ids needed for the video statistics api call
    for item in search_snippet:
        try:
            kind = item["id"]["kind"]
            if kind == "youtube#video":
                    video_ids.append(item["id"]["videoId"])
        except KeyError:
             print ("error")
    
    video_ids_updated = ','.join(video_ids)


    # Constructing videos url for the videos api call - https://developers.google.com/youtube/v3/docs/videos
    video_url = (
        f"https://youtube.googleapis.com/youtube/v3/videos?id={video_ids_updated}"
        f"&part=statistics"
        f"&key={api_key}"
    )

    # Defining the variable that holds the json response of the Videos url
    video_res = requests.get(video_url).json()
    
    
    # Indexing through the Videos api call to the items key as it contains the data we're looking for
    video_res_items = video_res["items"]

    # Creating video statistics dataframe
    #print(create_df(video_res_items))

   



main()
