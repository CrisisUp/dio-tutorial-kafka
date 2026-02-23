import requests
import json
import time
import random

url = "http://localhost:8080/api/salva-pedido"
produtos = ["Mac mini M4", "Monitor Studio Display", "Teclado Mecânico", "Mouse Magic", "AirPods Pro"]

print(f"--- Iniciando Stress Test: 100 Pedidos ---")

for i in range(1, 101):
    data = {
        "id": str(i),
        "nomeProduto": random.choice(produtos),
        "valor": round(random.uniform(500, 15000), 2)
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"[Pedido {i:03}] Enviado com sucesso!")
        else:
            print(f"[Erro] Status: {response.status_code}")
    except Exception as e:
        print(f"Erro de conexão: {e}")
    
    # Pequeno delay para podermos ver o Kafka UI atualizando
    time.sleep(0.05) 

print(f"--- Stress Test Finalizado ---")