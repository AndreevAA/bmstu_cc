# from parser import Parser
from vizual import M

tests = [
    '{ a := 3 ; aaa := p ; { a := p ; x := p and not p } }' 
    # '{ a := ( abs p and ( 1 ** 25 ) ) }', 
    # '{ a? := 1 and - ( + p and 1 ** 2 ** 455 ) }', 
    # '{ c := not ( p mod 5 / ( 2 + 2 ) ) }', 
    # '{ c := abs ( - p + 2 & 4 mod 5 / ( 2 ) ) }', 
    # '{ ll := ( p and - 22 ) }'
]

def main(input_string):
    input_string_split = list(input_string.strip().split())
    print()
    print('Tokens')
    print(input_string_split)
    parser = M(input_string_split)
    parser.render_tree()


if __name__ == "__main__":
    
    for _ in tests:
        main(_)

    # input = '{ a := 3 ; aaa := p ; { a := p ; x := p and not p } }'
    # input = '{ a := ( abs p and ( 1 ** 25 ) ) }'
    # input = '{ a? := 1 and - ( + p and 1 ** 2 ** 455 ) }'
    # input = '{ c := not ( p mod 5 / ( 2 + 2 ) ) }'
    # input = '{ c := abs ( - p + 2 & 4 mod 5 / ( 2 ) ) }'
    #input = '{ ll := ( p and - 22 ) }'
    #input = list(input.strip().split())
    # print('Tokens')
    # print(input)
    # parser = Parser(input)