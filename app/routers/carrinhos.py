from fastapi import APIRouter, status, Response

from app.schemas import carrinho
from app.repositories import carrinhos

app = APIRouter(
    prefix="/carrinho",
    tags=['Carrinho de Compra']
)


# Se não existir usuário com o id_usuario ou id_produto retornar falha, 
# se não existir um carrinho vinculado ao usuário, crie o carrinho
# e retornar OK
# senão adiciona produto ao carrinho e retornar OK
@app.post("/{id_usuario}/{id_produto}/",
    status_code= status.HTTP_201_CREATED,
    summary= 'Insere um carrinho de compras',
    responses= {
        200: {"description": "Já existe carrinho cadastrado \
            para o cliente informado"},
        201: {"description": "Carrinho cadastrado com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def adicionar_carrinho(id_usuario: int, id_produto: int, response: Response):
    """
    Método que cadastra o carrinho de compras e adiciona o produto.
    - **id_usuario**: Id do usuário. Deve estar cadastrado previamente.
    - **id_produtos**: Id do produto. Deve estar cadastrado previamente.
    - **preco_total**: Valor total do carrinho.
    - **quantidade_de_produtos**: Quantidade total do carrinho.
    """
    status, resultado = carrinhos.inserir_carrinho(id_usuario, id_produto)
    if not(status):
        response.status_code = 200
    return resultado


# Se não existir usuário com o id_usuario retornar falha, 
# senão deleta o carrinho correspondente ao id_usuario e retornar OK
@app.delete("/{id_usuario}/",
    status_code= status.HTTP_200_OK,
    summary= 'Exclui um produto do carrinho de compras',
    responses= {
        200: {"description": "Carrinho excluído com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def deletar_carrinho(id_usuario: int):
    """
    Método que exclui um carrinho de compras.
    """
    resultado = carrinhos.apagar_carrinho(id_usuario)
    return resultado


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o carrinho de compras.
@app.get("/{id_usuario}/",
    status_code= status.HTTP_200_OK,
    summary= 'Recupera o carrinho de um usuário',
    responses= {
        200: {"description": "Consulta realizada com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def retornar_carrinho(id_usuario: int):
    """
    Método que exibe o carrinho de compras de um usuário específico, \
        através do id do usuário.
    """
    _, resultado = carrinhos.localizar_carrinho(id_usuario)
    return resultado


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o o número de itens e o valor total do carrinho de compras.
@app.get("/total/{id_usuario}/",
    status_code= status.HTTP_200_OK,
    summary= 'Recupera quantidade e total do carrinho de um usuário',
    responses= {
        200: {"description": "Consulta realizada com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def retornar_total_carrinho(id_usuario: int):
    """
    Método que exibe a quantidade total de itens e o valor total de \
        um carrinho de um usuário.
    """
    resultado = carrinhos.consulta_totais_carrinho(id_usuario)
    return resultado

