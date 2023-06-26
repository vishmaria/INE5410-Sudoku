# checa se os argumentos são validos
def checkArgs(n_args, n_process, n_threads, n_sol):
    if (n_args != 4):  # checa número de argumento inseridos
        print("Entrada deve ser:$ python3 sudoku.py <arquivo soluções> <número processos trabalhadores> <número threads por processo trabalhador>")
        print("Entrada de argumentos fora do padrão")
        return False
    if (n_process <= 0):  # checa número de processos
        print("Entrada deve ser:$ python3 sudoku.py <arquivo soluções> <número processos trabalhadores> <número threads por processo trabalhador>")
        print("Número de processos trabalhadores deve ser positivo")
        return False
    if (n_process > n_sol):  # checa número de processos
        print("Entrada deve ser:$ python3 sudoku.py <arquivo soluções> <número processos trabalhadores> <número threads por processo trabalhador>")
        print("Número de processos trabalhadores deve ser menor ou igual ao número de soluções a serem testadas")
        return False
    if (n_threads <= 0):  # checa número de threads
        print("Entrada deve ser:$ python3 sudoku.py <arquivo soluções> <número processos trabalhadores> <número threads por processo trabalhador>")
        print("Número de threads por processo trabalhador deve ser positivo")
        return False
    if (n_threads > 9):  # checa número de threads
        print("Entrada deve ser:$ python3 sudoku.py <arquivo soluções> <número processos trabalhadores> <número threads por processo trabalhador>")
        print("Número de threads por processo trabalhador deve ser menor ou igual a 9")
        return False
    return True

# retorna uma lista com cada solução em forma de linhas, colunas e regiões
def getSolutions(arq):
    # lê o arquivo de entrada e extrai as soluções em linhas
    sdk_lin = []
    sdk = []
    arq_r = open(arq, 'r')
    for l in arq_r:
        if (not(l[0].isdigit())):
            sdk_lin.append(sdk)
            sdk = []
            continue
        else:
            sdk.append(l.rstrip())
    sdk_lin.append(sdk)
    arq_r.close()

    # tranforma as colunas das soluções em linhas
    sdk = []
    sdk_col = []
    for solution in sdk_lin:
        for l in range(9):
            coluna = ""
            for c in range(9):
                coluna += solution[c][l]
            sdk.append(coluna)
        sdk_col.append(sdk)
        sdk = []

    # transforma as regiões das soluções em linhas
    sdk_reg = []    
    for solution in sdk_lin:
        for l in range(3):
            for c in range(3):
                reg = ""
                for i in range(3):
                    for j in range(3):
                        reg += solution[i+l*3][j+c*3]
                sdk.append(reg)
        sdk_reg.append(sdk)
        sdk = []

    # armazena todas soluções em uma única lista[[L1, C1, R1], [L2, C2, R2]],
    # onde cada elemento é uma lista(matriz) que organiza as linhas do tipo de solução
    solutions = []
    for ind in range(len(sdk_lin)):
        temp = []
        temp.append(sdk_lin[ind])
        temp.append(sdk_col[ind])
        temp.append(sdk_reg[ind])
        solutions.append(temp)

    return solutions