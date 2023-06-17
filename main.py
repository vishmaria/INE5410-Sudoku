# Trabalho 2 INE-5410 

from helper import *

puzzleList = [] # Lista com os quebra cabecas

# Abre o arquivo e divide os cenarios:
with open("sudoku_boards.txt", "r") as f:
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


checkResult(puzzleDict)