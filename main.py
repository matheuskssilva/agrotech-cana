import json
import os

ARQUIVO = "banco_dados.json"

# =========================
# BANCO (JSON)
# =========================

def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)

# =========================
# VALIDAÇÃO
# =========================

def validar_numero(valor):
    try:
        num = float(valor)
        if num < 0:
            return None
        return num
    except:
        return None

# =========================
# FUNÇÕES PRINCIPAIS
# =========================

def registrar_colheita():
    print("\n=== REGISTRO DE COLHEITA ===")

    area = validar_numero(input("Área (hectares): "))
    producao = validar_numero(input("Produção (toneladas): "))
    tipo = input("Tipo (manual/mecanizada): ").lower()

    if area is None or producao is None or tipo not in ["manual", "mecanizada"]:
        print("❌ Dados inválidos!")
        return

    perda_percentual = 5 if tipo == "manual" else 15
    perda = producao * (perda_percentual / 100)

    registro = {
        "area": area,
        "producao": producao,
        "tipo": tipo,
        "perda_percentual": perda_percentual,
        "perda_ton": perda
    }

    dados = carregar_dados()
    dados.append(registro)
    salvar_dados(dados)

    print(f"✅ Registro salvo!")
    print(f"Perda estimada: {perda:.2f} toneladas")

# =========================

def listar_dados():
    print("\n=== HISTÓRICO ===")

    dados = carregar_dados()

    if not dados:
        print("Nenhum registro encontrado.")
        return

    for i, d in enumerate(dados, 1):
        print(f"\nRegistro {i}")
        print(f"Área: {d['area']} ha")
        print(f"Produção: {d['producao']} ton")
        print(f"Tipo: {d['tipo']}")
        print(f"Perda: {d['perda_ton']:.2f} ton ({d['perda_percentual']}%)")

# =========================

def analise_geral():
    dados = carregar_dados()

    if not dados:
        print("Sem dados para análise.")
        return

    total_producao = sum(d["producao"] for d in dados)
    total_perda = sum(d["perda_ton"] for d in dados)

    eficiencia = ((total_producao - total_perda) / total_producao) * 100

    print("\n=== ANÁLISE GERAL ===")
    print(f"Produção total: {total_producao:.2f} ton")
    print(f"Perda total: {total_perda:.2f} ton")
    print(f"Eficiência: {eficiencia:.2f}%")

    if eficiencia < 85:
        print("⚠️ Recomendação: Melhorar o processo de colheita.")
    else:
        print("✅ Boa eficiência!")

# =========================

def analise_detalhada():
    dados = carregar_dados()

    if not dados:
        print("Sem dados.")
        return

    producoes = [d["producao"] for d in dados]
    perdas = [d["perda_ton"] for d in dados]

    print("\n=== ANÁLISE DETALHADA ===")
    print(f"Média produção: {sum(producoes)/len(producoes):.2f}")
    print(f"Média perdas: {sum(perdas)/len(perdas):.2f}")
    print(f"Maior produção: {max(producoes):.2f}")
    print(f"Menor produção: {min(producoes):.2f}")

# =========================
# MENU
# =========================

def menu():
    while True:
        print("\n==============================")
        print("🌱 SISTEMA AGROTECH CANA")
        print("==============================")
        print("1 - Registrar colheita")
        print("2 - Ver histórico")
        print("3 - Análise geral")
        print("4 - Análise detalhada")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            registrar_colheita()
        elif op == "2":
            listar_dados()
        elif op == "3":
            analise_geral()
        elif op == "4":
            analise_detalhada()
        elif op == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()