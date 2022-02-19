import math

#Exercicio 4.1
impar = lambda x: x % 2 != 0

#Exercicio 4.2
positivo = lambda x: x > 0

#Exercicio 4.3
comparar_modulo = lambda x,y: abs(x) < abs(y)

#Exercicio 4.4
cart2pol = lambda x,y: (math.sqrt(math.pow(x, 2) + math.pow(y,2)), math.atan2(y,x))

#Exercicio 4.5
ex5 = lambda f,g,h: (lambda x,y,z: h(f(x,y), g(y,z))) # a função h tem que ser a última porque é uma condição (ver testes)

#Exercicio 4.6
def quantificador_universal(lista, f):

    if len(lista) == 1 & f(lista[0]):
        return True

    elif f(lista[0]):
        return quantificador_universal(lista[-1:], f)
    
    return False

#Exercicio 4.9
def ordem(lista, f):

    if len(lista) == 1:
        return lista[0]

    if f(lista[0],lista[1]):
        lista.pop(1)
        return ordem(lista, f)

    else:
        lista.pop(0)
        return ordem(lista, f)


#Exercicio 4.10
def filtrar_ordem(lista, f):

    if len(lista) == 1:
        return (lista[0], [])

    num, lst = filtrar_ordem(lista[1:], f)

    if f(lista[0], num):
        # lst.append(num)  ==> Não pode ser assim porque vai adicionar os elementos da lista ao contrário, por exemplo, dada a lista [1,-1,4,0], o resultado seria (-1, [4, 0, 1]) em vez de (-1, [1, 4, 0])
        num_menor = lista[0]
        lista.remove(lista[0])
        return (num_menor, lista)

    else:
        lista.remove(num)
        return (num, lista)


#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    
    if len(lista) == 1:
        return lista

    lst = ordenar_seleccao(lista[1:], ordem)

    if ordem(lista[0],lst[0]):
        lst = [lista[0]] + lst
        return lst

    else:
        pass
    

    
