# 🛡️ Experimento FHE com Pyfhel: Do BFV ao CKKS

Este projeto demonstra uma comunicação segura entre **cliente** e **servidor** utilizando Criptografia Homomórfica Total (FHE). O objetivo é realizar operações matemáticas em dados sensíveis sem que o servidor jamais tenha acesso aos valores originais.

## 🧐 O que é Criptografia Homomórfica?

Diferente da criptografia comum, onde os dados precisam ser descriptografados para serem processados, a FHE permite realizar cálculos diretamente nos dados cifrados. 

**Exemplo prático:** O cliente envia um salário criptografado; o servidor aplica um bônus de 10% sem saber se o salário é R$ 10,00 ou R$ 10.000,00; o cliente recebe o resultado e, ao abrir com sua chave privada, encontra o valor correto.



## 📁 Estrutura do Projeto

- `cliente.py`: gera o contexto matemático e as chaves (pública e privada). Cifra o salário e descriptografa o resultado final.
- `servidor.py`: atua como o processador "cego". Recebe os bytes, reconstrói o contexto, aplica a lógica de bônus no dado cifrado e devolve o resultado via API (Flask/Waitress).

## 🛠️ Evolução do Projeto: Desafios e Soluções

Durante o desenvolvimento, enfrentamos obstáculos reais que serviram como aprendizado sobre os limites dos esquemas criptográficos:

### 1. O Problema do BFV (Integer Overflow)
Inicialmente, utilizamos o esquema **BFV**, focado em inteiros. 
- **O erro:** Ao aplicar escalas para tratar centavos e multiplicar por 11 (bônus), o valor excedia o limite do "módulo" (o tamanho do balde matemático).
- **Sintoma:** O resultado retornava valores negativos ou aleatórios (ex: `-5.03`) devido ao estouro de inteiro (*wrap-around*).

### 2. A Solução com CKKS (Ponto Flutuante)
A solução definitiva foi a migração para o esquema **CKKS**, projetado para aritmética aproximada de números reais.
- **Resultado:** O CKKS gerencia o "ruído" matemático e a precisão decimal de forma muito mais robusta para cálculos financeiros, garantindo o resultado exato de **5500.00**.
- **Técnica:** Implementamos a **Relinearização**, que mantém o tamanho do dado cifrado estável após multiplicações.



## 🚀 Como executar

### Pré-requisitos
Recomendado usar um ambiente virtual (`python -m venv .venv`).

### Instalação
```bash
pip install Pyfhel flask requests waitress numpy