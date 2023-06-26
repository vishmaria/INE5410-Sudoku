from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from helpers import *
import threading, multiprocessing
import sys, os, time

# função executada por cada processo
def run_proc(sol):
    print("Processo {}: resolvendo quebra-cabeças {}".format(multiprocessing.current_process().name[-1:], sol+1))
    
    futs = []  # lista que recebe os futures do executor
    global n_threads  # número de threads

    # cria o executor das threads e executa(envia a solução a ser avaliada, o tipo da solução a ser avaliada(linha, coluna ou região) e
    #   qual linha do tipo da solução vai ser avaliada)
    ex_thread = ThreadPoolExecutor(max_workers=n_threads, thread_name_prefix="T")
    for type in range (3):
        for ind in range(9):
            futs.append(ex_thread.submit(run_thread, (sol, type, ind)))
    ex_thread.shutdown()
    
    qtd = 0  # quantidade de erros da solução

    # criado um dicionario com todas as threads como chaves
    total_erros = {}
    for i in range(n_threads):
        total_erros["T"+str(i+1)] = ""

    # percorre os futures do executor
    for res in as_completed(futs):
        # quando retorna None no future, é porque não teve erro na linha, coluna ou regiao avaliada
        if (res.result() != None):  # se teve erro
            # aumenta a quantidade de erros e adiciona o erro no dicionário, de acordo com a thread que detectou o erro
            qtd += 1
            if (total_erros[res.result()[0]] == ''):
                total_erros[res.result()[0]] += res.result()[1]
            else:
                total_erros[res.result()[0]] += ", "+res.result()[1]
    
    if (qtd == 0):  # se não teve erros na solução
        return ("Processo {}: 0 erros encontrados".format(multiprocessing.current_process().name[-1:]))
    else:  # se teve erros, adicionamos a thread e os erros dela ,como uma única string, em uma lista(se a thread detectou erros)
        out = []
        for key in total_erros.keys():  
            if (total_erros[key] != ''):
               out.append(key+": "+total_erros[key])
        
        out_form = '; '.join(out)  # transformamos a lista dos erros em uma string formatada para a saida desejada
        return ("Processo {}: {} erros encontrados ({})".format(multiprocessing.current_process().name[-1:], qtd, out_form))


# função executada pelas threads
def run_thread(args):
    global solutions  # soluções dos sudokus
    thread_name = "T"+str((int(threading.current_thread().name[2:])+1))  # formatação do nome da thread("T_*" -> "T*")

    # percorre todos os números possivéis do sudoku
    for num in range(1, 10):
        # se algum número tem contagem diferente de 1 é porque está errado
        if (solutions[args[0]][args[1]][args[2]].count(str(num)) != 1):
            
            if (args[1] == 0):  # Se a thread estiver checando uma linha, retorna(nome_da_thread, L{qual linha esta errada})
                return (thread_name, "L"+str(int(args[2])+1))
            elif (args[1] == 1):  # Se a thread estiver checando uma coluna, retorna(nome_da_thread, C{qual coluna esta errada})
                return (thread_name, "C"+str(int(args[2])+1))
            else:  # Se a thread estiver checando uma regiao, retorna(nome_da_thread, R{qual regiao esta errada})
                return (thread_name, "R"+str(int(args[2])+1))
        else:
            continue


if __name__ == '__main__':
    n_args = len(sys.argv)  # número de argumentos via terminal
    arq = sys.argv[1]  # arquivo de soluções
    n_process = int(sys.argv[2])  # número de processos
    n_threads = int(sys.argv[3])  # número de threads

    if not(os.path.isfile(arq)):  # checa se o caminho do arquivo de soluções existe
        print("Entrada deve ser:$ python3 sudoku.py <arquivo soluções> <número processos trabalhadores> <número threads por processo trabalhador>")
        print("Arquivo solução inserido não existe")
        sys.exit()
    
    solutions = getSolutions(arq)  # retorna as soluções
    n_sol = len(solutions)  # numero de soluções

    if not(checkArgs(n_args, n_process, n_threads, n_sol)):  # checa se os argumentos são válidos
        sys.exit()

    ini = time.time()
    # cria o executor dos processos e executa(envia qual solução vai ser avaliada entre as n_sol soluções)
    ex_proc = ProcessPoolExecutor(max_workers=n_process)
    for ind_sol in range(n_sol):
        #ex_proc.submit(run_proc, (ind_sol))
        print(ex_proc.submit(run_proc, (ind_sol)).result())
    ex_proc.shutdown()
    fim = time.time()
    print("{} segundos".format(fim-ini))