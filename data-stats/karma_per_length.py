import pandas as pd
import pandas.io as io

csv = pd.read_csv("comments.csv", sep=";", parse_dates=True)
df = pd.DataFrame(columns=["length", "karma"])

for index,row in csv.iterrows():
    length = len(row['comment'])
    df.loc[len(df)] = [length, row['karma']]

df.to_csv(path_or_buf="karma_count.csv")
