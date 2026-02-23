"""Cliente: Usa o esquema CKKS para lidar com números reais e precisão decimal."""
from __future__ import annotations
import base64
import numpy as np
import requests
from Pyfhel import Pyfhel, PyCtxt

class ClienteFHE:
    def __init__(self):
        self.he = Pyfhel()
        # CKKS: esquema ideal para números reais (float).
        # m=8192, qi=40, bitsScale=40: configuração de alta precisão.
        self.he.contextGen(scheme="ckks", n=8192, scale=2**40, qi_sizes=[60, 40, 40, 60])
        self.he.keyGen()
        self.he.relinKeyGen() # Necessário para multiplicações no CKKS

    def criptografar(self, valor: float) -> PyCtxt:
        # CKKS aceita floats diretamente via encodeFrac
        ptxt = self.he.encodeFrac(np.array([valor], dtype=np.float64))
        return self.he.encryptPtxt(ptxt)

    def descriptografar(self, cifrado: PyCtxt) -> float:
        res = self.he.decryptFrac(cifrado)
        return float(res[0])

    def obter_payload(self, cifrado: PyCtxt) -> dict:
        return {
            "context": base64.b64encode(self.he.to_bytes_context()).decode(),
            "public_key": base64.b64encode(self.he.to_bytes_public_key()).decode(),
            "relin_key": base64.b64encode(self.he.to_bytes_relin_key()).decode(),
            "ciphertext": base64.b64encode(cifrado.to_bytes()).decode(),
        }

def main():
    c = ClienteFHE()
    salario = 5000.0
    print(f"Cliente: Enviando salário original: {salario:.2f}")

    cifrado = c.criptografar(salario)
    payload = c.obter_payload(cifrado)

    try:
        r = requests.post("http://localhost:5000/bonus", json=payload, timeout=15)
        r.raise_for_status()
        
        res_bytes = base64.b64decode(r.json()["ciphertext"])
        res_cifrado = PyCtxt(pyfhel=c.he, bytestring=res_bytes)
        
        resultado = c.descriptografar(res_cifrado)
        print(f"Cliente: Resultado Final (Com 10% bônus): {resultado:.2f}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()