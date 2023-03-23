import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('files/output/depthOfCoverage/Illumina.csv', index_col=0, encoding='latin')

day = df["Date"]
sns.set(font_scale=1)
plt.figure(figsize=(10, 8))  # Set plot dimensions
g = sns.boxplot(x='Date', y='Depth of Coverage', data=df).set(title="Illumina Depth of coverage")
plt.xticks(rotation=85)

plt.savefig('files/output/depthOfCoverage/Illumina2.jpeg')
plt.show()
