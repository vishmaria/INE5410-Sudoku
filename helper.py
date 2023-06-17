import more_itertools
from helper import *
from multiprocessing import Process
from threading import Thread
import time

# Funcao executada pelas Threads;
def threadSolver(game, lineList, id):
    for key in game:
        for item in lineList:
            if(len(set(game[key][item])) != 9):
                errorList[id].append(str(key)+str(item+1))
    return errorList

# Processa a matriz e cria um dicionario com as informacoes necessarias para validacao
def matrixProcessing(matrix):
    puzzleLines = [matrix[i:i+9] for i in range(0, len(matrix), 9)] # Lista com o quebra cabeca dividido em linhas

    aux = list(zip(*puzzleLines)) # gera uma lista de tuplas com a matriz transposta de puzzleLines
    puzzleColumns = [list(item) for item in aux] # Lista com o quebra cabeca dividido em colunas

    puzzleRegions = [] # Lista com o quebra cabeca dividido em regioes
    # Parte feita com auxilio do chatGPT--- MUDAR!!!
    for i in range(3):
        for j in range(3):
            region = [puzzleLines[row][col] for row in range(i * 3, (i + 1) * 3) for col in range(j * 3, (j + 1) * 3)]
            puzzleRegions.append(region)
    # Fim chatGPT---

    # Cria dicionario com as tres matrizes
    listaGame = [puzzleLines, puzzleColumns, puzzleRegions]
    listaI = ['L', 'C', 'R'] # Lista dos indices
    gameDict = dict(zip(listaI, listaGame))
    return gameDict

# Funcao geral executada pelos processos;
def checkResult(game, gameI, pid, n_threads):
    for key in gameI:

        # Print do processo
        print('Processo %i: resolvendo quebra-cabeças %i' %(pid, key))
        gameDict = matrixProcessing(game[key])

        # Divisao das linhas entre threads
        listaI = [*range(9)] # Lista dos indices
        print(gameDict)
        threadLines = more_itertools.distribute(n_threads, listaI)

        #Craicao das threads e diconario global de erros
        threadList = []
        global errorList 
        errorList = {k+1: [] for k in range(n_threads)}

        # Inicializacao das threads
        for i in range(n_threads):
            threadList.append(Thread(target=threadSolver, args =(gameDict, threadLines[i], (i+1))))
            threadList[i].start()
        for i in range(n_threads):
            threadList[i].join()

        print(errorList)
        #print(errors)

