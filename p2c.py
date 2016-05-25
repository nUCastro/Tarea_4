from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma , gammainc

grado=2

f=open("datos.dat","r")
x=f.readline()
x=f.read()
f.close()
x=x.split()
asd=[]
for i in range(len(x)/3):
	asd.append(float(x[3*i]))

coef=[-0.0011300635323,
0.0122032308022,
-0.045056351572,
0.0742247709579,
-0.0563510163544,
0.0162396949521]



def pol(ls,asd):
	set1=[]
	for i in range(len(asd)):
		temp=0
		for j in range(len(ls)):
			temp+=(asd[i]**j*ls[j])
		temp+=np.random.normal(0,30e-6)
		set1.append(temp)
	return set1
	
def mat_par(t,f,grado):
	m=[]
	for i in range(len(t)):
		tmp=[]
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
#------------- fin del calculo de los coeficientes
chidos=[]
for o in range(3000):
	if o%100==0:
		print o
	set1=pol(coef,asd)
	te=mat_par(asd,set1,grado)
	y2=[]
	# Valor esperado para cada tiempo
	for i in range(len(asd)):
		tmp=0
		for j in range(grado+1):
			tmp+=(te[j]*(asd[i]**j))
		y2.append(tmp)
	plt.plot(asd,set1,'ro')
	plt.plot(asd,y2,'-b')
	plt.show()	
	#Test chi cuadrado
	chi2=0
	for i in range(len(asd)):
		chi2+=((set1[i]-y2[i])/30e-6)**2
	#Se supone que tenemos 300 datos, y ajustamos 6 parametros
	#Por lo tanto, el chi2 es con nu=294
	nu=294.0
	#print chi2, 'chi square'
	#Scypi calcula gammainc como la CDF de chisquare
	intchi2=1-gammainc(nu/2.0,chi2/2)
	chidos.append(intchi2)
plt.hist(chidos,bins=50,color='white')
plt.show()	
