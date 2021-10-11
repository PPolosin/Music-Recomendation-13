# Return list of lists form DATA.csv for next work
import pandas as pd

df = pd.read_csv('DATA.csv') # Считывание в датафрейм
from google.colab import output
res = []
for i in range(1,19719):
  array = list(df[df['user'] == i]['artist'])# Добавление в массив исполнителей
  if (array!=[]): res.append(array)
