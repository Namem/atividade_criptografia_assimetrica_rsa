    # Sistema de Criptografia RSA (Implementação Acadêmica)

Este repositório contém a implementação do algoritmo de criptografia assimétrica **RSA**, desenvolvida como requisito avaliativo da disciplina de **Segurança em Sistemas de Computação**.

O projeto demonstra matematicamente a geração de chaves, cifragem e decifragem, com foco didático na visualização dos dados em formato Hexadecimal e na seleção de primos via Crivo de Eratóstenes.

## 📋 Funcionalidades

O software é uma ferramenta de CLI (Linha de Comando) que realiza:

1.  **Geração de Primos:** Implementação do algoritmo *Crivo de Eratóstenes* para filtrar números primos.
2.  **Par de Chaves RSA:** Cálculo automatizado de:
    * Módulo ($n = p \times q$)
    * Totiente ($\phi(n)$)
    * Chave Pública ($e$) - escolhida aleatoriamente entre coprimos.
    * Chave Privada ($d$) - via Inverso Modular.
3.  **Tratamento de Dados:** Conversão da mensagem de texto para representação **Hexadecimal** antes da cifragem.
4.  **Criptografia/Descriptografia:** Aplicação direta das fórmulas de potência modular:
    * Cifrar: $C = M^e \pmod n$
    * Decifrar: $M = C^d \pmod n$

## 🚀 Como Executar

### Pré-requisitos
* **Python 3.8** ou superior.
* Nenhuma biblioteca externa é necessária (utiliza apenas `math` e `random` nativos).

### Passo a Passo
1.  Clone este repositório:
    ```bash
    git clone [https://github.com/SEU_USUARIO/NOME_DO_REPO.git](https://github.com/SEU_USUARIO/NOME_DO_REPO.git)
    ```
2.  Acesse a pasta do projeto:
    ```bash
    cd NOME_DO_REPO
    ```
3.  Execute o script:
    ```bash
    python rsa_v2.py
    ```

## 🧠 Lógica do Algoritmo

O funcionamento baseia-se na dificuldade computacional de fatorar grandes números inteiros. O fluxo de execução do código segue:

1.  **Crivo:** O sistema gera uma lista de primos até um limite configurado (ex: 1000).
2.  **Seleção:** Dois primos $p$ e $q$ (maiores que 70) são escolhidos para garantir que o módulo $n$ suporte a tabela ASCII.
3.  **Chaves:** O expoente público $e$ é selecionado de uma lista de candidatos coprimos a $\phi(n)$, garantindo variabilidade.
4.  **Conversão:** A entrada "ABC" é convertida para seus valores ASCII (65, 66, 67) e exibida como Hex (0x41, 0x42, 0x43).

## 📸 Exemplo de Execução

```text
========================================
   FERRAMENTA DE CRIPTOGRAFIA RSA 
========================================

[Sistema] Iniciando geração de chaves criptográficas...
 -> Primos escolhidos (via Crivo): p=137, q=229
 -> Módulo n: 31373
 -> Phi(n): 31008

[Sucesso] Chaves Geradas:
 >> Pública (e, n): (53, 31373)
 >> Privada (d, n): (19301, 31373)

[Conversão] Mensagem Original: 'Ola'
[Conversão] Representação Hex:  0x4F 0x6C 0x61

[Criptografia] Resultado (Vetor Cifrado): [28660, 29013, 30372]

[Descriptografia] Mensagem Original Restaurada: 'Ola'