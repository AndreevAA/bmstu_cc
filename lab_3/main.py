# from parser import Parser
from vizual import Parser

tests = [
    # '{ a := 3 ; aaa := p ; { a := p ; x := p and not p ; } ; } ' # верно по 
    """
    {
        a := 3 ;
        aaa := p ;
        { 
            a := p ;
            x := p and not p ;
        } ;
    } 
    """ # верно
    #'{ a := ( abs p and ( 1 ** 25 ) ) }', 
    #'{ a := 1 and - ( + p and 1 ** 2 ** 455 ) }', 
    #'{ c := not ( p mod 5 / ( 2 + 2 ) ) }', 
    #'{ c := abs ( - p + 2 & 4 mod 5 / ( 2 ) ) }', 
    #'{ ll := ( p and - 22 ) }'
]

# Было

# <блок>
#     { <список операторов> }

# <список операторов> 
#     <оператор> <хвост>

# <хвост>
#     ; <оператор> <хвост> | e

# <оператор>
#     <идентификатор> = <выражение> | <блок>

# Стало
# <блок>
#     { <список операторов> }

# <список операторов> 
#     <оператор> ; <список операторов> | e

# <оператор>
#     <идентификатор> = <выражение> | <блок>


def main(input_string):
    input_string_split = list(input_string.strip().split())
    print()
    print('Tokens')
    print(input_string_split)
    parser = Parser(input_string_split)
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