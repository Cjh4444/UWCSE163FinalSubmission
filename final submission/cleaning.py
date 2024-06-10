import pandas as pd
from pandas import DataFrame
from ast import literal_eval


def q1_data_cleaning(main_df: DataFrame, stream_df: DataFrame) -> DataFrame:
    """
    Combines and returns the combined DataFrame of main_df
    and stream_df

    Args:
        main_df (DataFrame): main DataFrame
        stream_df (DataFrame): stream DataFrame

    Returns:
        DataFrame: combined Dataframe of main and stream
    """
    main_df_clean = main_df.drop_duplicates(subset="track_id")
    main_df_clean = main_df_clean.dropna()

    stream_df_clean = stream_df.drop(columns=["Date", "Position"])

    stream_df_clean = stream_df_clean.dropna()

    stream_df_clean["Genre"] = stream_df_clean["Genre"].apply(literal_eval)

    # Group by 'Track Name' and 'Artist',
    # sum the 'Streams', and aggregate genres
    stream_grouped = (
        stream_df.groupby(["Track Name", "Artist"])
        .agg(
            {
                "Streams": "sum",
                "Genre": lambda x: list(
                    set([genre for sublist in x for genre in sublist])
                ),
            }
        )
        .reset_index()
    )

    sorted_stream_group = stream_grouped.sort_values(
        "Streams", ascending=False
    )

    merged_df = main_df_clean.merge(
        sorted_stream_group,
        left_on=["track_name", "track_artist"],
        right_on=["Track Name", "Artist"],
    )

    is_pop = merged_df["playlist_genre"] == "pop"
    df = merged_df[is_pop]

    relevant_cols = [
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "Streams",
    ]

    important_df = df[relevant_cols]

    return important_df


def q1_data_loading() -> tuple[DataFrame, DataFrame]:
    """
    Loads the csvs into DataFrames and returns them

    Returns:
        tuple[DataFrame, DataFrame]: csv to DataFrame
    """
    main_df = pd.read_csv("data/spotify_songs.csv")
    stream_df = pd.read_csv("data/stream_data.csv", sep="#")

    return main_df, stream_df


def get_q1_df() -> DataFrame:
    """
    Returns DataFrame for Q1 analysis

    Returns:
        DataFrame: merged, cleaned DataFrame
    """
    main_df, stream_df = q1_data_loading()

    merged_df = q1_data_cleaning(main_df, stream_df)
    return merged_df


def q2_data_cleaning(df: DataFrame) -> tuple[DataFrame, list]:
    """
    Combines and returns cleaned DataFrame

    Args:
        df (DataFrame): _description_

    Returns:
        tuple[DataFrame, list]: cleaned dataFrame and age groups
    """
    df = df.drop(df.columns[0], axis=1)

    important_cols = ["Age", "fav_music_genre"]
    important_data = df[important_cols]

    # important age groups have a decent amount of individuals
    important_age_groups = ["12-20", "20-35", "35-60"]
    age_group_filter = important_data["Age"].isin(important_age_groups)
    important_data = important_data[age_group_filter]

    return important_data, important_age_groups


def q2_data_loading() -> DataFrame:
    """
    Loads the data for Q2

    Returns:
        DataFrame: DataFrame of xlsx file
    """
    excel_file = pd.read_excel("data/user_questions.xlsx")
    excel_file.to_csv("data/user_questions.csv")

    return pd.read_csv("data/user_questions.csv")


def get_q2_df() -> tuple[DataFrame, list]:
    """
    Returns the DataFrame for the Q2 and necessary columns

    Returns:
        tuple[DataFrame, list]: DataFrame for the Q2 and necessary columns
    """
    df = q2_data_loading()

    return q2_data_cleaning(df)


def q3_data_cleaning(df) -> tuple[DataFrame, DataFrame, DataFrame]:
    """
    Returns the 3 DataFrames for Q3 that are relevant per attribute

    Args:
        df (DataFrame): Q3 Data

    Returns:
        tuple[DataFrame, DataFrame, DataFrame]: Relevant DataFrames
    """
    tempo_df = df["tempo"]
    key_df = df["key"]
    duration_df = df["duration_ms"]

    tempo_counts = (
        tempo_df.astype(int)
        .value_counts(sort=False)
        .rename_axis("unique_values")
        .reset_index(name="counts")
        .sort_values(by="unique_values")
    )

    key_counts = (
        key_df.value_counts(sort=False)
        .rename_axis("unique_values")
        .reset_index(name="counts")
        .sort_values(by="unique_values")
    )

    duration_counts = (
        duration_df.round(-3)
        .divide(1000)
        .astype(int)
        .value_counts(sort=False)
        .rename_axis("unique_values")
        .reset_index(name="counts")
        .sort_values(by="unique_values")
    )

    return tempo_counts, key_counts, duration_counts


def q3_data_loading() -> DataFrame:
    """
    Loads the data for Q3

    Returns:
        DataFrame: Q3 Data
    """
    return pd.read_csv("data/1000songdata.csv")


def get_q3_df():
    """
    Gets DataFrame for Q3

    Returns:
        _type_: Cleaned DataFrame
    """
    df = q3_data_loading()

    return q3_data_cleaning(df)
