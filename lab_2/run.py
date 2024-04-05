'''
Комментарии к коду:
1. Открывается файл 'gi.txt', содержащий описание грамматики.
2. Создается пустой словарь `gr` для хранения грамматики в виде левых и правых продукций.
3. Каждая строка из файла обрабатывается, удаляются лишние пробелы.
4. Левая и правая части продукции разделяются по символу '='.
5. Левая и правая части продукции очищаются от лишних пробелов и преобразуются в кортеж.
6. Проверяется, существует ли уже левая часть продукции в словаре `gr`, и добавляется правая часть.
7. Выводится исходная грамматика.
8. Производится преобразование грамматики путем удаления левой рекурсии и добавления новых продукций.
9. Выводится преобразованная грамматика.
'''

# Открываем файл 'g1.txt', содержащий описание грамматики
gr_file = open('g3.txt')
gr = {}

# Чтение и обработка строк файла для создания грамматики
for line in gr_file:
    line = line.strip()
    if not line:
        continue
    l_product, r_product = line.split('=')
    l_product = l_product.strip()
    r_product = r_product.strip()
    r_product = tuple(r_product.split())
    if l_product in gr:
        gr[l_product].add(r_product)
    else:
        gr[l_product] = {r_product}

# Вывод исходной грамматики
print("Исходная грамматика")
for l_product in gr:
    for r_product in gr[l_product]:
        print(l_product, '=', *r_product)

def print_new_grammer(gr):
    # Вывод преобразованной грамматики
    print("Преобразованная грамматика")
    for l_product in sorted(gr):
        for r_product in gr[l_product]:
            print(l_product, '=', *r_product)

# Преобразование грамматики
non_terminal = sorted(gr)
for A_i in non_terminal:
    for A_j in non_terminal:
        if A_j == A_i:
            break
        for r_product in gr[A_i].copy():
            if not r_product or r_product[0] != A_j:
                continue
            gamma = r_product[1:]
            gr[A_i].remove((A_j,) + gamma)
            for sigma in gr[A_j]:
                gr[A_i].add(sigma + gamma)
            print_new_grammer(gr)

    print_new_grammer(gr)

    gr[A_i + '`'] = {()}
    for alpha_i in gr[A_i].copy():
        gr[A_i].remove(alpha_i)
        if alpha_i and alpha_i[0] == A_i:
            gr[A_i + ''].add(alpha_i[1:] + (A_i + '',))
        else:
            gr[A_i].add(alpha_i + (A_i + '`',))
    
    print_new_grammer(gr)

# Вывод преобразованной грамматики
print("Преобразованная грамматика")
for l_product in sorted(gr):
    for r_product in gr[l_product]:
        print(l_product, '=', *r_product)