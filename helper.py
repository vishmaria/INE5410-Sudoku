
# Funcao executada pelas Threads;
def threadSolver(game):
    errorList = []
    for key in game:
        for i in range(9):
            if(len(set(game[key][i])) != 9):
                errorList.append(str(key)+str(i+1))
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

    listaGame = [puzzleLines, puzzleColumns, puzzleRegions]
    listaI = ['L', 'C', 'R'] # Lista dos indices
    gameDict = dict(zip(listaI, listaGame))
    return gameDict

# Funcao geral executada pelos processos;
def checkResult(game):
    for i in range(len(game)):
        print('Resolvendo jogo', i+1)
        gameDict = matrixProcessing(game[i+1])
        errors = threadSolver(gameDict)
        print(errors)

