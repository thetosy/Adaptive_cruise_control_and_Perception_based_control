import pandas as pd

df_train = pd.read_csv('data/train.csv')
X_train = df_train[['xmin', 'ymin', 'xmax', 'ymax']].values
print(X_train)

