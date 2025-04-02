from http.client import responses

from flask import Flask, jsonify, request
import pandas as pd
from fuzzywuzzy import fuzz, process
import re
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS (app,origins=["http://localhost:8080"],supports_credentials=True)

df = pd.read_csv('dados.csv', sep=';', encoding='utf-8')

df['search_text'] = df.apply(lambda row: ' '.join([
    str(row['Razao_Social']),
    str(row['Nome_Fantasia']),
    str(row['Cidade']),
    str(row['UF']),
    str(row['Modalidade'])
]).lower(), axis=1)

@app.route('/busca', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('q', '').lower()
    if not termo:
        return jsonify({"error": "Parâmetro 'q' é obrigatório"}), 400

    limite = int(request.args.get('limit', 10))

    def calcular_relevancia(texto):

        if termo in texto:
            return 100
        return fuzz.partial_ratio(termo, texto)

    df['relevancia'] = df['search_text'].apply(calcular_relevancia)

    resultados = df[df['relevancia'] > 50].sort_values('relevancia', ascending=False).head(limite)

    response = {
        "termo_busca": termo,
        "total_resultados": len(resultados),
        "resultados": resultados.drop(columns=['search_text', 'relevancia']).replace({np.nan: None}).to_dict(
            orient='records')
    }
    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)