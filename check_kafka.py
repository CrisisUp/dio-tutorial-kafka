import socket
import time

def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

if __name__ == "__main__":
    host = "127.0.0.1"
    # Ajuste: Removido Zookeeper e mantido apenas o Kafka (Broker)
    # Adicionei a porta 9093 caso queira validar o Controller do KRaft
    ports = {"Kafka Broker": 9092}
    
    print(f"--- Iniciando Verificação de Infraestrutura (Modo KRaft) ---")
    for service, port in ports.items():
        if check_port(host, port):
            print(f"[OK] {service} está respondendo na porta {port}.")
        else:
            print(f"[ERRO] {service} NÃO está acessível na porta {port}. Verifique se o container subiu.")