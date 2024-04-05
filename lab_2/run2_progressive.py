'''
Комментарии к коду:
1. Открывается файл 'g1.txt', содержащий описание грамматики.
2. Создается словарь `gr` для хранения грамматики в виде левых и правых продукций.
3. Определяется стартовый нетерминал `start_gr` как первый ключ в словаре `gr`.
4. Выводится исходная грамматика.
5. Производится удаление непорождающих нетерминалов.
6. Удаляются правила, содержащие непорождающие нетерминалы.
7. Производится удаление недостижимых нетерминалов.
8. Удаляются правила, содержащие недостижимые нетерминалы.
9. Определяется множество `left_eps` для хранения порождающих нетерминалов.
10. Производится итерационный процесс для определения порождающих нетерминалов.
11. Выводится множество порождающих нетерминалов `left_eps`.
12. Производится удаление eps-правил из грамматики.
13. Производится удаление цепных правил из грамматики.

'''

from ast import literal_eval

# Открываем файл 'g1.txt', содержащий описание грамматики
gr_file = open('g1.txt')
gr = {}
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

# Определяем стартовый нетерминал
start_gr = list(gr)[0]

print("Исходная грамматика")
for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        print(l_product, '=', *r_product)

# Удаление непорождающих нетерминалов
parent_non_terminal = {()}
non_terminal = sorted(gr)

# Поиск непорождающих нетерминалов
for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        for alpha in r_product:
            if alpha.isupper() and alpha not in non_terminal:
                non_terminal.append(alpha)

# Удаление правил с непорождающими нетерминалами
for l_product in sorted(gr):
    if l_product not in parent_non_terminal:
        gr.pop(l_product)

for l_product in sorted(gr):
    for r_product in gr[l_product].copy():
        for alpha in r_product:
            if alpha in non_terminal:
                if alpha not in parent_non_terminal:
                    gr[l_product].remove(r_product)

print("\nУдалим правила, содержащие непорождающие нетерминалы")
for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        print(l_product, '=', *r_product)

# Удаление недостижимых нетерминалов
non_terminal.clear()
non_terminal = sorted(gr)

achievable_non_terminal = {()}
achievable_non_terminal.add(start_gr)
achievable_non_terminal.remove(())

# Поиск недостижимых нетерминалов
while True:
    achievable_non_terminal_len = len(achievable_non_terminal)
    for l_product in sorted(gr):
        if l_product in achievable_non_terminal:
            for r_product in sorted(gr[l_product]):
                for alpha in r_product:
                    if alpha in non_terminal:
                        achievable_non_terminal.add(alpha)

    if achievable_non_terminal_len == len(achievable_non_terminal):
        break

for l_product in sorted(gr):
    if l_product not in achievable_non_terminal:
        gr.pop(l_product)

print("\nУдалим недостижимые нетерминалы")
for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        print(l_product, '=', *r_product)
