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




api_key = "AIzaSyBT0b-OYNZX6X9m3jmsRHIuLHzg9wVisek"

channel_id = "UCVRobwJfa8nHMfJI3C8Rgdw"
page_token = ""

base_url = "https://www.googleapis.com/youtube/v3"
search_url = (
        f"search?key={api_key}"
        f"&channelId={channel_id}"
        f"&part=snippet,id&order=date&maxResults=1000{page_token}"
    )

request_url = f"{base_url}/{search_url}"

search_response = requests.get(request_url).json()
search_snippet = search_response["items"]

#trying to create a loop to iterate thru the different video ids
"""for item in search_snippet:
    try:
        kind = item["id"]["kind"]
        if kind == 'youtube#video':
            video_id = item['id']['videoId']   
    except KeyError:
        print("error")"""


search_df = create_df(search_snippet)

video_id = search_df["id.videoId"]



video_url = (
        f"https://youtube.googleapis.com/youtube/v3/videos?id={video_id}"
        f"&part=statistics&key={api_key}"
        f"&maxResults=1000&channelId={channel_id}&order=date"
        )

video_res = requests.get(video_url).json()

pp.pprint(video_res)
pd.set_option('display.max_columns', None)

#print(search_df.head())
#print(video_id)
