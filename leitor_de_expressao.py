import re
from igraph import Graph, plot


class noArvore:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None

def format_str(string: str) -> str:
    string = string.replace('\n', '')
    return string

def olhar_topo_pilha(pilha: list):
    return pilha[-1] if pilha else None

def maior_precedencia(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def printa_arvore(node, level=0, prefix="Raiz: "):
    if node is not None:
        print(" " * (level * 4) + prefix + str(node.valor))
        if node.esquerda or node.direita:
            if node.esquerda:
                printa_arvore(node.esquerda, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if node.direita:
                printa_arvore(node.direita, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")

def lexer(expression):
    pattern = r'-?\d+|\d+|[()+\-*/]'
    tokens = re.findall(pattern, expression)
    tokens = [int(token) if re.fullmatch(r'-?\d+', token) else token for token in tokens]
    return tokens

def parser(list_tokens: list) -> list:
    
    operadores = ['+','-','*','/']
    fila_saida, pilha_operador = [], []
    for token in list_tokens:
        if isinstance(token, int):
            fila_saida.append(noArvore(token))
        elif token == '(':  
            pilha_operador.append(token)
        elif token == ')':
            while olhar_topo_pilha(pilha_operador) and olhar_topo_pilha(pilha_operador) != '(':
                # aplicar_operadores(pilha_operador, fila_saida)
                fila_saida.append(noArvore(pilha_operador.pop()))
            pilha_operador.pop()
        else:
            while (pilha_operador and maior_precedencia(pilha_operador[-1]) >= maior_precedencia(token)):
                # aplicar_operadores(pilha_operador, fila_saida)
                fila_saida.append(noArvore(pilha_operador.pop()))
            pilha_operador.append(token)
    while olhar_topo_pilha(pilha_operador):
        fila_saida.append(noArvore(pilha_operador.pop()))
        
    no_pilha = []
    
    for token in fila_saida:
        if isinstance(token.valor, int):
            no_pilha.append(token)
        else:
            no_arvore = token
            no_arvore.direita = no_pilha.pop()
            no_arvore.esquerda = no_pilha.pop()
            no_pilha.append(no_arvore)
            
    return no_pilha[0] if no_pilha else None

def eval_step(no_arvore: noArvore) -> noArvore:
    if no_arvore.direita and no_arvore.esquerda:
        if isinstance(no_arvore.esquerda.valor, int) and isinstance(no_arvore.direita.valor, int): 
            if no_arvore.valor == '+':
                return noArvore(no_arvore.esquerda.valor + no_arvore.direita.valor)
            elif no_arvore.valor == '-':
                return noArvore(no_arvore.esquerda.valor - no_arvore.direita.valor)
            elif no_arvore.valor == '*':
                return noArvore(no_arvore.esquerda.valor * no_arvore.direita.valor)
            elif no_arvore.valor == '/':
                return noArvore(no_arvore.esquerda.valor // no_arvore.direita.valor) 
            
    return no_arvore
    
def eval_tree(no_arvore: noArvore) -> noArvore:
    if no_arvore is None or (no_arvore.esquerda is None and no_arvore.direita is None):
        return no_arvore
    
    no_arvore.esquerda = eval_tree(no_arvore.esquerda)
    no_arvore.direita = eval_tree(no_arvore.direita)
    
    no_arvore_pos_eval = eval_step(no_arvore)
    
    return no_arvore_pos_eval      

def to_string(no_arvore: noArvore) -> str:
    if not no_arvore.direita and not no_arvore.esquerda:
        return str(no_arvore.valor)
    
    str_esquerda = to_string(no_arvore.esquerda)
    str_direita = to_string(no_arvore.direita)
    
    print(f"({str_esquerda} {no_arvore.valor} {str_direita})")
    return f"({str_esquerda} {no_arvore.valor} {str_direita})"

def evaluate_expressions(input_file: __file__) -> None:
    
    with open('./avaliador_de_expressoes/test_file.txt', 'r') as arquivo:
        expressoes = []
        expressoes = arquivo.readlines()
        expressoes_formatadas = list(map(format_str, expressoes))
        
        for expressao in expressoes_formatadas:
            tokens = lexer(expressao)
            print('Expressão separada em tokens: ', tokens)
            print('\n')
            arvore = parser(tokens)
            print('Arvore da expressão: ')
            printa_arvore(arvore)
            print('\n')
            if arvore is None:
                print('Expressão inválida!')
                return
            while arvore.esquerda or arvore.direita:
                print('Transformação da árvore para expressão: ')
                to_string(arvore)
                arvore = eval_tree(arvore)
            print('\n')
            print('Resultado da expressão: ', arvore.valor)
            print('\n')

            
if __name__ == "__main__":
    evaluate_expressions('nada')
        