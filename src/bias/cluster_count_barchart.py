import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('files/output/PhylogeneticTree/cluster_count.csv')
print(df, df['count'])
plt.bar(df['cluster'], df['count'])
plt.xticks(rotation=45,fontsize=7)

plt.xlabel('clusters')
plt.ylabel('number of variants per cluster')
plt.title('Distribution of variants in each country in clusters')
plt.savefig('files/output/PhylogeneticTree/cluster_count_barchart.jpeg', dpi=1600)

plt.show()