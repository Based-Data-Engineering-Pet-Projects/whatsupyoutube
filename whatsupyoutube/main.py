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

    api_key = get_env_var("API_KEY")

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

    search_df = create_df(search_snippet)

    video_id = search_df["id.videoId"]

    video_url = (
        f"https://youtube.googleapis.com/youtube/v3/videos?id={video_id}"
        "&part=statistics&key=AIzaSyBT0b-OYNZX6X9m3jmsRHIuLHzg9wVisek"
        "&maxResults=1000&channelId=UCVRobwJfa8nHMfJI3C8Rgdw&order=date"
    )

    video_res = requests.get(video_url).json()

    pp.pprint(video_res)


main()
