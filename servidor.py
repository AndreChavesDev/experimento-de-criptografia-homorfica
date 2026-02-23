"""Servidor: Realiza operações de ponto flutuante em dados cifrados."""
import base64
from flask import Flask, jsonify, request
from Pyfhel import Pyfhel, PyCtxt
from waitress import serve

app = Flask(__name__)

@app.post("/bonus")
def bonus():
    try:
        data = request.get_json()
        he = Pyfhel()
        he.from_bytes_context(base64.b64decode(data["context"]))
        he.from_bytes_public_key(base64.b64decode(data["public_key"]))
        he.from_bytes_relin_key(base64.b64decode(data["relin_key"]))
        
        cifrado = PyCtxt(pyfhel=he, bytestring=base64.b64decode(data["ciphertext"]))
        
        # Multiplicar por 1.1 (110%) para aplicar os 10% de bônus
        # O CKKS lida com isso de forma muito mais natural que o BFV
        resultado = cifrado * 1.1
        
        return jsonify({
            "ciphertext": base64.b64encode(resultado.to_bytes()).decode()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("Servidor CKKS rodando na porta 5000...")
    serve(app, host='0.0.0.0', port=5000)