from os import system
from sys import platform


# ESTA FUNçAO SIMPLIFICA UMA DIVISAO
def simplificar(num,denom,fir=2):
	if num % denom==0:
		return [num / denom,1]
	if num%fir == 0 and denom%fir==0:
		return simplificar(num/fir,denom/fir,fir+1)
	if fir==20:
		return [num,denom]
	return simplificar(num, denom, fir + 1)


# ESTA FUNçAO CRIA UM ROL COM OS DADOS NA STRING ACIMA
def get_rol(lista):
	lista = lista.strip().split(" ")
	for i in range(len(lista)):
		lista[i]= int(lista[i])
	rol = sorted(lista)
	return rol # lista ordenada dos elementos


# ESTA FUNçAO CRIA UM DICIONARIO COM UM ELEMENTO E A SUA RESPETIVA FREQUENCIA
def get_frequency(rol):
	dict = {}  # vai ser um dicionario que mostra a frequencia de cada elemento
	ind = 0
	for r in rol:
		if r in dict:
			dict[r] += 1
		else:
			dict[r] = 1
		ind += 1
	return dict


# ESTA FUNçAO RETORNA OS INTERVALOS DA TABELA SENDO DADOS O DICIONARIO DAS FREQUENCIAS E A LARGURA DOS INTERVALOS
def get_intervalos(dict, largura, maxm):
	rangef, rangei,interv = 0, 0,[]
	for d in dict:
		if rangef==0 and rangei==0:
			rangei,rangef=d,d+largura
		if rangef>= maxm:
			interv.append([rangei, rangef])
			break
		interv.append([rangei,rangef])
		rangei, rangef = rangef, rangef+largura
	return interv

#retorna uma lista onde cada elemento representa uma linha da tabela, e ovalor é de a frequencia total dos elementos que pertencem a essa linha
def frequencia_absoluta(interv,dict,ultimo):
	fr_tot=0
	linhas=[]
	for i in interv:
		atual=i[0]
		if i[-1]==ultimo:
			while atual<=i[1]:
				if atual in dict:
					fr_tot+=dict[atual]
				atual+=1
			linhas.append(fr_tot)
			fr_tot=0
		else:
			while atual<i[1]:
				if atual in dict:
					fr_tot+=dict[atual]
				atual+=1
			linhas.append(fr_tot)
			fr_tot=0
	return linhas

#ESTA FUNçAO RETORNA uma lista onde cada elemento representa uma linha da tabela, e ovalor é de a frequencia RELATIVA DESTA LINHA
def frequencia_relativa(fr_abs,num_elem):
	linhas=[]
	for f in fr_abs:
		linhas.append(simplificar(f,num_elem))
	return linhas

def frequencia_relativa_percentual(fr_rel):
	linhas=[]
	for f in fr_rel:
		linhas.append((f[0]/f[1]*100)*1000//1/1000)
	return linhas

def frequencia_acumulada(fr_abs):
	acum,linhas=0,[]
	for f in fr_abs:
		acum+=f
		linhas.append(acum)
	return linhas

def frequencia_acumulada_percentual(fr_acum):
	num_elem,linhas=fr_acum[-1],[]
	for f in fr_acum:
		linhas.append((f*100/num_elem)*1000//1/1000)
	return linhas

def mudar_formato1(frel):
	linhas=[]
	for f in frel:
		linhas.append(str(int(f[0]))+"/"+str(int(f[1])))
	return linhas

def mudar_formato2(cla):
	linhas=[]
	for c in cla:
		linhas.append(str(int(c[0]))+"|-"+str(int(c[1])))
	return linhas

def mostrar_tabela(colunas):
	linhas=[]
	numeros=[7,14,14,22,17,21]
	colunas[2]=mudar_formato1(colunas[2])
	colunas[0]=mudar_formato2(colunas[0])
	linha= "| "
	i=0
	while i<=len(colunas[0])-1:
		for c in colunas:
			espacamento=(numeros[colunas.index(c)]-len(str(c[i])))//2
			linha+= " "*espacamento+str(c[i])+" "*espacamento+"  |"
		linhas.append(linha)
		linha= "| "
		i+=1
	print(" Classe      | Freq. Absoluta | Freq. Relativa| Freq. Rel. Percentual| Freq. Acumulativa| Freq. Acum. Percentual|")
	for line in linhas:
		print("------------------------------------------------------------------------------------------------------------------")
		print(line)
def calcular_num_classes(rol):
	n=len(rol)
	k=n**(1/2)
	if type(k)==float:
		k=int(k//1+1)
	return k

def get_moda(fre_abs):
	maior=0
	index=0
	for f in fre_abs:
		if f >maior:
			maior=f
			index=fre_abs.index(f)
	return index

def get_mediana(rol):
	if len(rol)%2==0:
		return rol[int(len(rol)/2)]
	else:
		return [rol[int(len(rol)//2)-1],rol[int(len(rol)/2)]+1]

def get_desvio_padrao(media,rol,tamanho):
    atual=[]
    for r in rol:
        atual.append((r-media)**2)
    print(atual)
    valor=sum(atual)/tamanho
    return valor**(1/2)

lista=input("cole aqui a string que contem os valores: \n")
escolha=input("deseja especificar o tamanho das classes? (y/n): ")
rol = get_rol(lista)
amplitude_total=rol[-1]-rol[0]
num_classes=calcular_num_classes(rol)
if escolha =="y":
	amplitude_classe=int(input("Insira o valor dos intervalos das classes:"))
else:
	amplitude_classe= amplitude_total/num_classes
	if amplitude_classe//1 != amplitude_classe:
		amplitude_classe= int(amplitude_classe//1+1)

#print(f"maximo: {max(rol)}; minimo: {min(rol)}") #MOSTRAR O MAXIMO E O MINIMO DA LISTA
#NESTA PARTE PODEM SER FEITAS AS OPERAçOES QUE SE DESEJAM REALIZAR COM OS DADOS DO ENUNCIADO

if platform == "linux" or platform == "linux2":
	system("clear")
elif platform == "win32":
	system("cls")
tamanho=len(rol)
freq = get_frequency(rol)
intervalos=get_intervalos(freq,amplitude_classe,max(rol))
fr_abs=frequencia_absoluta(intervalos,freq,rol[-1])
fr_rel=frequencia_relativa(fr_abs,len(rol))
fr_rel_perc=frequencia_relativa_percentual(fr_rel)
fr_acum=frequencia_acumulada(fr_abs)
fr_acum_perc=frequencia_acumulada_percentual(fr_acum)
media=(sum(rol)/len(rol))*10000//1/10000
moda=intervalos[get_moda(fr_abs)]
mediana=get_mediana(rol)
desvio_padrao= get_desvio_padrao(media,rol,tamanho)
varianca=desvio_padrao**2
if escolha=="y":
	num_classes=len(fr_abs)

print(f" Rol dos dados: {rol};")
print(f" Amplitude total (R): {amplitude_total};")
print(f" Amplitude das classes (h): {int(amplitude_classe)};")
print(f" Tamanho da amostra (n): {tamanho};")
print(f" Numero de classes (K): {num_classes};")
print(f" Media aritmetica: {media};")
print(f" Moda (Mo): {moda};")
print(f" Mediana : {mediana};")
print(f" varianca : {varianca};")
print(f" Desvio Padrao : {desvio_padrao};\n")

mostrar_tabela([intervalos,fr_abs,fr_rel,fr_rel_perc,fr_acum,fr_acum_perc])
