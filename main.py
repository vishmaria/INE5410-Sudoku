# Trabalho 2 INE-5410 
import more_itertools
from helper import *
from multiprocessing import Process
from threading import Thread
import time

print('Start')
start_time = time.time()

n_process = 16 # Num de processos NAO pode ser maior que num de Jogos
n_threads = 1
processList = []

puzzleList = [] # Lista com os quebra cabecas
# Abre o arquivo e divide os cenarios:
with open("5M.txt", "r") as f:
    contents = f.read()
    puzzleList = contents.split('\n\n')

# Remove quebra de linha dos cenarios:
for i in range(len(puzzleList)):
    item = puzzleList[i].replace('\n', '')
    item = [*item]
    puzzleList[i] = item

# Divide os jogos entre os processos
listaI = [*range(1, (len(puzzleList))+ 1)] # Lista dos indices
gameIds = more_itertools.divide(n_process, listaI)
games = []

# Cria dicionario com cenarios:
for item in gameIds:
    listId = list(item) # Necessario devido a biblioteca more itertools
    beg, end = listId[0]-1, listId[-1]
    puzzleDict = dict(zip(listId, puzzleList[beg:end]))
    games.append(puzzleDict)

gameIds = more_itertools.divide(n_process, listaI) # Por alguma razao o codigo nao funciona com gameIds antigo

print("Fim parte sequencial\n--- %s seconds ---" % (time.time() - start_time))
# Criacao dos processos
if __name__ == '__main__': # caso for o programa principal
    for i in range(n_process):
        processName = i+1
        process = Process(target=checkResult, args=(games[i], gameIds[i], processName, n_threads), name = str(i+1))
        processList.append(process)
        process.start()

    for process in processList:
        process.join()

    print("Tempo total:\n--- %s seconds ---" % (time.time() - start_time))
