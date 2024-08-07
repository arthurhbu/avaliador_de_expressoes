import re

class no_arvore:
    def __init__(self, value) -> None:
        self.value = value
        self.esquerda = None
        self.direita = None


def format_str(string: str) -> str:
    string = string.replace('\n', '')
    return string

def lexer(expression):
    pattern = r'-?\d+|\d+|[()+\-*/]'
    tokens = re.findall(pattern, expression)
    tokens = [int(token) if re.fullmatch(r'-?\d+', token) else token for token in tokens]
    return tokens
    



def parser(list_tokens: list) -> list:
    ...
    



with open('./avaliador_de_expressoes/test_file.txt', 'r') as arquivo:
        expressoes = []
        expressoes = arquivo.readlines()
        expressoes_formatadas = list(map(format_str, expressoes))
        
        for expressao in expressoes_formatadas:
            tokens = lexer(expressao)
            print(tokens)
            
        