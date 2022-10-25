import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

with open("forum_posts.json", "r") as file:
    posts = json.load(file)

def add_interaction(users, from_user, to_user):
    if from_user not in users:
        users[from_user] = {}
    if to_user not in users[from_user]:
        users[from_user][to_user] = 0
    users[from_user][to_user] += 1

# create interactions dictionary
users = {}
for thread in posts[:5]:
    first_one = None
    for post in thread:
        user = post["user"]
        quoted = post.get("quoted")
        if not first_one:
            first_one = user
        elif not quoted:
            add_interaction(users, user, first_one)
        else:
            for quoted_user in quoted:
                add_interaction(users, user, quoted_user)

    # stop at frst thread
    # break

try:
    df = pd.DataFrame.from_dict(users, orient="index").fillna(0)

    heatmap = plt.pcolor(df, cmap="Blues")
    y_vals = np.arange(0.5, len(df.index), 1)
    x_vals = np.arange(0.5, len(df.columns), 1)
    plt.yticks(y_vals, df.index)
    plt.xticks(x_vals, df.columns, rotation="vertical")

    for y in range(len(df.index)):
        for x in range(len(df.columns)):
            if df.iloc[x, y] == 0:
                continue
            plt.text(x+0.5, y+0.5, "%.0f" % (df.iloc[x,y]), horizontalalignment="center", verticalalignment="center")
except IndexError as ie:
    print(ie)

plt.show()