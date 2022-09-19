from app.repositories.utils import OK, FALHA

db_usuarios = []
db_end = {}        # enderecos_dos_usuarios


def inserir_usuario(usuario):
    _, resultado_pesquisa = localizar_usuario(usuario.id)
    if resultado_pesquisa.get("usuario"):
        resultado = {
            "status": FALHA,
            "detalhes": f"Já existe usuário cadastrado com id {usuario.id}"
            }
        return False, resultado
    
    db_usuarios.append(dict(usuario))

    resultado = {
        "status": OK,
        "usuario": dict(usuario)
    }
    return True, resultado


def apagar_usuario(id_usuario):
    indice, _ = localizar_usuario(id_usuario)

    if indice == None:
        return {
            "status": FALHA,
            "detalhes": f"Não foi encontrado usuário com id {id_usuario}"
            }

    db_end.pop(id_usuario, None)
    db_usuarios.pop(indice)
    return {
            "status": OK,
            "detalhes": "Usuário excluído com sucesso"
            }


def localizar_usuario(id_usuario):
    for i in range(len(db_usuarios)):
        usu_id = db_usuarios[i].get("id")

        if usu_id == id_usuario:
            resultado = {
                "status": OK,
                "usuario": dict(db_usuarios[i])
            }
            return i, resultado

    resultado = {
                "status": FALHA,
                "detalhes": f"Não foi encontrado usuário com id {id_usuario}"
            }
    return None, resultado


def localizar_usuario_nome(nome):
    for i in range(len(db_usuarios)):
        usu_nome = db_usuarios[i].get("nome")
        primeiro_nome = usu_nome.split()

        if primeiro_nome[0].upper() == nome.upper():
            resultado = {
                "status": OK,
                "usuario": dict(db_usuarios[i])
            }
            return resultado

    return {
                "status": FALHA,
                "detalhes": f"Não foi encontrado usuário com o nome {nome}"
            }


def localizar_usuarios_dominio_email(dominio, page, per_page):
    emails = []
    for i in range(len(db_usuarios)):
        email = db_usuarios[i].get("email")

        if str.__contains__(email, '@' + dominio):
            emails.append(db_usuarios[i]["email"])

    if len(emails) == 0:
        return {
            "status": FALHA,
            "detalhes": "Não foram encontrados emails com o domínio informado"
            }

    return {
        "status": OK,
        "emails": sorted(emails)
    }


def inserir_endereco(endereco, id_usuario):
    indice, _ = localizar_usuario(id_usuario)

    if indice == None:
        resultado = {
            "status": FALHA,
            "detalhes": f"Não foi encontrado nenhum usuário cadastrado com o id {id_usuario}"}
        return resultado
    
    end_existente = db_end.get(id_usuario)
 
    if end_existente == None:
        db_end[id_usuario] = []

    db_end[id_usuario].append(dict(endereco))

    resultado = {
        "status": OK,
        "endereco": [dict(endereco)]
    }
    return resultado


def apagar_endereco(id_usuario, id_endereco):
    indice, _ = localizar_usuario(id_usuario)

    if indice == None:
        return {
            "status": FALHA,
            "detalhes": f"Não foi encontrado nenhum usuário cadastrado com o id {id_usuario}"
            }
    
    enderecos = db_end.get(id_usuario)

    if enderecos == None:
        return {
            "status": FALHA,
            "detalhes": f"Não foi encontrado nenhum endereço no cadastro do usuário"
            }

    for i in range(len(enderecos)):
        end_id = enderecos[i].get("id")
        
        if end_id == id_endereco:
            db_end[id_usuario].pop(i)

            if len(enderecos) == 0:
                db_end.pop(id_usuario, None)

            return {
                    "status": OK,
                    "detalhes": "Endereço excluído com sucesso"
                    }
    return {
        "status": FALHA,
        "detalhes": f"Não foi encontrado endereço com id {id_endereco}"
        }


def listar_enderecos_usuario(id_usuario):
    indice, _ = localizar_usuario(id_usuario)

    if indice == None:
        return {
            "status": FALHA,
            "detalhes": f"Não foi encontrado nenhum usuário cadastrado com o id {id_usuario}"}
    
    enderecos = db_end.get(id_usuario)
    if enderecos == None:
         return {
            "status": FALHA,
            "detalhes": f"Não foi encontrado nenhum endereço para o usuário com id {id_usuario}"}

    def ordenar_enderecos(e):
        return e["id"]

    enderecos.sort(key=ordenar_enderecos)

    return {
        "status": OK,
        "enderecos": enderecos
    }
