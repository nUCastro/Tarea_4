from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma , gammainc
#P 2 a)

def mat_par(t,f,grado):
	m=[]
	for i in range(len(t)):
		tmp=[]
		#El numero marca los grados del polinomio
		for j in range(grado+1):
			tmp.append(t[i]**j)
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

ls=[-0.0011300635323,
0.0122032308022,
-0.045056351572,
0.0742247709579,
-0.0563510163544,
0.0162396949521]
f=open("datos.dat","r")
f.readline()
asd=[]
tmp=(f.read()).split()
#Esto para tener los valores de tiempo 

for i in range(len(tmp)/3):
	asd.append(float(tmp[3*i]))
f.close()	
grado=5
#Funcion creadora de set de datos
def pol(ls,asd):
	set1=[]
	for i in range(len(asd)):
		temp=0
		for j in range(len(ls)):
			temp+=(asd[i]**j*ls[j])
		temp+=np.random.normal(0,30e-6)+1
		set1.append(temp)
	return set1
error=30e-6
chidos=[]
nu=len(asd)-1-grado	
for i in range(10000):
	if i%100==0:
		print i
	set1=pol(ls,asd)
	te=mat_par(asd,set1,grado)
	chi2,y2=0,[]
	for i in range(len(asd)):
		tmp=0
		for j in range(grado+1):
			tmp+=(te[j]*asd[i]**j)
		y2.append(tmp)
	#plt.plot(asd,set1,'ro')
	#plt.plot(asd,y2,'-b')
	#plt.show()	
	for i in range(len(set1)):
		chi2+=((set1[i]-y2[i])/error)**2
	intchi2=1-gammainc(nu/2.0,chi2/2)
	chidos.append(intchi2)

(n,bins,nose)=plt.hist(chidos,bins=90)
plt.xlim(-0.1,1.1)
plt.show()
