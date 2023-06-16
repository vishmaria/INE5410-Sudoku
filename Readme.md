# Verificador de Sudoku Concorrente
O trabalho 2 consiste em desenvolver um validador de soluções de quebra-cabeças sudoku em Python de maneira paralela. A regra para a colocação dos números nas células vazias é a seguinte. Em cada coluna, linha e região da grade, os números de 1 à 9 só podem aparecer uma única vez. Em outras palavras, não é permitido a repetição de um número em uma mesma linha, coluna ou região da grade.
## Entrada
As soluções a serem validadas serão fornecidas através de um arquivo texto, o qual conterá um conjunto de grades de tamanho **9x9**, separadas entre si por uma linha em branco.
O seu programa deve receber como parâmetros de entrada:
 **(I)** o nome do arquivo com as soluções a serem validadas, 
**(II)** o número de processos trabalhadores 
e 
**(III)** o número de threads de correção a serem utilizadas por cada processo trabalhador.

## Validação
Após serem criados, os processos trabalhadores deverão dividir o trabalho de validação das soluções de Sudoku fornecidas no arquivo. Cada *processo trabalhador* contará com um conjunto de *threads de correção* para verificar possíveis erros em cada grade destinada ao processo trabalhador. Portanto, a verificação das regras do jogo sobre as linhas, colunas e regiões para uma grade deverá, necessariamente, ser *feita de forma concorrente* por diferentes *threads de correção* do *processo trabalhador.*
A forma de divisão do trabalho computacional a ser realizado para validar todas as soluções fornecidas no arquivo deverá ser definida pelo grupo. Porém, deseja-se evitar ao máximo que processos trabalhadores e threads de correção sejam criados e permaneçam ociosos sem realizar nenhum trabalho. A solução deverá funcionar para diferentes números de processos trabalhadores e threads de correção, evitando-se, porém, a criação de processos trabalhadores e/ou threads de correção quando não for possível e/ou necessário.

## Saída
Antes de começar o processamento de um quebra-cabeças, o processo trabalhador deve imprimir na tela
 `Processo P: resolvendo quebra-cabeças S`
 onde **P** é um identificador único de processo trabalhador e **S** é um identificador
único de quebra-cabeças, conforme ordem disposta no arquivo de entrada. Uma vez terminado o processamento do quebra-cabeças pelo processo, o mesmo deverá imprimir na tela a *quantidade de erros encontrados* e, havendo erros, os *locais em que as threads de correção encontraram os erros* utilizando as seguintes siglas: 
**L** (erro em uma linha),
 **C** (erro em uma coluna) e 
 **R** (erro em uma região). 
Além da sigla, deverá ser informado um número, que representará a linha/coluna/região em que o erro foi encontrado. 
O **identificador de processos trabalhadores, threads de correção e quebra-cabeças** deverá ser um **número inteiro sequencial** entre 1 e n , onde n é o número total processos, o número total de threads de correção de um processo trabalhador ou o número total de quebra-cabeças fornecido no arquivo de entrada. Em caso de erros encontrados, a ordem de apresentação seguirá a ordem crescente da numeração das threads corretoras (T1, T2, ...). 
A impressão da localização dos erros encontrados pelas threads corretoras deverá obedecer a seguinte ordem: 

 - Erros encontrados nas linhas (**L**),   
 - depois colunas (**C**),
 -  e por fim nas regiões (**R**).

O caractere “`;`” deverá ser utilizado para separar as informações dos erros encontrados por cada thread.

> Exemplo de saída válida:

```
$ python sudoku solucoes.txt 2 2
Processo 1: resolvendo quebra-cabeças 1
Processo 2: resolvendo quebra-cabeças 2
Processo 1: 0 erros encontrados
Processo 2: 5 erros encontrados (T1: C1, C9, R9; T2: L4, C2)
```

> Written with [StackEdit](https://stackedit.io/).

