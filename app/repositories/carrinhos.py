from app.repositories.utils import OK, FALHA
from app.repositories import produtos, usuarios

db_carrinhos = []


def inserir_carrinho(id_usuario, id_produto):
	existe_usuario, _ = usuarios.localizar_usuario(id_usuario)
	if  existe_usuario == None:
		resultado = {
			"status": FALHA,
			"detalhes": f"Não existe usuário cadastrado com id {id_usuario}"
			}
		return False, resultado

	existe_produto, produto_resultado = produtos.localizar_produto(id_produto)
	if existe_produto == None:
		resultado = {
			"status": FALHA,
			"detalhes": f"Não existe produto cadastrado com o id {id_produto}"
			}
		return False, resultado
	
	produto = produto_resultado.get("produto")

	preco_total = produto.get("preco")
	quantidade_de_produtos = produto.get("quantidade")

	indice_carrinho, carrinho_retornado = localizar_carrinho(id_usuario)

	if indice_carrinho == None:
		id_produtos = list([id_produto])

		carrinho_novo = {"id_usuario": id_usuario,
				"id_produtos": id_produtos,
				"preco_total": preco_total,
				"quantidade_de_produtos": quantidade_de_produtos}

		db_carrinhos.append(carrinho_novo)

		resultado = {
			"status": OK,
			"carrinho": dict(carrinho_novo)
		}
		return True, resultado
	
	carrinho_resultado = carrinho_retornado.get("carrinho")
	preco_total += carrinho_resultado.get("preco_total")
	quantidade_de_produtos += carrinho_resultado.get("quantidade_de_produtos")

	db_carrinhos[indice_carrinho]["id_produtos"].append(id_produto)
	db_carrinhos[indice_carrinho]["preco_total"] = round(preco_total, 2)
	db_carrinhos[indice_carrinho]["quantidade_de_produtos"] = round(quantidade_de_produtos, 2)

	resultado = {
		"status": OK,
		"carrinho": db_carrinhos[indice_carrinho]
	}
	return True, resultado


def apagar_carrinho(id_usuario):
    indice_carrinho, _ = localizar_carrinho(id_usuario)

    if indice_carrinho == None:
        return {
            "status": FALHA,
            "detalhes": f"Não foi encontrado carrinho para o usuário com id {id_usuario}"
            }

    db_carrinhos.pop(indice_carrinho)
    return {
            "status": OK,
            "detalhes": "Carrinho excluído com sucesso"
            }


def localizar_carrinho(id_usuario):

	for i in range(len(db_carrinhos)):
		usu_id = db_carrinhos[i].get("id_usuario")

		if usu_id == id_usuario:
			resultado = {
				"status": OK,
				"carrinho": dict(db_carrinhos[i])
			}
			return i, resultado

	resultado = {
		"status": FALHA,
		"detalhes": f"Não foi encontrado carrinho com as informações especificadas"
	}

	return None, resultado


def consulta_totais_carrinho(id_usuario):
	for i in range(len(db_carrinhos)):
		usu_id = db_carrinhos[i].get("id_usuario")

		if usu_id == id_usuario:
			valor_total = db_carrinhos[i].get("preco_total")
			quantidade_total_itens = db_carrinhos[i].get("quantidade_de_produtos")

			return {
				"status": OK,
				"valor_total": valor_total,
				"quantidade_total_itens": quantidade_total_itens
			}

	return {
			"status": FALHA,
			"detalhes": f"Não foi encontrado carrinho com id {id_usuario}"
		}
