from pydantic import BaseModel


# Classe representando os dados do produto
class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int
