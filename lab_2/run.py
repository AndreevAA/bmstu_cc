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

print("Исходная грамматика")
for l_product in gr:
    for r_product in gr[l_product]:
        print(l_product, '=', *r_product)

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

    gr[A_i + '`'] = {()}
    for alpha_i in gr[A_i].copy():
        gr[A_i].remove(alpha_i)
        if alpha_i and alpha_i[0] == A_i:
            gr[A_i + '`'].add(alpha_i[1:] + (A_i + '`',))
        else:
            gr[A_i].add(alpha_i + (A_i + '`',))

print("Преобразованная грамматика")
for l_product in sorted(gr):
    for r_product in gr[l_product]:
        print(l_product, '=', *r_product)
