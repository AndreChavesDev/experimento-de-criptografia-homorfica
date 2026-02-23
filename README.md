# 🛡️ Experimento FHE com Pyfhel: Do BFV ao CKKS

Este projeto demonstra uma implementação prática de **Criptografia Homomórfica Total (FHE)** para comunicação segura entre um ambiente cliente e um servidor. O objetivo principal é permitir que um servidor processe cálculos matemáticos em dados sensíveis sem nunca ter acesso aos valores originais (em texto claro).

---

## 🧐 O que é Criptografia Homomórfica?

Diferente da criptografia convencional, onde os dados devem ser descriptografados para processamento (expondo-os), a **FHE (Fully Homomorphic Encryption)** permite realizar operações aritméticas diretamente sobre o texto cifrado.

> **Exemplo Prático deste Projeto:**
> 1. **Cliente:** Cifra seu salário (ex: R$ 5.000,00) com uma chave pública.
> 2. **Servidor:** Recebe o dado cifrado e aplica um bônus de 10% (multiplicação por 1.1) "no escuro".
> 3. **Cliente:** Recebe o resultado ainda criptografado, usa sua chave privada para abrir e encontra o valor correto: **R$ 5.500,00**.

---

## 🛠️ Evolução do Projeto: Desafios e Soluções

Abaixo, descrevo a jornada técnica e as lições aprendidas ao lidar com as limitações dos esquemas criptográficos:

### 1. O Problema do BFV (Integer Overflow)
Inicialmente, utilizei o esquema **BFV**, focado em aritmética de números inteiros.
* **O Erro:** Ao tentar tratar centavos (aplicando escalas) e multiplicar por fatores de bônus, o valor excedia o **limite do módulo** (o "tamanho do balde" matemático definido no contexto).
* **Sintoma:** O resultado retornava valores negativos ou aleatórios (ex: `-5.03`) devido ao fenômeno de *wrap-around* (estouro de inteiro).

### 2. A Solução com CKKS (Ponto Flutuante)
A migração para o esquema **CKKS** foi o ponto de virada, pois ele é projetado para aritmética aproximada de números reais.
* **Resultado:** O CKKS gerencia o "ruído" matemático e a precisão decimal de forma robusta para cálculos financeiros.
* **Técnica de Relinearização:** Implementamos a relinearização para manter o tamanho do dado cifrado estável após multiplicações, evitando que o crescimento do polinômio inviabilizasse o processamento.

---

## 📁 Estrutura do Projeto

| Arquivo | Função |
| :--- | :--- |
| `cliente.py` | Gera o contexto matemático, chaves (pública/privada), cifra o dado inicial e descriptografa o resultado final. |
| `servidor.py` | Atua como o processador "cego". Reconstrói o contexto através dos bytes recebidos, aplica a lógica de bônus via API (Flask/Waitress) e devolve o dado cifrado. |

---

## 💡 Casos de Uso Reais da FHE

* **Finanças:** Análise preditiva e detecção de fraudes em modelos de ML sem expor dados confidenciais de transações.
* **Saúde:** Processamento de dados genômicos e clínicos em nuvem mantendo a conformidade com leis de privacidade (LGPD/GDPR).
* **Varejo:** Insights sobre comportamento do consumidor sem comprometer a identidade ou histórico de compras individual.

---

## 🚀 Como Executar no VS Code

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.8+** instalado. Recomenda-se o uso de um ambiente virtual para manter as dependências isoladas.

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar no Windows (Prompt/PowerShell)
.venv\Scripts\activate

# Ativar no Linux/Mac
source .venv/bin/activate
