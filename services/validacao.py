import re


def validar_aluno(dados):
    
    nome, email, telefone, sexo, data, endereco, curso, _ = dados
    erros = []

    if not nome or len(nome.strip()) < 3:
        erros.append("• Nome deve ter pelo menos 3 caracteres.")

    if not email or not re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$", email, re.I):
        erros.append("• Email inválido (ex: aluno@email.com).")

    tel_raw = re.sub(r"\D", "", telefone)
    if len(tel_raw) < 10 or len(tel_raw) > 11:
        erros.append("• Telefone deve ter 10 ou 11 dígitos.")

    if not sexo:
        erros.append("• Selecione o sexo.")

    if not data:
        erros.append("• Informe a data de nascimento.")

    if not endereco or len(endereco.strip()) < 5:
        erros.append("• Endereço muito curto.")

    if not curso:
        erros.append("• Selecione o curso.")

    return erros


def mascarar_telefone(valor):
    
    raw = re.sub(r"\D", "", valor)[:11]
    if len(raw) == 11:
        return f"({raw[:2]}) {raw[2:7]}-{raw[7:]}"
    elif len(raw) > 6:
        return f"({raw[:2]}) {raw[2:6]}-{raw[6:]}"
    return raw