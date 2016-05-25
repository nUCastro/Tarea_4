from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma , gammainc


# --------- leyendo el archivo
f=open("datos.dat","r")
x=f.readline()
x=f.read()
f.close()
x=x.split()
t,f,error=[],[],[]
for i in range(len(x)/3):
	t.append(float(x[3*i]))
	#Esto es para ajustar la funcion 1-delta
	f.append(float(x[3*i+1])-1)
	error.append(float(x[3*i+2]))

#---------fin de leer el archivo	


#Proceso de creacion de la matriz M	
#(mt m )-1 mt
def mat_par(t,f):
	m=[]
	for i in range(len(t)):
		tmp=[]
		for j in range(6):
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
#------------- fin del calculo de los coeficientes

te=mat_par(t,f)

#------------- Procedimento de graficar
equis=np.linspace(0.1,0.9,1000)
ygriega=[]
y2=[]
for i in range(len(equis)):
	tmp=0
	for j in range(6):
	
		tmp+=(te[j]*equis[i]**j)
	if equis[i]>=0.4 and equis[i] <=0.7:
		tmp+=-(1.0*te[6])
	
	ygriega.append(tmp)

for i in range(len(t)):
	tmp=0
	for j in range(6):
		tmp+=(te[j]*t[i]**j)
	if t[i]>=0.4 and t[i] <=0.7:
		tmp+=-(1.0*te[6])
	y2.append(tmp)
plt.plot(t,f,'ro',label='Datos')
plt.plot(equis,ygriega,'-b',label=r'$\vecy = \bf{M} \vec{\Theta}$')
plt.title('$ \delta \ \    $')
plt.legend()
for i in range(len(te)-1):
	print 'x'+str(i)+' ='+str(te[i])
print 'delta =' + str(te[6])	
'''
D=open("coef","w")
for i in range(len(te)):
	D.write(str(te[i])+'\n')
D.close()	
'''
print 
print 'Rp/R* = ' + str(sqrt(te[6]))
plt.ylim(min(f)-std(f),max(f)+std(f))
#PLT desactivado.
	

#Test chi cuadrado

chi2=0
for i in range(len(t)):
	chi2+=((f[i]-y2[i])/error[i])**2
#Se supone que tenemos 300 datos, y ajustamos 7 parametros
#Por lo tanto, el chi2 es con nu=293
nu=293.0
print chi2, 'chi square'


#Scypi calcula gammainc como la CDF de chisquare
intchi2=1-gammainc(nu/2.0,chi2/2)
print intchi2 ,'p-value'
lol=raw_input("Presione intro para continuar...")
plt.show()
