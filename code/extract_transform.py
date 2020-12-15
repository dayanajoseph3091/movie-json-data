import json
import pandas as pd


# def load_json(data):
    # Load JSON
#x=pd.DataFrame()
def load():
    with open("../json/top-rated-movies-02.json") as f:
        data = json.load(f)
        # print(data)
        df = pd.DataFrame(data)
    return df

#print(load(x))
# JSON to DataFrame
def json_to_df():
    dataframe = load()
    print(dataframe)
    #dataframe
    # type conversion
    dataframe['genres'] = dataframe['genres'].astype('str').apply(
        lambda x: x.lower().strip().replace("[", "").replace("]", "").replace("\'", "").replace("\"", "").replace(", ",
                                                                                                                  ","))
    dataframe['ratings'] = dataframe['ratings'].astype('str')

    dataframe['duration'] = dataframe['duration'].astype('str').apply(
        lambda x: x.strip().replace("PT", "").replace("M", "")).astype(int)
    dataframe['imdbRating'] = dataframe['imdbRating'].astype('float')
    dataframe['actors'] = dataframe['actors'].astype('str').apply(
        lambda x: x.lower().strip().replace("[", "").replace("]", "").replace("\'", "").replace("\"", "").replace(", ",
                                                                                    ","))
    return dataframe
