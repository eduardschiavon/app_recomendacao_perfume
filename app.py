from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import csv
import os
from datetime import datetime


app = Flask(__name__)
CORS(app)


# Função para carregar seus arquivos JSON
def carregar_dados(arquivo):
    caminho = os.path.join(os.path.dirname(__file__), arquivo)
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# Função para salvar a pesquisa da cliente para você analisar depois
def registrar_pesquisa(dados):
    arquivo = 'pesquisas_clientes.csv'
    colunas = ['id', 'data_hora', 'cidade', 'signo', 'nota_favorita', 'ocasiao']
    existe = os.path.exists(arquivo)
    
    with open(arquivo, 'a', newline='', encoding='utf-8-sig') as f:
        escritor = csv.DictWriter(f, fieldnames=colunas)
        if not existe:
            escritor.writeheader()
        escritor.writerow(dados)


@app.route('/selecao', methods=['POST'])
def gerar_selecao():
    # Recebe os dados da cliente (Cidade, Data de Nascimento, Nota Favorita, Ocasiao)
    entrada = request.json
    
    cidade = entrada.get('cidade', 'Nao informada')
    nota_fav = entrada.get('nota_fav', 'Geral')
    ocasiao = entrada.get('ocasiao', 'Dia a dia')
    data_nasc = entrada.get('data_nasc', '01/01/2000')


    # Exemplo de lógica simplificada baseada nos seus arquivos
    # Aqui voce carregaria o Jjon_signo_perfume.JSON e buscaria pelo signo
    # Vamos gerar um ID unico para sua pesquisa
    id_pesquisa = f"{data_nasc.replace('/', '')}-{cidade[:3].lower()}"
    
    # Registro silencioso no seu banco de dados
    registrar_pesquisa({
        'id': id_pesquisa,
        'data_hora': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'cidade': cidade,
        'signo': "Signo Identificado", # Aqui entraria a logica de data -> signo
        'nota_favorita': nota_fav,
        'ocasiao': ocasiao
    })


    # Resposta limpa para a cliente (sem emojis ou negritos)
    resposta = {
        "status": "sucesso",
        "mensagem": f"Selecao preparada para cliente em {cidade}.",
        "identidade": "Sua assinatura astral baseada em seu perfil.",
        "recomendacao": f"Para {ocasiao}, sugerimos uma fragrancia que harmonize com {nota_fav}.",
        "dica": f"Como voce aprecia {nota_fav}, recomendamos aplicar o perfume em pontos de pulsacao."
    }
    
    return jsonify(resposta)


if __name__ == '__main__':
    # O Render e o Railway exigem que a porta seja definida por variavel de ambiente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
