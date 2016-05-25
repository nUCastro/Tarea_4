import numpy as np
from pylab import *
from scipy.special import gammaincinv as gi
from scipy.special import gamma
import matplotlib.pyplot as plt
a=np.random.random(size=10000)
def chi2(x,df):
	return 1.0 / (2*gamma(df/2)) * (x/2)**(df/2-1) * exp(-x/2)
nu=120
b,c=[],[]
for i in a:
	b.append(2*gi(nu/2.0,i))
print len(b)
print max(b),min(b)	
plt.hist(b,bins=150)
d=np.linspace(min(b),max(b),100)
for i in range(len(d)):
	c.append(10000*(chi2(d[i],nu)))
print c	
plt.plot(d,c,'-r')	
#plt.savefig(str(nu)+'.png')
plt.show()
