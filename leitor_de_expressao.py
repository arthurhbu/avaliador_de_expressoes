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
    
with open('./avaliador_de_expressoes/test_file.txt', 'r') as arquivo:
    expressoes = []
    expressoes = arquivo.readlines()
    expressoes_formatadas = list(map(format_str, expressoes))
    
    tokens = lexer(expressoes_formatadas[0])
    print(tokens)
    arvore = parser(tokens)
    printa_arvore(arvore)
        
        # for expressao in expressoes_formatadas:
        #     tokens = lexer(expressao)
        #     print(tokens)
        #     arvore = parser(tokens)
            
        