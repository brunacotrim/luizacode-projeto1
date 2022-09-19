from app.repositories import utils
from app.repositories.utils import OK, FALHA

db_produtos = []


def inserir_produto(produto):
    _, resultado_pesquisa = localizar_produto(produto.id)
    if resultado_pesquisa.get("produto"):
        resultado = {
            "status": FALHA,
            "detalhes": f"Já existe produto cadastrado com id {produto.id}"
            }
        return False, resultado
    
    db_produtos.append(dict(produto))

    resultado = {
        "status": OK,
        "produto": dict(produto)
    }
    return True, resultado


def apagar_produto(id_produto):
    indice, _ = localizar_produto(id_produto)

    if indice == None:
        return {
            "status": FALHA,
            "detalhes": f"Não foi encontrado produto com id {id_produto}"
            }

    db_produtos.pop(indice)
    return {
            "status": OK,
            "detalhes": "Produto excluído com sucesso"
            }


def localizar_produto(id_produto):
    for i in range(len(db_produtos)):
        prod_id = db_produtos[i].get("id")

        if prod_id == id_produto:
            resultado = {
                "status": OK,
                "produto": dict(db_produtos[i])
            }
            return i, resultado

    resultado = {
                "status": FALHA,
                "detalhes": f"Não foi encontrado produto com id {id_produto}"
            }
    return None, resultado


def listar_produtos(page, per_page):
    if len(db_produtos) == 0:
        return {
            "status": FALHA,
            "detalhes": "Não há produtos cadastrados"
            }

    def ordenar_produtos(e):
        return e["id"]

    db_produtos.sort(key=ordenar_produtos)

    inicio, fim, total, per_page = utils.paginacao(page, per_page, db_produtos)

    if fim == 0:
        return {
            "status": FALHA,
            "detalhes": "Não foram encontrados produtos através dos parâmetros especificados"
            }

    produtos = db_produtos[inicio:fim]

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "produtos": produtos
    }
