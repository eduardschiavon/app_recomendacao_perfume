import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def carregar_dados(nome_arquivo):
    # Esta linha garante que o Python ache o arquivo mesmo que seja .json ou .JSON
    caminho = os.path.join(os.getcwd(), nome_arquivo)
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def obter_signo(dia, mes):
    # Lógica simples para retornar o signo sem acentos
    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19): return "aries"
    if (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20): return "touro"
    if (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20): return "gemeos"
    if (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22): return "cancer"
    if (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22): return "leao"
    if (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22): return "virgem"
    if (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22): return "libra"
    if (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21): return "escorpiao"
    if (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21): return "sagitario"
    if (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19): return "capricornio"
    if (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18): return "aquario"
    return "peixes"

@app.route('/selecao', methods=['POST'])
def gerar_selecao():
    dados = request.json
    cidade = dados.get('cidade', 'nao informada')
    ocasiao = dados.get('ocasiao', 'dia_a_dia').lower()
    data_nasc = dados.get('data_nasc', '')

    # 1. Carregar Dados (Usando o nome exato que está no seu GitHub)
    db_signos = carregar_dados('Jjon_signo_perfume.JSON')
    db_ocasiao = carregar_dados('Jjon_ocasiao_perfume.JSON')

    # 2. Descobrir Signo
    try:
        dia, mes, _ = map(int, data_nasc.split('/'))
        signo = obter_signo(dia, mes)
    except:
        signo = "aries" # fallback

    # 3. Buscar Perfumes Reais
    # Pega o primeiro perfume da lista do signo ou da ocasiao
    perfume_signo = db_signos.get(signo, ["Fragrancia Astral"])[0] if db_signos else "Fragrancia Astral"
    perfume_ocasiao = db_ocasiao.get(ocasiao, ["Fragrancia Momento"])[0] if db_ocasiao else "Fragrancia Momento"

    return jsonify({
        "status": "sucesso",
        "mensagem": f"Selecao preparada para cliente em {cidade}.",
        "identidade": f"Sua assinatura baseada no signo de {signo.capitalize()} sugere {perfume_signo}.",
        "recomendacao": f"Para {ocasiao}, a nossa escolha principal e o {perfume_ocasiao}.",
        "dica": "Aplique nos pontos de pulsacao para uma melhor performance da fragrancia."
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
