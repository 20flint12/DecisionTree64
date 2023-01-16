import pandas as pd
print("pd.__version__", pd.__version__)

# df = pd.read_csv('moon_zodiac.csv')
#
# # print(df.head(0)[0], df.head(0)[1])
# print(df.head(0))
#
# print(df.columns[0])
# print(df.columns.dtype)

# first_column_name = df.iloc[:, 1].name
# print(first_column_name)

# print(df.head(1))
# print(df.info())
# print(df.loc[1]["description"])

# res = df.loc[1].to_dict()
# print(res)


lon = 44354.55

zod_id = int((lon % 360) / 30) + 1

print(lon, zod_id)



