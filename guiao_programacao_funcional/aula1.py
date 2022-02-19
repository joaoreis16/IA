#Exercicio 1.1
def comprimento(lista):
	
	if len(lista) == 0:
		return 0

	count = comprimento(lista[1:])

	return count + 1


#Exercicio 1.2
def soma(lista):
	
	if len(lista) == 0:
		return 0
	
	sum = soma(lista[1:])

	return sum + lista[0]

#Exercicio 1.3
def existe(lista, elem):

	if not lista:
		return False

	elif lista[0] == elem:
		return True

	return existe(lista[1:], elem)

#Exercicio 1.4
def concat(l1, l2):
	
	if not l1:
		return l2

	if not l2:
		return l1

	l1.append( l2[0] )
	concat(l1, l2[1:])
	return l1


#Exercicio 1.5
def inverte(lista):

	if len(lista) == 0:
		return []

	lst = inverte(lista[1:])
	lst.append(lista[0])

	return lst


#Exercicio 1.6
def capicua(lista):

	if not lista:
		return True

	elif lista[0] != lista[-1]:
		return False

	return capicua(lista[1:-1])


#Exercicio 1.7
def explode(lista):
	
	if len(lista) == 1:
		return lista[0]

	lst = explode(lista[1:])

	lst = lista[0] + lst
	return lst

#Exercicio 1.8
def substitui(lista, original, novo):

	if not lista:
		return []

	previous = substitui(lista[1:], original, novo)
	if lista[0] == original:
		return [novo] + previous
	
	return [lista[0]] + previous

#Exercicio 1.9
def junta_ordenado(lista1, lista2):

	if lista1 == []:
		return lista2

	if lista2 == []:
		return  lista1

	if lista1[0] < lista2[0]:
		print(junta_ordenado(lista1[1:], lista2))
		return [lista1[0]] + junta_ordenado(lista1[1:], lista2)

	return [lista2[0]] + junta_ordenado(lista1, lista2[1:])

#Exercicio 2.1
def separar(lista):
	if not lista:
		return [],[]

	lista1, lista2 = separar(lista[1:])
	print(lista1)
	print(lista2)

	return ( [lista[0][0]] + lista1, [lista[0][1]] + lista2)



#Exercicio 2.2
def remove_e_conta(lista, elem):

	if len(lista) == 0:
		return ([],0)

	lst, count = remove_e_conta(lista[1:], elem)

	if lista[0] == elem:
		return (lst, count+1)

	else:
		lst = [lista[0]] + lst
		return (lst, count)


#Exercicio 3.1
def cabeca(lista):
	pass

#Exercicio 3.2
def cauda(lista):
	pass

#Exercicio 3.3
def juntar(l1, l2):
	if len(l1) != len(l2):
		return None

	if not l1: return []

	lista = juntar(l1[1:], l2[1:])
	print(lista)
	
	return [(l1[0], l2[0])] + lista

    

#Exercicio 3.4
def menor(lista):

	if not lista:
		return None

	num = menor(lista[1:])

	if num == None: 
		return lista[0]

	elif lista[0] < num :
		return lista[0]
		
	else:
		return num

#Exercicio 3.6
def max_min(lista):
	pass
