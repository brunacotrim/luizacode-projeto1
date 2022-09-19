from fastapi import APIRouter, status, Response, Query

from app.schemas import produto
from app.repositories import produtos
from app.doc.modelos_openapi import *

app = APIRouter(
    prefix="/produto",
    tags=['Produtos']
)


# Se tiver outro produto com o mesmo ID retornar falha, 
# senão cria um produto e retornar OK
@app.post("/",
    status_code= status.HTTP_201_CREATED,
    summary= 'Insere um produto',
    responses= {
        200: {"description": "Já existe produto cadastrado \
            com o id informado"},
        201: {"description": "Produto cadastrado com sucesso",
            "content": MODELO_PRODUTO_200},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def criar_produto(produto: produto.Produto, response: Response):
    """
    Método que cadastra um produto do banco de dados.
    - **id**: Id do produto. Se o id informado já existir na base \
        de dados, não será possível inserir o produto.
    - **nome**: Nome do produto.
    - **descricao**: Descrição detalhada do produto.
    - **preco**: Preço do produto.
    - **quantidade**: Quantidade do produto.
    """
    status, resultado = produtos.inserir_produto(produto)
    if not(status):
        response.status_code = 200
    return resultado


# Se não existir produto com o id_produto retornar falha, 
# senão deleta produto correspondente ao id_produto e retornar OK
# (lembrar de desvincular o produto dos carrinhos do usuário)
@app.delete("/{id_produto}/",
    status_code= status.HTTP_200_OK,
    summary= 'Exclui um produto',
    responses= {
        200: {"description": "Produto excluído com sucesso",
            "content": MODELO_EXCLUSAO_PRODUTO_200},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def deletar_produto(id_produto: int):
    """
    Método que exclui um produto do banco de dados.
    """
    resultado = produtos.apagar_produto(id_produto)
    return resultado


@app.get("/{id_produto}/",
    status_code= status.HTTP_200_OK,
    summary= 'Recupera um produto específico pelo id',
    responses= {
        200: {"description": "Consulta realizada com sucesso",
            "content": MODELO_PRODUTO_200},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def pesquisar_produto(id_produto: int):
    """
    Método que exibe os dados de um produto específico \
        através de pesquisa por id.
    """
    _, resultado = produtos.localizar_produto(id_produto)
    return resultado


@app.get("/",
    status_code= status.HTTP_200_OK,
    summary='Recupera todos os produtos cadastrados',
    responses= {
        200: {"description": "Consulta realizada com sucesso",
            "content": MODELO_LISTA_PRODUTO_200},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def listar_produtos(
    page: int = Query(default=1,
        description="Número da página"),
    per_page: int = Query(default=5,
        description="Quantidade de registros por página. Valor máximo: 5")):
    """
    Método que exibe uma lista com os dados dos \
        produtos cadastrados.
    """
    resultado = produtos.listar_produtos(page, per_page)
    return resultado
