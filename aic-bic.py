import numpy as np
from pylab import *
import matplotlib.pyplot as plt

f=open("datos.dat","r")
x=f.readline()
x=f.read()
f.close()
x=x.split()
t,f,error=[],[],[]
for i in range(len(x)/3):
	t.append(float(x[3*i]))
	f.append(float(x[3*i+1])-1)
	error.append(float(x[3*i+2]))


def mat_par(t,f,grado):
	m=[]
	for i in range(len(t)):
		tmp=[]
		for j in range(grado+1):
			tmp.append(t[i]**j)
		if t[i]<0.4:
			tmp.append(0)
		if t[i]>=0.4 and t[i] <=0.7:
			tmp.append(-1)
		if t[i]>0.7:
			tmp.append(0)
		#An_adiendo los valores para delta	
		m.append(tmp)	
	m1=np.matrix(m)
	#calculando (mT m)-1 mT
	m1=np.dot(  np.linalg.inv ( np.dot( np.matrix.transpose(m1),m1)), np.matrix.transpose(m1))
	ff=np.array(f)
	te=np.dot(m1,ff)
	tmp=te.tolist()
	te=[]
	for i in tmp[0]:
		te.append(i)
	return te
AIC,BIC=[],[]
for k in range(1,14):
	te=mat_par(t,f,k)
	print len(te)
	y2=[]
	for i in range(len(t)):
		tmp=0
		for j in range(k+1):
			tmp+=(te[j]*t[i]**j)
		if t[i]>=0.4 and t[i] <=0.7:
			tmp+=-(1.0*te[k+1])
		y2.append(tmp)
	chi2=0
	for i in range(len(t)):
		chi2+=((f[i]-y2[i])/error[i])**2
	loglaiclijud=300*log(1.0/(sqrt(2*pi)*error[0]))-0.5*chi2
	print loglaiclijud
	aic=-2*loglaiclijud+2.0*(k+1)+(2.0*(k+1)*(k+2))/(300-k-2)
	bic=-2*loglaiclijud+(k+1)*log(300)
	AIC.append(aic)
	BIC.append(bic)
k=[1,2,3,4,5,6,7,8,9,10,11,12,13]
plt.plot(k,AIC,'-ro',label="AIC")
plt.plot(k,BIC,'-bo',label="BIC")
plt.legend()
plt.show()
	
