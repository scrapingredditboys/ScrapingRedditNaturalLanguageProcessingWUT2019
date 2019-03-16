import pandas as pd
import pandas.io as io

csv = pd.read_csv("comments.csv", sep=";", parse_dates=True)
df = pd.DataFrame(columns=["word", "uses", "unique", "karma"])
df.set_index('word', drop=True, inplace=True)

for index,row in csv.iterrows():
    words = row['comment'].lower().split(" ")
    for word in words:
        if word not in df.index:
            df.loc[word] = [0] * df.columns.size
        df['uses'][word] += 1
    for word in set(words):
        df["unique"][word] += 1
        df["karma"][word] += row['karma']
        

df.to_csv(path_or_buf="comment_count.csv")
