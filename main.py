# Trabalho 2 INE-5410 
import more_itertools
from helper import *
from multiprocessing import Process
from threading import Thread
import time

start_time = time.time()

n_process = 1
n_threads = 1
processList = []

puzzleList = [] # Lista com os quebra cabecas
# Abre o arquivo e divide os cenarios:
with open("input-sample.txt", "r") as f:
    contents = f.read()
    puzzleList = contents.split('\n\n')

# Remove quebra de linha dos cenarios:
for i in range(len(puzzleList)):
    item = puzzleList[i].replace('\n', '')
    item = [*item]
    puzzleList[i] = item

# Cria dicionario com cenarios:
listaI = [*range(1, (len(puzzleList))+ 1)] # Lista dos indices
puzzleDict = dict(zip(listaI, puzzleList))

# Divide os jogos entre os processos// Falta otimizar para que nao precise ser passado o diconario completo de jogos para cada thread
gameIds = more_itertools.distribute(n_process, listaI)

# Criacao dos processos
if __name__ == '__main__': # caso for o programa principal
    for i in range(n_process):
        processName = i+1
        process = Process(target=checkResult, args=(puzzleDict, gameIds[i], processName, n_threads), name = str(i+1))
        processList.append(process)
        process.start()

    for process in processList:
        process.join()

    print("--- %s seconds ---" % (time.time() - start_time))
#checkResult()