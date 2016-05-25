import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy.special import gammainc
nu=293.0
f=open("coef2","r")

ls=[-0.0011300635323,
0.0122032308022,
-0.045056351572,
0.0742247709579,
-0.0563510163544,
0.0162396949521,
0.000101000997816]

f=open("datos.dat","r")
f.readline()
asd=[]
tmp=(f.read()).split()
#Esto para tener los valores de tiempo fijos
for i in range(len(tmp)/3):
	asd.append(float(tmp[3*i]))
f.close()
#asd tiene los tiempos
def mkset(asd,ls):
	set1=[]
	for i in range(len(asd)):
		temp=0
		for j in range(len(ls)-1):
			temp+=((asd[i]**j)*ls[j])
		if asd[i]>=0.4 and asd[i]<=0.7:
			#Resto el delta
			temp-=ls[len(ls)-1]
		temp+=np.random.normal(0,30e-6)
		set1.append(temp)
	#plt.plot(asd,set1,'ro')
	#plt.show()
	return set1
error=3e-5
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
grado=5
chidos=[]
for i in range(10000):
	if i%100==0:
		print i
	set1=mkset(asd,ls)
	te=mat_par(asd,set1,grado)
	chi2,y2=0,[]
	for i in range(len(asd)):
		tmp=0
		for j in range(grado+1):
			tmp+=(te[j]*asd[i]**j)
		if asd[i]>=0.4 and asd[i]<=0.7:
			#Sumo el delta
			tmp-=ls[len(ls)-1]
		y2.append(tmp)
	#Daban cosas raras, por eso hay plots
	#plt.plot(asd,set1,'ro')
	#plt.plot(asd,y2,'-b')
	#plt.show()	
	for i in range(len(set1)):
		chi2+=((set1[i]-y2[i])/error)**2
	intchi2=1-gammainc(nu/2.0,chi2/2)
	chidos.append(intchi2)
plt.hist(chidos,bins=50)
plt.show()
