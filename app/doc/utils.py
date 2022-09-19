OK = "OK"
FALHA = "FALHA"


def paginacao(page, per_page, itens):
    inicio = 0

    if per_page > 5:
        per_page = 5
    
    total = len(itens)
    if len(itens) > per_page:
        total = per_page

    if page > 1:
        inicio = (page-1) * per_page
        
        if len(itens) <= inicio:
            return 0, 0, 0, 0

        total = len(itens) - inicio
        if total > per_page:
            total = per_page

    fim = inicio + total

    return inicio, fim, total, per_page