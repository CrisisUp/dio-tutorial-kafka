# 🚀 Tutorial: Arquitetura de Eventos Segura com Kafka KRaft e Spring Boot 3

Este guia detalha a modernização de um sistema de microsserviços para mensageria, focado em performance, escalabilidade e segurança de rede.

Este projeto demonstra uma arquitetura de microsserviços baseada em eventos, utilizando Spring Boot 3.2.3 e Apache Kafka em modo KRaft. 

Originalmente desenvolvido para um desafio da DIO em 2021, o sistema foi totalmente modernizado para rodar com Java 21 e arquitetura ARM (Apple M4), eliminando vulnerabilidades de segurança e otimizando a rede.

## 🏗️ 1. Infraestrutura: Kafka em modo KRaft (Docker)

Para rodar o Kafka sem a dependência do Zookeeper, utilizamos o modo KRaft. A configuração do docker-compose.yml foi ajustada para permitir comunicação interna (entre containers) e externa (seu Mac).

### Configuração de Rede (Listeners)

* **CLIENT (9092):** Canal para sua máquina local (Mac) se conectar.

* **INTERNAL (29092):** Canal exclusivo para o Kafka UI e outros containers conversarem entre si.

* **ADVERTISED_LISTENERS:** Essencial para que o Kafka informe aos clientes em qual "ramal" de rede ele está atendendo.

## 🛡️ 2. Segurança e Modernização (Remediação Red Hat)

O projeto original apresentava 31 vulnerabilidades (CVEs) críticas e altas. Realizamos a atualização do núcleo do sistema para zerar esses riscos:

Mudanças no `pom.xml`:

* **Spring Boot:** Atualizado da versão 2.5.5 para 3.2.3.

* **Java:** Configurado para o Java 17/21, aproveitando a arquitetura ARM do chip M4.

* **Lombok:** Atualizado para a versão 1.18.30 para garantir compatibilidade com o compilador moderno.

* **Kafka Client:** Salto da versão 2.7 para 3.6.1, garantindo patches de segurança de rede.

### 🛡️ Remediação de Segurança (CVEs)

O projeto passou por uma auditoria técnica baseada no relatório da Red Hat, onde foram identificadas falhas em versões legadas do Spring e Jackson-databind.

* **Ação:** Upgrade do Spring Boot Parent de 2.5.5 para 3.2.3.

* **Resultado:** Eliminação de 23 vulnerabilidades transitivas no starter-web e 18 vulnerabilidades no spring-kafka.

## 💻 3. Desenvolvimento dos Microsserviços

O fluxo de dados foi dividido em dois componentes principais, ambos utilizando POJOs puros e Generics para facilitar a manutenção.

* **Produtor (tutorial-rest-kafka):** Disponibiliza uma API REST no endpoint /api/salva-pedido.

* **Consumidor (tutorial-microsservico-kafka):** Escuta o tópico SalvarPedido e processa os eventos em tempo real.

## 🧪 4. Teste de Stress e Escalabilidade

Para validar se a rede suporta carga real, utilizamos um script Python que dispara 100 pedidos em milissegundos.

* **Resultados Obtidos:** Escalabilidade Horizontal: Aumentamos o tópico de 1 para 3 partições via Kafka UI.

* **Balanceamento de Carga:** Com múltiplas instâncias do consumidor rodando, o Kafka dividiu os 601 pedidos entre elas automaticamente.

* **Performance:** O tempo de processamento médio foi de aproximadamente 40-50ms por mensagem no Mac mini M4.

## 🛠️ Como rodar este projeto?

### 1. Subir a infra

```Bash
docker-compose up -d
```

### 2. Configurar o Tópico (Obrigatório para Escalabilidade)

Acesse <http://localhost:8090> no seu navegador.

Vá em Topics -> Add a Topic e crie o tópico com o nome SalvarPedido e 3 partições.

### 3. Compilar Apps

```Bash
./mvnw clean compile
```

em ambas as pastas dos microsserviços.

### 4. Iniciar o Produtor (Terminal 1)

```Bash
cd tutorial-rest-kafka
./mvnw spring-boot:run 
```

para iniciar o fluxo.

### 5. Iniciar o Consumidor (Terminal 2)

```Bash
cd tutorial-microsservico-kafka
./mvnw spring-boot:run 
```

para iniciar o fluxo.

### 6. Executar o Teste de Carga (Terminal 3)

```Bash
pip install requests --break-system-packages
python3 stress_test.py
```

 para injetar dados.

Este tutorial reflete as competências adquiridas no segundo ano do curso de Técnico de Redes no SENAI São Caetano, unindo teoria de redes com a prática moderna de DevOps.
