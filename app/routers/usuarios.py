from fastapi import APIRouter, status, Response, Query

from app.schemas.usuario import *
from app.repositories import usuarios

app = APIRouter(
    prefix="/usuario",
    tags=['Usuários']
)


# Criar um usuário,
# se tiver outro usuário com o mesmo ID retornar falha, 
# se o email não tiver o @ retornar falha, 
# senha tem que ser maior ou igual a 3 caracteres, 
# senão retornar OK
# Parametro query ? &
@app.post("/",
    status_code= status.HTTP_201_CREATED,
    summary= 'Insere um usuário',
    responses= {
        200: {"description": "Já existe usuário cadastrado \
            com o id informado"},
        201: {"description": "Usuário cadastrado com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def criar_usuário(usuario: Usuario, response: Response):
    """
    Método que cadastra um usuário do banco de dados.
    - **id**: Id do usuário. Se o id informado já existir na base \
        de dados, não será possível realizar o cadastro.
    - **nome**: Nome completo do usuário.
    - **email**: E-mail de login.
    - **senha**: Senha de acesso na loja virtual.
    """
    status, resultado = usuarios.inserir_usuario(usuario)
    if not(status):
        response.status_code = 200
    return resultado


# Se o id do usuário existir, deletar o usuário e retornar OK
# senão retornar falha
# ao deletar o usuário, deletar também endereços e carrinhos vinculados a ele
@app.delete("/",
    status_code= status.HTTP_200_OK,
    summary= 'Exclui um usuário',
    responses= {
        200: {"description": "Usuário excluído com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def deletar_usuario(id: int):
    """
    Método que exclui um usuário do banco de dados.
    """
    resultado = usuarios.apagar_usuario(id)
    return resultado


# Se o id do usuário existir, retornar os dados do usuário
# senão retornar falha
@app.get("/",
    status_code= status.HTTP_200_OK,
    summary= 'Recupera um usuário específico pelo id',
    responses= {
        200: {"description": "Consulta realizada com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def retornar_usuario(id: int):
    """
    Método que exibe os dados de um usuário específico, \
        através de pesquisa por id.
    """
    _, resultado = usuarios.localizar_usuario(id)
    return resultado


# Se existir um usuário com exatamente o mesmo nome, retornar os dados do usuário PRIMEIRO NOME
# senão retornar falha
@app.get("/nome",
    status_code= status.HTTP_200_OK,
    summary= 'Recupera um usuário específico pelo nome',
    responses= {
        200: {"description": "Consulta realizada com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def retornar_usuario_com_nome(nome: str):
    """
    Método que exibe os dados de um usuário específico, \
        através de pesquisa por nome.
    """
    resultado = usuarios.localizar_usuario_nome(nome)
    return resultado


# Retornar todos os emails que possuem o mesmo domínio
# (domínio do email é tudo que vêm depois do @)
# senão retornar falha
@app.get("/emails/",
    status_code= status.HTTP_200_OK,
    summary= 'Recupera lista de e-mails de um domínio específico',
    responses= {
        200: {"description": "Consulta realizada com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def retornar_emails(dominio: str,
    page: int = Query(default=1,
        description="Número da página"),
    per_page: int = Query(default=5,
        description="Quantidade de registros por página. Valor máximo: 5")):
    """
    Método que exibe a lista de e-mails de usuários, que são de um domínio específico.
    """
    resultado = usuarios.localizar_usuarios_dominio_email(dominio, page, per_page)
    return resultado


# Se não existir usuário com o id_usuario retornar falha, 
# senão cria um endereço, vincula ao usuário e retornar OK
@app.post("/{id_usuario}/endereco/",
    status_code= status.HTTP_201_CREATED,
    summary= 'Insere um endereço para o usuário',
    responses= {
        201: {"description": "Endereço cadastrado com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def criar_endereco(endereco: Endereco, id_usuario: int):
    """
    Método que insere um endereço para o usuário informado.
    - **id**: Id do endereço.
    - **rua**: Logradouro.
    - **cep**: Código postal.
    - **cidade**: Nome da cidade.
    - **estado**: Estado (UF).
    """
    resultado = usuarios.inserir_endereco(endereco, id_usuario)
    return resultado


# Se não existir endereço com o id_endereco retornar falha, 
# senão deleta endereço correspondente ao id_endereco e retornar OK
# (lembrar de desvincular o endereço ao usuário)
@app.delete("/{id_usuario}/endereco/{id_endereco}",
    status_code= status.HTTP_200_OK,
    summary= 'Exclui um endereço do usuário',
    responses= {
        200: {"description": "Endereço excluído com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def deletar_endereco(id_usuario: int, id_endereco: int):
    """
    Método que exclui um endereço do usuário.
    """
    resultado = usuarios.apagar_endereco(id_usuario, id_endereco)
    return resultado


# Se não existir usuário com o id_usuario retornar falha, 
# senão retornar uma lista de todos os endereços vinculados ao usuário
# caso o usuário não possua nenhum endereço vinculado a ele, retornar 
# uma lista vazia
### Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/{id_usuario}/enderecos/",
    status_code= status.HTTP_200_OK,
    summary='Recupera todos os endereços do usuário',
    responses= {
        200: {"description": "Consulta realizada com sucesso"},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    })
async def retornar_enderecos_do_usuario(id_usuario: int):
    """
    Método que exibe a lista de endereços do usuário informado.
    """
    resultado = usuarios.listar_enderecos_usuario(id_usuario)
    return resultado



