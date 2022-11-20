import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

df = pandas.read_csv("moon.csv")

d = {'food1': 1,
     'food2': 2,
     'food3': 3,
     'food4': 4,
     'food5': 5,
     'food6': 6,
     'food7': 7,
     'food10': 10}
# df['Food'] = df['Food'].map(d)

features = ['SDeg', 'MDeg', 'Taste']
X = df[features]
y = df['Food']

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

# Deg,Exp,Taste,Food    00,10,9,F1
# print(dtree.predict([[60, 10, 7]]))
# print(dtree.predict([[250, 12, 7]]))

# 74 ,	 90 ,	 5 ,	 1
# 94 ,	 161 ,	 9 ,	 4
# 202 ,	 326 ,	 5 ,	 5

listval = dtree.predict([[202, 326, 5]])
key = list(d.keys())[list(d.values()).index(listval[0])]

print(key)

