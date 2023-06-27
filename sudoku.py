from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from helpers import *
import threading, multiprocessing
import sys, os, time


# função executada por cada processo
def run_proc(ini_proc, fim_proc):

    # lista com as threads
    threads = []
    for sol in range(ini_proc, fim_proc):
        print("Processo {}: resolvendo quebra-cabeças {}".format(multiprocessing.current_process().name[-1:], sol+1))
        
        global total_erros
        global qtd
        
        # cria os dics com a quantidade de erros e os erros que cada thread detectou
        qtd = {}
        total_erros = {}
        for i in range(n_threads):
            total_erros["T"+str(i+1)] = ""
            qtd["T"+str(i+1)] = 0

        # divide as linhas das soluções que cada thread fará e executa as threads
        res_thr = 9 % n_threads
        ini_thr = 0
        for j in range(n_threads):
            fim_thr = ini_thr + (9 // n_threads)

            if (j < res_thr):
                fim_thr += 1

            threads.append(threading.Thread(target=run_thread, name="T"+str(j+1), args=(sol, ini_thr, fim_thr)))
            threads[j].start()
            ini_thr = fim_thr

        # sincroniza as threads
        for j in range(n_threads):
            threads[j].join()

        out = []  # lista usada para fim de formatação da saída
        n_qtd = 0  # quantidade de erros

        # percorre os dicionários, setando o número de erros do jogo, criando uma string das threads com seus erros e pondo na lista
        for key in total_erros:
            n_qtd += qtd[key]
            if (total_erros[key] != ''):
                out.append(key+" :"+str(total_erros[key]))

        # prints formatados
        if (len(out) == 0):
            print("Processo {}: 0 erros encontrados".format(multiprocessing.current_process().name[-1:]))
        else:
            print("Processo {}: {} erros encontrados ({})".format(multiprocessing.current_process().name[-1:], n_qtd, '; '.join(out)))

        threads.clear()


# função executada pelas threads    
def run_thread(sol, ini, fim):
    for i in range(3):  # percorre entre os tipos de jogos(linhas, colunas e regiões) da solução
        for j in range(ini, fim):  # percorre entre as linhas da thread
            for num in range(1, 10):  # percorre entre os número válidos em um sudoku
                if (solutions[sol][i][j].count(str(num)) != 1): # caso possua mais de um número igual, detecta erro e adiciona no dicionario
                    if (i == 0):  # se a thread estiver checando uma linha, retorna(nome_da_thread, L{qual linha esta errada})
                        if (total_erros[threading.current_thread().name] != ''):
                            total_erros[threading.current_thread().name] += ','
                        total_erros[threading.current_thread().name] += " L"+str(j+1)
                        qtd[threading.current_thread().name] += 1
                        break
                    elif (i == 1):  # se a thread estiver checando uma coluna, retorna(nome_da_thread, C{qual coluna esta errada})
                        if (total_erros[threading.current_thread().name] != ''):
                            total_erros[threading.current_thread().name] += ','
                        total_erros[threading.current_thread().name] += " C"+str(j+1)
                        qtd[threading.current_thread().name] += 1
                        break
                    else:  # se a thread estiver checando uma regiao, retorna(nome_da_thread, R{qual regiao esta errada})
                        if (total_erros[threading.current_thread().name] != ''):
                            total_erros[threading.current_thread().name] += ','
                        total_erros[threading.current_thread().name] += " R"+str(j+1)
                        qtd[threading.current_thread().name] += 1
                        break


if __name__ == '__main__':

    n_args = len(sys.argv)  # número de argumentos via terminal
    arq = sys.argv[1]  # arquivo de soluções
    n_process = int(sys.argv[2])  # número de processos
    global n_threads
    n_threads = int(sys.argv[3])  # número de threads

    if not(os.path.isfile(arq)):  # checa se o caminho do arquivo de soluções existe
        print("Entrada deve ser:$ python3 sudoku.py <arquivo soluções> <número processos trabalhadores> <número threads por processo trabalhador>")
        print("Arquivo solução inserido não existe")
        sys.exit()

    global solutions
    solutions = getSolutions(arq)  # retorna as soluções
    n_sol = len(solutions)  # numero de soluções

    if not(checkArgs(n_args, n_process, n_threads, n_sol)):  # checa se os argumentos são válidos
        sys.exit()

    proc = []  # lista com os processos
    res_sol = n_sol%n_process  # resto da divisao do número de soluções por número de processos
    ini_proc = 0

    # cria os processos, dividindo os jogos que cada um testará
    for i in range(n_process):
        fim_proc = ini_proc + n_sol//n_process
        
        if (i < res_sol):
            fim_proc += 1

        proc.append(multiprocessing.Process(target=run_proc, args=(ini_proc, ini_proc+(n_sol // n_process))))
        proc[i].start()
        ini_proc = fim_proc

    # sincroniza os processos
    for i in range(n_process):
        proc[i].join()