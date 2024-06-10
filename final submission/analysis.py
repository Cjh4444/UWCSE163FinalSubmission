import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cleaning
import numpy as np


def q1_analysis():
    """
    Provides the graphs to Q1:
    Is there a correlation between certain attributes and song popularity?
    """
    df = cleaning.get_q1_df()

    corr_matrix = df.corr()

    popularity_corr = corr_matrix["Streams"].drop("Streams")

    plt.figure(figsize=(20, 15))

    sns.barplot(x=popularity_corr.index, y=popularity_corr.values)

    plt.xticks(rotation=90)
    plt.xlabel("Factors")
    plt.ylabel("Correlation with # of Streams")
    plt.title("Correlation of Factors with # of Streams")
    plt.savefig("output/Q1_correlation_graph")
    plt.close()


def q2_analysis():
    """
    Provides the graphs to Q2:
    How does the age of a listener affect their preferences in music genres?
    """
    df, age_groups = cleaning.get_q2_df()

    fig, [ax1, ax2, ax3] = plt.subplots(ncols=3, figsize=(15, 20))

    axes = [ax1, ax2, ax3]

    for age, axis in zip(age_groups, axes):
        is_age = df["Age"] == age
        age_df = df[is_age]

        genre_counts = age_df["fav_music_genre"].value_counts()

        axis.bar(genre_counts.index, genre_counts.values)

        axis.set_xlabel("Favorite Music Genre")
        axis.set_ylabel("Count")
        axis.set_title(
            f"{age}",
            fontdict={"fontsize": 20},
        )

        axis.tick_params(axis="x", rotation=90)

    plt.savefig("output/Q2_bar_graphs")
    plt.close()


def q3_analysis():
    """
    Provides the graphs to Q3:
    What are the most common musical elements among songs in the top 1000?
    """
    tempo_counts, key_counts, duration_counts = cleaning.get_q3_df()

    ax = tempo_counts.plot(
        kind="bar",
        x="unique_values",
        y="counts",
        color="skyblue",
        legend=False,
    )

    ax.set_xlabel("Tempo")
    ax.set_ylabel("Count")
    ax.set_title("Tempo Counts")
    ax.set_xticks(np.arange(0, 203, step=5))
    ax.set_xlim(
        0,
        tempo_counts["unique_values"].max()
        - tempo_counts["unique_values"].min()
        - 11,
    )

    plt.savefig("output/Q3_tempo_counts")
    plt.close()

    ax = key_counts.plot(
        kind="bar",
        x="unique_values",
        y="counts",
        color="skyblue",
        legend=False,
    )

    ax.set_xlabel("Key")
    ax.set_ylabel("Count")
    ax.set_title("Key Counts")
    ax.set_xticks(
        np.arange(
            -1,
            12,
        )
    )
    ax.set_xlim(-1, key_counts["unique_values"].max() + 1)

    plt.savefig("output/Q3_key_counts")
    plt.close()

    ax = duration_counts.plot(
        kind="bar",
        x="unique_values",
        y="counts",
        color="skyblue",
        legend=False,
    )

    ax.set_xlabel("Duration (seconds)")
    ax.set_ylabel("Count")
    ax.set_title("Duration Counts")
    ax.set_xticks(np.arange(0, 600, step=10))
    ax.set_yticks(np.arange(0, 21, step=3))

    ax.set_xlim(
        0,
        220,
    )

    plt.savefig("output/Q3_duration_counts")
    plt.close()


def q1_test():
    """
    Test cases for Q1
    """
    df = pd.read_csv("data/test/testing_song_features.csv")
    corr_matrix = df.corr()

    popularity_corr = corr_matrix["Streams"].drop("Streams")

    plt.figure(figsize=(20, 15))
    palette = [
        "#D98672" if value < 0 else "#859FE5"
        for value in popularity_corr.values
    ]
    sns.barplot(
        x=popularity_corr.index, y=popularity_corr.values, palette=palette
    )

    plt.xticks(rotation=90)
    plt.xlabel("Factors")
    plt.ylabel("Correlation with # of Streams")
    plt.title("Correlation of Factors with # of Streams")
    plt.savefig("output/Q1_test")
    plt.close()


def q2_test():
    """
    Test cases for Q2
    """
    df = pd.read_csv("data/test/testing_age_genre.csv")

    fig, ax = plt.subplots(1)

    genre_counts = df["fav_music_genre"].value_counts()

    ax.bar(genre_counts.index, genre_counts.values)

    ax.set_xlabel("Favorite Music Genre")
    ax.set_ylabel("Count")
    ax.set_title(
        "1-99",
        fontdict={"fontsize": 20},
    )

    plt.savefig("output/Q2_test")
    plt.close()


def q3_test():
    """
    Test cases for Q3
    """
    df = pd.read_csv("data/test/testing_tempo.csv")

    ax = df.plot(
        kind="bar",
        x="unique_values",
        y="counts",
        color="skyblue",
        legend=False,
    )

    ax.set_xlabel("Tempo")
    ax.set_ylabel("Count")
    ax.set_title("Tempo Counts")
    ax.set_xticks(
        np.arange(
            0,
            87,
        )
    )
    ax.set_xlim(-1, df["unique_values"].max() - df["unique_values"].min() - 1)

    plt.savefig("output/Q3_test")
    plt.close()


def main():
    """
    Main method: runs all analyses and tests
    """
    q1_analysis()
    # q1_test()
    # q2_analysis()
    # q2_test()
    # q3_analysis()
    # q3_test()


if __name__ == "__main__":
    main()
