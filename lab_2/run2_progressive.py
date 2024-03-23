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

# Удаление eps-правил
left_eps = {()}
left_eps.remove(())
non_terminal.clear()
non_terminal = sorted(gr)

for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        if r_product == ():
            left_eps.add(l_product)

# Определение порождающих нетерминалов
while True:
    len_left_eps = len(left_eps)
    for l_product in sorted(gr):
        for r_product in sorted(gr[l_product]):
            rplen = 0
            for alpha in r_product:
                if non_terminal.contains(alpha) and left_eps.contains(alpha):
                    rplen = rplen + 1
            if rplen == len(r_product):
                left_eps.add(l_product)
    if len_left_eps == len(left_eps):
        break

# Вывод порождающих нетерминалов
print("\neps - порождающие нетерминалы:")
print(left_eps)

# Удаление eps-правил
for l_product in sorted(gr):
    while True:
        pr_len = len(gr[l_product])
        for r_product in sorted(gr[l_product]):
            len_r_pr = r_product.len()
            for alpha in r_product:
                if left_eps.contains(alpha):
                    prod = str(r_product)
                    str1 = prod.replace(alpha, '')
                    str1 = str1.strip()
                    indx = 0
                    python_dict = literal_eval(str1)
                    as_list = list(python_dict)
                    for c in as_list:
                        if c == '':
                            del as_list[indx]
                        indx = indx + 1
                    python_dict = tuple(as_list)
                    gr[l_product].add(python_dict)
        if pr_len == len(gr[l_product]):
            break

# Удаление пустых правил и правил вида A -> A
for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        if r_product == () or (l_product == r_product[0] and r_product.len() == 1):
            gr[l_product].remove(r_product)

# Добавление нового стартового нетерминала, если старый был порождающим
if left_eps.contains(start_gr):
    gr[start_gr + '`'] = {()}
    gr[start_gr + '`'].add(start_gr)

print("\nУдалим eps-правила")
for l_product in sorted(gr):
    for r_product in (gr[l_product]):
        print(l_product, '=', *r_product)

# Удаление цепных правил
betas = {}
non_terminal_symbls = sorted(gr)

# Поиск цепных правил
for A_i in non_terminal_symbls:
    N_prev = A_i
    i = 1
    end = False
    while not end:
        N_i = set().union(N_prev)
        for B in N_prev:
            for C in gr[B]:
                if len(C) == 1 and C[0] in non_terminal_symbls:
                    N_i.add(C[0])
        if N_i != N_prev:
            N_prev = N_i
            i += 1
        else:
            betas[A_i] = N_i
            end = True

# Функция для проверки цепных правил
def is_chain(alpha, non_terminals):
    return len(alpha) == 1 and alpha[0] in non_terminals

# Удаление цепных правил из грамматики
new_gr = {}
for B, alphas in gr.items():
    for alpha in alphas:
        if not is_chain(alpha, non_terminal_symbls):
            for A, Bs in betas.items():
                if B in Bs:
                    if A in new_gr:
                        new_gr[A].add(alpha)
                    else:
                        new_gr[A] = {alpha}

print("\nУдалим цепные правила")
for l_product in sorted(new_gr):
    for r_product in new_gr[l_product]:
        print(l_product, '=', *r_product)