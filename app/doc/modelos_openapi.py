

MODELO_PRODUTO_200 = {
                "application/json": {
                    "example": {
                        "status": "OK",
                        "produto": {
                                "id": 123,
                                "nome": "Bicicleta Aro 29 Freio a Disco 21M. Velox Branca/Verde",
                                "descricao": "Bicicleta produzida com materiais de qualidade e foi criada pensando nas pessoas que desejam praticar o ciclismo e ter uma vida saudável.",
                                "preco": 1900.99,
                                "estoque": 34
                            }
                        }
                    }
                }

MODELO_LISTA_PRODUTO_200 = {
                "application/json": {
                    "example": {
                        "page": 1,
                        "per_page": 5,
                        "total": 2,
                        "produtos": [
                                {
                                    "id": 123,
                                    "nome": "Bicicleta Aro 29 Freio a Disco 21M. Velox Branca/Verde",
                                     "descricao": "Bicicleta produzida com materiais de qualidade e foi criada pensando nas pessoas que desejam praticar o ciclismo e ter uma vida saudável.",
                                    "preco": 1900.99,
                                    "estoque": 34
                                },
                                {
                                    "id": 456,
                                    "nome": "Fritadeira Elétrica sem Óleo/Air Fryer - Preto 3,2L com Timer",
                                    "descricao": "A fritadeira elétrica é um eletroportátil que não pode faltar na sua cozinha. O produto proporciona uma alimentação mais saudável.",
                                    "preco": 684.00,
                                    "estoque": 7
                                }
                            ]
                        }
                    }
                }

MODELO_EXCLUSAO_PRODUTO_200 = {
                "application/json": {
                    "example": {
                        "status": "OK",
                        "detalhes": "Produto excluído com sucesso"
                        }
                    }
                }