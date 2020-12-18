import json
import pandas as pd


def load():
    with open("../json/top-rated-movies-02.json") as f:
        data = json.load(f)
        # print(data)
        df = pd.DataFrame(data)
    return df


# JSON to DataFrame
def json_to_df():
    dataframe = load()

    # type conversion
    # list to string for movie_genre_relationship table
    dataframe['genres'] = dataframe['genres'].astype('str').apply(
        lambda x: x.lower().strip().replace("[", "").replace("]", "")
            .replace("\'", "").replace("\"", "").replace(", ", ","))

    # extract relevant duration PT89M --> 89
    dataframe['duration'] = dataframe['duration'].astype('str').apply(
        lambda x: x.strip().replace("PT", "").replace("M", "")).astype(int)

    # string to float conversion
    dataframe['imdbRating'] = dataframe['imdbRating'].astype('float')

    # handling names like Genelia D'Souza which was causing string handling issues
    dataframe['actors'] = dataframe['actors'].astype('str').apply(
        lambda x: x.lower().strip().replace("[", "").replace("]", "").
            replace("\'", "").replace("\"", "").replace(", ", ","))
    return dataframe
