#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea los conectivos
conectivos = ['Y', 'O', '>', '=']
# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def String2Tree(A):
	# Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
	# Input: - A, lista de caracteres con una formula escrita en notacion polaca inversa
	#        - letrasProposicionales, lista de letras proposicionales
	#        - conectivos, lista de conectivos
	# Output: formula como tree
	pila = []
	for c in A:
		# print("Examinando " + str(c))
		if c in letrasProposicionales:
			# print(u"El símbolo es letra proposicional")
			pila.append(Tree(c, None, None))
		elif c == '-':
			# print("Negamos")
			formulaAux = Tree(c, None, pila[-1])
			del pila[-1]
			pila.append(formulaAux)
		elif c in conectivos:
			# print("Unimos mediante conectivo")
			formulaAux = Tree(c, pila[-1], pila[-2])
			del pila[-1]
			del pila[-1]
			pila.append(formulaAux)
		else:
			print(u"Hay un problema: el símbolo " + str(c) + " no se reconoce")
	return pila[-1]

def Inorder2Tree(A):
	if len(A) == 1:
		return Tree(A[0], None, None)
	elif A[0] == '-':
		return Tree(A[0], None, Inorder2Tree(A[1:]))
	elif A[0] == "(":
		counter = 0 #Contador de parentesis
		for i in range(1, len(A)):
			if A[i] == "(":
				counter += 1
			elif A[i] == ")":
				counter -=1
			elif (A[i] in ['Y', 'O', '>', '=']) and (counter == 0):
				return Tree(A[i], Inorder2Tree(A[1:i]), Inorder2Tree(A[i + 1:-1]))
	else:
		return -1

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def imprime_listaHojas(L):
	for h in L:
		print(imprime_hoja(h))

def complemento(l):
    if l in letrasProposicionales:
        c = "-" + l
    else:
        c = l[1:]
    return c

    pass
#print(complemento('-q'))

def par_complementario(h):
    for a in h:
        p1 = a
        for i in h:
            if i == p1:
                continue
            p2 = complemento(i)
            if p1 == p2:
                pc = 1
                break
            else:
                pc = 0
        if pc == 1:
            return True
    return False

    pass
#ht = [Tree('-',None,Tree('Z1',None,None)), Tree('S1',None,None), Tree('-',None,Tree('S10',None,None)), Tree('Z10',None,None)]
#h = []
#for a in ht:
#    l = Inorder(a)
#    h.append(l)
#print(h)
#print(par_complementario(h))

def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
        if f.right == None:
            return True
        if f.label == "-":
            return es_literal(f.right)
        else:
            return False
    
xd = Tree('O',Tree('k',None,None),Tree('Y',Tree('i',None,None),Tree('j',None,None)))
print(es_literal(xd))
print(Inorder(xd))

def no_literales(l):
#        if l.right == None:
#            return False
#        if l.label == "-":
#            if l.right == None:
#                return False
#            if l.right == 
#            else: 
#                return False

	pass

def clasificacion(f):
	# clasifica una fórmula como alfa o beta
	# Input: f, una fórmula como árbol
	# Output: string de la clasificación de la formula

	pass

def clasifica_y_extiende(f, h):
	# Extiende listaHojas de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# 		 h, una hoja (lista de fórmulas como árboles)
	# Output: no tiene output, pues modifica la variable global listaHojas

	global listaHojas

	print("Formula:", Inorder(f))
	print("Hoja:", imprime_hoja(h))

	assert(f in h), "La formula no esta en la lista!"

	clase = clasificacion(f)
	print("Clasificada como:", clase)
	assert(clase != None), "Formula incorrecta " + imprime_hoja(h)

	if clase == 'Alfa1':
		aux = [x for x in h if x != f] + [f.right.right]
		listaHojas.remove(h)
		listaHojas.append(aux)
	elif clase == 'Alfa2':
		pass
	# Aqui el resto de casos


def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f

	global listaHojas
	global listaInterpsVerdaderas

	A = String2Tree(f)
	print(u'La fórmula introducida es:\n', Inorder(A))

	listaHojas = [[A]]

	while (len(listaHojas) > 0):
		h = choice(listaHojas)
		print("Trabajando con hoja:\n", imprime_hoja(h))
		x = no_literales(h)
		if x == None:
			if par_complementario(h):
				listaHojas.remove(h)
			else:
				listaInterpsVerdaderas.append(h)
				listaHojas.remove(h)
		else:
			clasifica_y_extiende(x, h)

	return listaInterpsVerdaderas

