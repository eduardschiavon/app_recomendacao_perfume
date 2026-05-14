import os
import json
import random
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
    # Lógica simplificada de signos
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
        ocasiao_key = dados.get('ocasiao', 'reuniao')
        data_str = dados.get('data_nasc', '').strip()

        # Cálculo de Signo e Idade
        partes = data_str.split('/')
        dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
        if ano < 100: ano += 1900 if ano > 25 else 2000
        hoje = datetime.now()
        idade = hoje.year - ano
        if (hoje.month, hoje.day) < (mes, dia): idade -= 1
        signo = obter_signo(dia, mes)

        # Carrega Bancos
        db_signos = carregar_dados('Jjon_signo_perfume.JSON')
        db_ocasiao = carregar_dados('Jjon_ocasiao_perfume.JSON')
        dataset = carregar_dados('dataset_perfumes.json')

        # Sorteio com fallback
        p_signo = random.choice(db_signos.get(signo, ["Fragrancia Astral"]))
        p_ocasiao = random.choice(db_ocasiao.get(ocasiao_key, ["Fragrancia Momento"]))
        
        # Busca Perfil Etário no Dataset principal
        p_idade = "Uma fragrancia atemporal Schiavon"
        if dataset:
            faixa = [p['Perfume'] for p in dataset if p.get('Idade_Min', 0) <= idade <= p.get('Idade_Max', 100)]
            if faixa: p_idade = random.choice(faixa)

        return jsonify({
            "status": "sucesso",
            "identidade": f"Sua aura de {signo.capitalize()} harmoniza com o {p_signo}.",
            "recomendacao": f"Para sua ocasiao de {ocasiao_key.replace('_',' ')}, sugerimos o {p_ocasiao}.",
            "idade_perfil": f"Para seu perfil de {idade} anos, o {p_idade} e nossa escolha especial."
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})

@app.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('termo', '').lower().strip()
    dataset = carregar_dados('dataset_perfumes.json')
    if not dataset or not termo: return jsonify({"resultado": "Digite um termo para busca."})

    for p in dataset:
        # Busca em todos os campos para o efeito "UAU"
        campos = [
            str(p.get('Perfume', '')),
            str(p.get('Marca', '')),
            str(p.get('Familia_Olfativa', '')),
            str(p.get('Ingrediente_Assinatura', '')),
            " ".join(p.get('Buscas', []))
        ]
        
        if any(termo in c.lower() for c in campos):
            return jsonify({
                "resultado": f"✨ <strong>{p['Perfume']}</strong> ({p['Marca']})<br>" +
                             f"💎 Estilo: {p['Familia_Olfativa']}<br>" +
                             f"🌿 Notas: {p['Ingrediente_Assinatura']}<br>" +
                             f"⭐ Avaliação: {p['Estrelas']} estrelas"
            })
            
    return jsonify({"resultado": "Nao encontramos essa nota no acervo Schiavon ainda."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
