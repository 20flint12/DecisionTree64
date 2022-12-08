import pandas as pd
print(pd.__version__)

df = pd.read_csv('moon_zodiac.csv')
# df = pd.read_json('moon_zodiac.json')

print(df.head(5))

print(df.info())

print(df.loc[1]["description"])

print(df.__len__())
# res = df.loc[1].to_dict()
# print(res)

