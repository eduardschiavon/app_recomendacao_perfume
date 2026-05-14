import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def carregar_dados(nome_arquivo):
    caminho = os.path.join(os.getcwd(), nome_arquivo)
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def obter_signo(dia, mes):
    # Removi acentos das chaves para bater com o seu JSON
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
    try:
        dados = request.json
        cidade = dados.get('cidade', 'nao informada')
        ocasiao = dados.get('ocasiao', 'dia_a_dia').lower()
        data_string = dados.get('data_nasc', '').strip()

        # --- LÓGICA DE DATA REFORÇADA ---
        try:
            # Tenta converter a data. Se o usuário digitar 84, vira 1984.
            partes = data_string.split('/')
            dia = int(partes[0])
            mes = int(partes[1])
            ano = int(partes[2])
            
            if ano < 100: # Se digitaram só "84"
                ano += 1900 if ano > 25 else 2000
            
            hoje = datetime.now()
            idade = hoje.year - ano
            # Ajuste fino: se ainda não fez aniversário este ano, subtrai 1
            if (hoje.month, hoje.day) < (mes, dia):
                idade -= 1
                
            signo = obter_signo(dia, mes)
        except Exception as e:
            print(f"Erro na data: {e}")
            idade = 0
            signo = "peixes" # Fallback se der erro
        # --------------------------------

        db_signos = carregar_dados('Jjon_signo_perfume.JSON')
        db_ocasiao = carregar_dados('Jjon_ocasiao_perfume.JSON')
        dataset = carregar_dados('dataset_perfumes.json')

        # Busca por Idade
        perfume_idade = "Fragrancia de Prestigio"
        if dataset:
            for p in dataset:
                i_min = p.get('Idade_Min') or p.get('idade_min', 0)
                i_max = p.get('Idade_Max') or p.get('idade_max', 100)
                if i_min <= idade <= i_max:
                    perfume_idade = p.get('Perfume', 'Fragrancia Especial')
                    break

        p_signo = db_signos.get(signo, ["Fragrancia Astral"])[0] if db_signos else "Fragrancia Astral"
        p_ocasiao = db_ocasiao.get(ocasiao, ["Fragrancia Momento"])[0] if db_ocasiao else "Fragrancia Momento"

        return jsonify({
            "status": "sucesso",
            "mensagem": f"Seleção preparada para cliente em {cidade}.",
            "identidade": f"Sua assinatura baseada no signo de {signo.capitalize()} sugere {p_signo}.",
            "recomendacao": f"Para {ocasiao.replace('_',' ')}, a nossa escolha principal é o {p_ocasiao}.",
            "idade_perfil": f"Considerando o seu perfil de {idade} anos, o {perfume_idade} é a nossa recomendação especial.",
            "dica": "Aplique nos pontos de pulsação para uma melhor performance da fragrância."
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})
        

        

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
