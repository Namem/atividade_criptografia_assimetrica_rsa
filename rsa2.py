import random
import math


LIMITE_CRIVO = 1000  
def gerar_crivo_eratostenes(teto_maximo):
    """
    Implementação do Crivo de Eratóstenes para listar primos até 'teto_maximo'.
    Baseado na eliminação progressiva de múltiplos
    """
    # Inicializa lista assumindo que todos são primos (True)
    eh_primo = [True] * (teto_maximo + 1)
    eh_primo[0] = eh_primo[1] = False  # 0 e 1 não são primos

    # Itera de 2 até a raiz quadrada do teto
    for i in range(2, int(math.isqrt(teto_maximo)) + 1):
        if eh_primo[i]:
            # Marca múltiplos de i como False, começando de i*i
            for multiplo in range(i * i, teto_maximo + 1, i):
                eh_primo[multiplo] = False
    
    # Retorna lista de índices que permaneceram True
    lista_primos = [num for num, p in enumerate(eh_primo) if p]
    return lista_primos

def calcular_inverso_modular(e, phi):
    """
    Calcula d tal que (d * e) % phi == 1.
    Utiliza a função nativa pow() que implementa o algoritmo extendido de Euclides.
    """
    try:
        d = pow(e, -1, phi)
        return d
    except ValueError:
        return None

def selecionar_chaves():
    """
    Orquestra a geração de p, q, n, phi, e, d.
    """
    print("\n[Sistema] Iniciando geração de chaves criptográficas...")
    
    # 1. Obter primos via Crivo 
    todos_primos = gerar_crivo_eratostenes(LIMITE_CRIVO)
    
    # Filtra primos muito pequenos para garantir segurança mínima na tabela ASCII
    primos_uteis = [p for p in todos_primos if p > 70]
    
    if len(primos_uteis) < 2:
        raise Exception("Limite do Crivo muito baixo para gerar chaves seguras.")

    # 2. Escolha aleatória de p e q distintos
    p = random.choice(primos_uteis)
    q = random.choice(primos_uteis)
    while p == q:
        q = random.choice(primos_uteis)
    
    print(f" -> Primos escolhidos (via Crivo): p={p}, q={q}")

    # 3. Cálculos de n e totiente (phi) 
    n = p * q
    phi = (p - 1) * (q - 1)
    
    print(f" -> Módulo n: {n}")
    print(f" -> Phi(n): {phi}")

    # 4. Escolha do expoente público 'e'
    # 'e' deve ser coprimo de phi e 1 < e < phi 
    candidatos_e = []
    # Testamos uma faixa para pegar alguns candidatos
    for x in range(3, min(phi, 10000), 2): 
        if math.gcd(x, phi) == 1:
            candidatos_e.append(x)
            # Se já achamos 50 candidatos, paramos para não demorar
            if len(candidatos_e) > 50: break
    
    e = random.choice(candidatos_e) # Escolha aleatória para variar a chave
    
    # 5. Cálculo da chave privada 'd' 
    d = calcular_inverso_modular(e, phi)
    
    print(f"\n[Sucesso] Chaves Geradas:")
    print(f" >> Pública (e, n): ({e}, {n})")
    print(f" >> Privada (d, n): ({d}, {n})")
    
    return {'pub': (e, n), 'priv': (d, n)}

def converter_para_hex(msg_texto):
    """
    Converte string para representação visual Hexadecimal e lista de inteiros.
    Requisito: Exibir representação pré-codificada hexadecimal.
    """
    blocos_numericos = []
    visual_hex = []
    
    for char in msg_texto:
        valor_ascii = ord(char)
        blocos_numericos.append(valor_ascii)
        # Formata como 0xUU
        visual_hex.append(f"0x{valor_ascii:02X}")
        
    print(f"\n[Conversão] Mensagem Original: '{msg_texto}'")
    print(f"[Conversão] Representação Hex:  {' '.join(visual_hex)}")
    
    return blocos_numericos

def cifrar_rsa(lista_msg, chave_publica):
    """
    Aplica C = M^e mod n 
    """
    e, n = chave_publica
    msg_cifrada = []
    
    print("\n[Criptografia] Iniciando processo...")
    for m in lista_msg:
        if m >= n:
            print(f"[Erro] O bloco '{m}' é maior que o módulo n ({n}). Criptografia falhará.")
            return None
        c = pow(m, e, n)
        msg_cifrada.append(c)
        
    print(f"[Criptografia] Resultado (Vetor Cifrado): {msg_cifrada}")
    return msg_cifrada

def decifrar_rsa(lista_cifrada, chave_privada):
    """
    Aplica M = C^d mod n 
    """
    d, n = chave_privada
    msg_decifrada_chars = []
    
    print("\n[Descriptografia] Iniciando processo...")
    for c in lista_cifrada:
        m = pow(c, d, n)
        msg_decifrada_chars.append(chr(m))
        
    texto_final = "".join(msg_decifrada_chars)
    print(f"[Descriptografia] Mensagem Original Restaurada: '{texto_final}'")
    return texto_final

# --- Loop Principal ---
def iniciar_sistema():
    chaves = None
    buffer_cifrado = None
    
    while True:
        print("\n" + "="*40)
        print("   FERRAMENTA DE CRIPTOGRAFIA RSA v2.0")
        print("="*40)
        print("1. [Configuração] Gerar Pares de Chaves")
        print("2. [Operação] Cifrar Mensagem")
        print("3. [Operação] Decifrar Mensagem Atual")
        print("0. Sair")
        
        escolha = input("\nEscolha uma operação: ").strip()
        
        if escolha == '1':
            try:
                chaves = selecionar_chaves()
                buffer_cifrado = None # Limpa buffer anterior ao trocar chaves
            except Exception as err:
                print(f"[Erro Crítico] {err}")
                
        elif escolha == '2':
            if not chaves:
                print("[!] Alerta: Gere as chaves primeiro (Opção 1).")
                continue
            
            texto = input("Digite a mensagem de texto: ")
            # Converte para estrutura numérica (Hex/Int)
            blocos = converter_para_hex(texto)
            # Realiza a cifragem
            buffer_cifrado = cifrar_rsa(blocos, chaves['pub'])
            
        elif escolha == '3':
            if not chaves or not buffer_cifrado:
                print("[!] Nada para decifrar. Cifre algo primeiro.")
                continue
            
            decifrar_rsa(buffer_cifrado, chaves['priv'])
            
        elif escolha == '0':
            print("Encerrando sistema...")
            break
        else:
            print("Opção desconhecida.")

if __name__ == "__main__":
    iniciar_sistema()