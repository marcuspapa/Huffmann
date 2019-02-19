#!/usr/bin/env python

import sys
import heapq
import operator

verbose = False
codigos = {}
mapaSimboloCodigo = {}
freq = {}

# Classe dos nodos da arvore de Huffman
class nodoHeapq:

        #Construtor
	def __init__(self, simbolo, probabilidade):
		self.probabilidade = probabilidade    # probabilidade desse nodo
		self.simbolo = simbolo                # simbolo associado a esse nodo
		self.esq = None                       # nodo a esquerda desse na arvore
		self.dir = None                       # nodo a direita desse na arvore

        # Comparacao entre objetos: para manter o heapq ordenado probabilidades menor pro maior e juntar nodos adequadamente
	def __cmp__(self, outro):
		return self.probabilidade > outro.probabilidade

# Conta a frequencia de cada simbolo no arquivo e as ordena 
def probabilidadeSimbolos(simb):

    # Varre o iteravel e conta as aparicoes de cada simbolo
    for x in xrange (0, len(simb)):
        if not simb[x] in freq:
            freq[simb[x]] = 0
        freq[simb[x]] += 1

    # Converte contagem em probabilidade (divide pelo total)
    for x in freq:
        freq[x] /= len(simb)*1.0 # Multiplica por 1.0 para fazer cast para float
    
    # Ordena: menor probabilidade para maior probabilidade
    sortedProb = sorted(freq.items(), key = operator.itemgetter(1))
    
    if verbose:
        print("\nProbabilidades dos bytes (ordem crescente):")
        print(sortedProb)
        print("\n")
    return sortedProb

# Funcao recursiva que percorre toda arvore de Huffman atribuindo codigos aos nodos
def codificaSimbolos(nodo, codigo):
    
    if(nodo.simbolo != None):
        codigos[nodo.simbolo] = codigo
	mapaSimboloCodigo[nodo.simbolo] = codigo
	return

    # Vai recursivamente para os proximos nodos da arvore com a convencao:
    # esquerda = adiciona 0 no codigo
    # direita = adiciona 1 no codigo
    codificaSimbolos(nodo.dir, codigo + "0")
    codificaSimbolos(nodo.esq, codigo + "1")   

# Acao: Compressao de arquivo ########################################################################
def compress():
    
    # Controle para abertura do arquivo a ser (des)compactado (rb = read binary)
    # Ainda, le conteudo do arquivo, armazenando cada 1 byte (8 bits), e o fecha
    simbolos = []
    try:
        with open(sys.argv[2], 'rb') as fl:
            while True:
                byte = fl.read(1)
                simbolos.append(byte)
                if not byte:        # No fim do arquivo, sai do loop while
                    break
    except IOError:
        print ("ERRO! Arquivo nao encontrado. Forneca caminho absoluto ou tenha o arquivo"+\
              " no diretorio atual")
        sys.exit()

    probabilidades = probabilidadeSimbolos(simbolos)
    heap = []

    # Cria nodos da arvore e adiciona seus valores
    for valor in probabilidades:

        # value[0] = simbolo; value[1] = probabilidade. Cria esse nodo e adiciona no heapq
        nodo = nodoHeapq(valor[0], valor[1])
        heapq.heappush(heap, nodo)

    # Junta dois nodos de menor probabilidade enquanto houver mais de um nodo
    while (len(heap)>1):
        nodoA = heapq.heappop(heap)
        nodoB = heapq.heappop(heap)
        fusaoAB = nodoHeapq(None, nodoA.probabilidade + nodoB.probabilidade) # Novo nodo com Prob = soma das prob dos nodos anteriores
        fusaoAB.dir = nodoA
        fusaoAB.esq = nodoB
        heapq.heappush(heap, fusaoAB)   # adiciona nodo novo no heapq, ordenado corretamente quanto a probabilidade

    # Com a arvore de nodos feita, deve-se atribuir a codificacao de cada nodo de simbolo:
    raiz = heapq.heappop(heap)      # Analise da arvore comeca pela raiz
    codificacao = ""

    # chama funcao que gera codificacao para os simbolos de acordo com a arvore criada
    codificaSimbolos(raiz, codificacao)

    # Se execucao verbosa, fornece mais informacoes
    if verbose:
        print ("Codificacao para cada simbolo:")
        print(mapaSimboloCodigo)

        # Calculo do tamanho medio de palavras
        tamanhoMedio = 0
        for simb in mapaSimboloCodigo:
            tamanhoMedio += len(mapaSimboloCodigo[simb]) * freq[simb]
        print ("\nTamanho medio das palavras de codigo: " + str(tamanhoMedio))
    
    arquivoSaida = sys.argv[2].split(".")[0] + ".arq"
    arqEscrever = open(arquivoSaida, "wb")

    # Tendo as palavras de codigo para cada simbolo, deve-se escrever no arquivo de saida
    byteCodigos = bytearray()
    for caracter in simbolos:
        
        #codigosConcatenados += mapaSimboloCodigo[caracter]
        faltaPra8 = 8 - len(mapaSimboloCodigo[caracter]) % 8
        byteCodigo = mapaSimboloCodigo[caracter]

        for x in range (faltaPra8):
            byteCodigo += "0"
        #print byteCodigo
        byteCodigos.append(int(byteCodigo, 2))

    arqEscrever.write(bytes(byteCodigos))
                        
    





    
    

    
# Acao: decompressao ########################################################################
def decompress():
    print "a fazer"

#############################################################################################

# Tres (e um quarto opcional) argumentos devem ser passados por linha de comando:
# o arquivo .py; a acao (compactar ou descompactar); o arquivo a sofrer a acao; quarto argumento para definir execucao verbosa
if (len(sys.argv) != 3) and (len(sys.argv) != 4):
    print ("ERRO! Uso apropriado: \"Huffman.py -c <arquivo>\" para compactar ou" +\
    "\n\"Huffman.py -d <arquivo>\" para descompactar. Use --verbose para mais informacao da execucao")
    sys.exit()

# Configura para execucao verbose ou nao
if (len(sys.argv) == 4):
    if(sys.argv[3] == "--verbose"):
        verbose = True
    else:
        print("ERRO! Unico quarto parametro possivel e \"--verbose\"")
        sys.exit()

# Le a acao a ser feita (compactar ou descompactar)
if (sys.argv[1] == "-c"):
    compress()
elif (sys.argv[1] == "-d"):
    decompress()
else:
    print ("ERRO! Acoes possiveis: \"-c\" para compactar ou"+\
          "\n\"-d\" para descompactar")
sys.exit()
