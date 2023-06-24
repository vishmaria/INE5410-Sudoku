# Trabalho 2 INE-5410 
from sys import argv
from helper import *
from multiprocessing import Process
from threading import Thread
import time


def inputs(argv):
    file = argv[1]
    if not file:
        print("O arquivo não existe")
        return
    n_process = int(argv[2])
    n_threads = int(argv[3])
    if n_process < 1 or n_threads < 1:
        print("Really?")
        return
    return file, n_process, n_threads
def main():

    file, n_process, n_threads = inputs(argv)

    processList = []

    start_time = time.time()

    puzzleList = list()  # Lista com os quebra cabecas
    # Abre o arquivo e divide os cenarios:
    with open(file, 'r') as f:
        contents = f.readlines()
        puzzleList = contents.split('\n\n')

    # Remove quebra de linha dos cenarios:
    for i in range(len(puzzleList)):
        puzzleList = [i for i in puzzleList if i != '\n']

    # Cria dicionario com cenarios:
    listaI = [*range(1, (len(puzzleList)) + 1)]  # Lista dos indices
    puzzleDict = dict(zip(listaI, puzzleList))

    # Divide os jogos entre os processos.
    # Abordagem parecida com o T1, tratando casos de mais processos que jogos e vice-versa
    # fazendo a divisão inteira de células no tabuleiro.
    # TODO: Falta otimizar para que nao precise ser passado o dicionario completo de jogos para cada thread
    if n_process > len(puzzleDict):
        n_process = len(puzzleDict)
    if n_threads > len(puzzleDict):
        n_threads = len(puzzleDict)

    r = len(puzzleDict) % n_process
    n_puzzles = len(puzzleDict) // n_process

    # TODO: verificar função chuncked do more_itertools.
    gameIds = list()

    # Criacao dos processos
    begin = 0
    if __name__ == '__main__':  # caso for o programa principal
        for i in range(n_process):
            processName = i + 1
            end = begin + n_puzzles
            if r > 0:
                end += 1
                r -= 1
            process = Process(target=checkResult, args=(puzzleDict, gameIds[i], processName, n_threads),
                              name=str(i + 1))
            processList.append(process)
            begin = end

        for process in processList:
            process.start()

        for process in processList:
            process.join()

        print("--- %s seconds ---" % (time.time() - start_time))
