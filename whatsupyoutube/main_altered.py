import os
import pprint
import urllib
from os.path import dirname, join

import pandas as pd
import requests
from dotenv import load_dotenv


pp = pprint.PrettyPrinter(indent=4)


class MissingEnvironmentVariable(Exception):
    pass


def get_env_var(var_name: str) -> str | Exception:
    try:
        return os.environ[var_name]
    except KeyError:
        raise MissingEnvironmentVariable(f"{var_name} does not exist")


def create_df(search_results) -> pd.DataFrame:
    df_array = [pd.DataFrame(pd.json_normalize(x)) for x in search_results]
    return pd.concat(df_array)


def main() -> None:
    load_dotenv()



    #api url components
    api_key = get_env_var("API_Key")

    channel_id = "UCX6OQ3DkcsbYNE6H8uQQuVA"
    

    #constructing the search api url
    base_url = "https://www.googleapis.com/youtube/v3"
    search_url = (
        f"search?key={api_key}"
        f"&channelId={channel_id}"
        f"&part=snippet,id&order=date&maxResults=50"
        
    )



    request_url = f"{base_url}/{search_url}"

    search_response = requests.get(request_url).json()
    
    next_page_token = search_response['nextPageToken']

    next_search_url = (
        f"search?key={api_key}"
        f"&channelId={channel_id}"
        f"&part=snippet,id&order=date&maxResults=50"
        f"&pageToken={next_page_token}"
        
    )

    next_search_response = f"{base_url}/{next_search_url}"
    next_page_search = requests.get(next_search_response)

    #while loop to page all the way through
    """while next_page_token is not None:
        next_page_search = next_search_url"""
         

    search_snippet = search_response["items"]
    
    #creating search api dataframe
    search_df = create_df(search_snippet)


    


    #search dataframe transformations

    
    #creating statistics dataframe
    video_ids = []
  
    for item in search_snippet:
        try:
            kind = item["id"]["kind"]
            if kind == "youtube#video":
                    video_ids.append(item["id"]["videoId"])
        except KeyError:
             print ("error")
    
    video_ids_updated = ','.join(video_ids)


    #constructing videos url
    video_url = (
        f"https://youtube.googleapis.com/youtube/v3/videos?id={video_ids_updated}"
        f"&part=statistics"
        f"&key={api_key}"
    )

    video_res = requests.get(video_url).json()
    video_res_items = video_res["items"]
    #print(create_df(video_res_items))
    #print(search_df)
    print(next_page_token)
   

    #video statistics dataframe transformations


main()
