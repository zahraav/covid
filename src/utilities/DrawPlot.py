from scipy.stats import chisquare
import seaborn as sns
import matplotlib.pyplot as plt


datalist=([6,8,6,4,2,2])
print(' --> ',chisquare([16, 18, 16, 14, 12, 12]))
f_obs=datalist
#scipy.stats.chisquare(f_obs,f_exp=None,ddof=0,axis=0)
#sns.lmplot(x="internetuserate", y="lifeexpectancy", data=datalist, fit_reg=False)
#plt.title("Internet Use Rate and Employment Rate")
#plt.show()
