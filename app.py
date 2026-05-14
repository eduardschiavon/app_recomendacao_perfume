import os
import json
import random # Importante para variar as recomendações
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

@app.route('/selecao', methods=['POST'])
def gerar_selecao():
    try:
        dados = request.json
        cidade = dados.get('cidade', 'nao informada')
        ocasiao = dados.get('ocasiao', 'dia_a_dia').lower()
        data_str = dados.get('data_nasc', '').strip()

        # Cálculo de idade e signo (mesma lógica anterior)
        partes = data_str.split('/')
        dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
        if ano < 100: ano += 1900 if ano > 25 else 2000
        hoje = datetime.now()
        idade = hoje.year - ano
        
        # Carregar bancos
        db_signos = carregar_dados('Jjon_signo_perfume.JSON')
        db_ocasiao = carregar_dados('Jjon_ocasiao_perfume.JSON')

        # SORTEIO ALEATÓRIO: Agora ele escolhe qualquer um da lista!
        lista_signo = db_signos.get("peixes", ["Kenzo Amour"]) # Fallback para peixes como exemplo
        p_signo = random.choice(lista_signo) 

        lista_ocasiao = db_ocasiao.get(ocasiao, ["Fragrancia Especial"])
        p_ocasiao = random.choice(lista_ocasiao)

        return jsonify({
            "status": "sucesso",
            "mensagem": f"Selecao preparada para cliente em {cidade}.",
            "identidade": f"Sua assinatura astral sugere {p_signo}.",
            "recomendacao": f"Para {ocasiao}, sugerimos o {p_ocasiao}.",
            "idade_perfil": f"Com {idade} anos, o Lily EDP e sua recomendacao especial.",
            "dica": "Aplique nos pontos de pulsacao."
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})

@app.route('/buscar', methods=['GET'])
def buscar():
    # Transformamos o termo da busca em minúsculo e removemos espaços
    termo = request.args.get('termo', '').lower().strip()
    dataset = carregar_dados('dataset_perfumes.json')
    
    if not dataset:
        return jsonify({"resultado": "Catalogo indisponivel."})
    
    resultados_encontrados = []

    for p in dataset:
        # Verificamos nome e notas ignorando maiúsculas/minúsculas
        nome_perfume = p.get('Perfume', '').lower()
        notas_perfume = p.get('Notas', '').lower()
        
        if termo in nome_perfume or termo in notas_perfume:
            resultados_encontrados.append(p['Perfume'])

    if resultados_encontrados:
        # Retorna o primeiro encontrado ou uma lista
        return jsonify({"resultado": f"Encontramos: {', '.join(resultados_encontrados[:2])}"})
    
    return jsonify({"resultado": "Fragrancia nao encontrada no catalogo atual."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
