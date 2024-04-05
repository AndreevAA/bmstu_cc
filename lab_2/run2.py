from ast import literal_eval

gr_file = open('g10.txt')
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

start_gr = list(gr)[0]

print("Исходная грамматика")
for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        print(l_product, '=', *r_product)

# Удаление непорождающих нетерминалов
parent_non_terminal = {()}
non_terminal = sorted(gr)

for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        for alpha in r_product:
            if alpha.isupper() and not non_terminal.__contains__(alpha):
                non_terminal.append(alpha)

for NT in non_terminal:
    if gr.keys().__contains__(NT):
        for r_product in gr[NT].copy():
            if not any(nt in non_terminal for nt in r_product):
                parent_non_terminal.add(NT)

parent_non_terminal.remove(())

while True:
    start_len_parent = len(parent_non_terminal)
    for NT in non_terminal:
        if gr.keys().__contains__(NT):
            for r_product in gr[NT].copy():
                cnt = 0
                t_cnt = 0
                for alpha in r_product:
                    if non_terminal.__contains__(alpha):
                        if parent_non_terminal.__contains__(alpha):
                            cnt = 1
                        else:
                            cnt = 0
                            break
                if cnt == 1:
                    parent_non_terminal.add(NT)
    if start_len_parent == len(parent_non_terminal):
        break

for l_product in sorted(gr):
    if not (parent_non_terminal.__contains__(l_product)):
        gr.pop(l_product)

for l_product in sorted(gr):
    for r_product in gr[l_product].copy():
        for alpha in r_product:
            if non_terminal.__contains__(alpha):
                if not parent_non_terminal.__contains__(alpha):
                    gr[l_product].remove(r_product)

print("\nУдалим правила, содержащие непорождающие нетерминалы")
for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        print(l_product, '=', *r_product)

# Удаление недостижимых нетерминалов
non_terminal.clear()
non_terminal = sorted(gr)

for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        for alpha in r_product:
            if alpha.isupper() and not non_terminal.__contains__(alpha):
                non_terminal.append(alpha)

achievable_non_terminal = {()}
achievable_non_terminal.add(start_gr)
achievable_non_terminal.remove(())

while True:
    achievable_non_terminal_len = len(achievable_non_terminal)
    for l_product in sorted(gr):
        if achievable_non_terminal.__contains__(l_product):
            for r_product in sorted(gr[l_product]):
                for alpha in r_product:
                    if non_terminal.__contains__(alpha):
                        achievable_non_terminal.add(alpha)

    if achievable_non_terminal_len == len(achievable_non_terminal):
        break

for l_product in sorted(gr):
    if not achievable_non_terminal.__contains__(l_product):
        gr.pop(l_product)

print("\nУдалим недостижимые нетерминалы")
for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        print(l_product, '=', *r_product)

# Удаление eps-правил
start_gr = list(gr)[0]
left_eps = {()}
left_eps.remove(())
non_terminal.clear()
non_terminal = sorted(gr)

for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        if r_product == ():
            left_eps.add(l_product)

while True:
    len_left_eps = len(left_eps)
    for l_product in sorted(gr):
        for r_product in sorted(gr[l_product]):
            rplen = 0
            for alpha in r_product:
                if non_terminal.__contains__(alpha) and left_eps.__contains__(alpha):
                    rplen = rplen + 1
            if rplen == len(r_product):
                left_eps.add(l_product)
    if len_left_eps == len(left_eps):
        break

print("\neps - порождающие нетерминалы:")
print(left_eps)

for l_product in sorted(gr):
    while True:
        pr_len = len(gr[l_product])
        for r_product in sorted(gr[l_product]):
            len_r_pr = r_product.__len__()
            for alpha in r_product:
                if left_eps.__contains__(alpha):
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

for l_product in sorted(gr):
    for r_product in sorted(gr[l_product]):
        if r_product == () or (l_product == r_product[0] and r_product.__len__() == 1):
            gr[l_product].remove(r_product)

if left_eps.__contains__(start_gr):
    gr[start_gr + '`'] = {()}
    gr[start_gr + '`'].add(start_gr)

print("\nУдалим eps-правила")
for l_product in sorted(gr):
    for r_product in (gr[l_product]):
        print(l_product, '=', *r_product)

# Удаление цепных правил
betas = {}
non_terminal_symbls = sorted(gr)

for A_i in non_terminal_symbls:
    N_prev = A_i
    i = 1
    end = False
    while not end:
        N_i = set().union(N_prev)
        for B in N_prev:
            try:
                for C in gr[B]:
                    if len(C) == 1 and C[0] in non_terminal_symbls:
                        N_i.add(C[0])
            except:
                pass
        if N_i != N_prev:
            N_prev = N_i
            i += 1
        else:
            betas[A_i] = N_i
            end = True


def is_chain(alpha, non_terminals):
    return len(alpha) == 1 and alpha[0] in non_terminals


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
