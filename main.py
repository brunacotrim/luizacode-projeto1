from fastapi import FastAPI

from app.routers import carrinhos, produtos, usuarios


descricao_api = "Esta API é responsável pelos carrinhos de compra, cadastro \
     de produtos e usuários da loja online SevenTeam."

app = FastAPI(title="API Carrinho de Compras",
    description=descricao_api,
    version="1.0.0",
    )

app.include_router(carrinhos.app)
app.include_router(usuarios.app)
app.include_router(produtos.app)

@app.get("/",
    tags=['Home'],
    responses= {
        200: {"description": "A API está disponível"}})
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')
