# PUC Minas

# Trabalho prático Unidade 2 Kubernetes da matéria Conteinerização e Orquestração

# Fork do Jogo de Adivinhação com Flask e React

Este é um divertido jogo de adivinhação no qual você tenta descobrir uma senha gerada aleatoriamente! 
Ele foi desenvolvido com Flask para o backend (servidor) e React para o frontend (interface visual). 
O jogo fornece dicas sobre quantas letras da sua tentativa estão corretas e se elas estão na posição certa.

Original: [Git-FAMS] (https://github.com/fams/guess_game)

## Funcionalidades do Jogo

- 🎲 **Iniciar um novo jogo**: Crie uma partida com uma senha secreta.
- 🔑 **Tentar adivinhar a senha**: Receba dicas sobre quais letras estão corretas e quais estão na posição correta.
- 🔒 **Segurança**: As senhas são protegidas usando codificação base64.
- 🔍 **Dicas**: Ao errar a senha, o jogo fornece sugestões para novas tentativas.


## Pré-requisitos

Para executar o jogo, você precisará de:

- **Docker** v20.10.0 ou mais recente
- **Docker Compose** v3.9 ou mais recente


## Como Rodar o Jogo

1. Clone este repositório:

   ```bash
   git clone https://github.com/fellipedemoraes/kb8-puc.git
   cd kb8-puc

2. Execute o jogo usando Docker Compose:

   ```bash
   docker compose up -d
   ```

3. Abra o jogo em seu navegador: [http://localhost:80](http://localhost:80) 🎮

## Como Jogar

1. Criar um Novo Jogo

Visite: http://localhost:80/maker

Escolha uma senha secreta.

Guarde o game-id que será gerado; você vai precisar dele para jogar.

2. Tentar Adivinhar a Senha

Visite: http://localhost:80/breaker

Insira o game-id que você salvou e comece a adivinhar!

# Estrutura do Projeto e Docker

O jogo é organizado em três serviços principais:

**db:** Banco de dados PostgreSQL para armazenar as informações do jogo.
**backend:** Servidor Flask que gerencia a lógica do jogo.
**frontend:** Servidor Nginx para a interface do jogo (React) e proxy reverso.

#### Serviços:

```yaml
services:
  db:
    image: postgres:14.13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d postgres"]
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backnet
  backend:
    build:
      context: backend
    environment:
      - FLASK_DB_HOST=db
    networks:
      - backnet
      - frontnet
    depends_on:
      db:
        condition: service_healthy
  frontend:
    build:
      context: frontend
    ports:
      - 80:80
    networks:
      - frontnet
```

## Volumes e Redes

**Volúme db-data:** Armazena dados do banco de dados, mantendo-os seguros em caso de reinício do container.
**Redes backnet e frontnet:** Conectam os serviços db-backend e frontend-backend, respectivamente.


- **db**: PostgreSQL, onde as informações do jogo são armazenadas. Ele tem um sistema que verifica se está funcionando corretamente e usa um volume para salvar os dados, mesmo que o container seja reiniciado.

```yml
db:
  image: postgres:14.13
  restart: always
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres -d postgres"]
    interval: 3s
    retries: 5
    start_period: 30s
  secrets:
    - db-password
  volumes:
    - db-data:/var/lib/postgresql/data
  networks:
    - backnet
  environment:
    - POSTGRES_PASSWORD=/run/secrets/db-password
  expose:
    - 5432
```

- **backend**: Flask, a lógica do jogo com comunicação com o Postgres. Ele só começa a funcionar depois que o banco de dados estiver pronto.

```yml
backend:
  build:
    context: backend
  restart: always
  secrets:
    - db-password
  environment:
    - FLASK_DB_PASSWORD=/run/secrets/db-password
    - FLASK_DB_HOST=db
  expose:
    - 5000
  networks:
    - backnet
    - frontnet
  depends_on:
    db:
      condition: service_healthy
```

- **frontend**: É o servidor WEB Nginx, que mostra a interface do jogo (React) e faz a conexão entre o frontend e o backend.

```yml
frontend:
  build:
    context: frontend
  restart: always
  ports:
    - 80:80
  depends_on:
    - backend
  networks:
    - frontnet
```

#### Volumes

O volume `db-data` é usado para garantir que os dados do banco de dados não sejam perdidos, mesmo que o container seja reiniciado.

```yml
volumes:
  db-data:
```

#### Redes

O projeto usa duas redes:

- **backnet**: Conecta o banco de dados ao backend.
- **frontnet**: Conecta o frontend ao backend.

```yml
networks:
  backnet:
  frontnet:
```

#### Balanceamento de Carga

O Nginx, além de servir o frontend, também age como um "mensageiro", encaminhando as requisições do frontend para o backend.

```nginx
upstream backend {
  server backend:5000;
}

server {
  listen 80;

  location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
    try_files $uri $uri/ /index.html;
  }

  location /api {
    proxy_pass http://backend/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

# Kubernetes Deployment Guide

## Introdução

Este repositório contém os manifestos Kubernetes necessários para configurar e implantar a aplicação. Cada componente é configurado de forma modular, seguindo de ConfigMaps, Secrets, e Horizontal Pod Autoscaler (HPA) para escalabilidade automática.

### Estrutura dos Manifestos

- **Backend**: Configuração do serviço de backend da aplicação.
- **Frontend**: Configuração do serviço de frontend da aplicação.
- **PostgreSQL**: Configuração do banco de dados relacional.
- **NGINX**: Configuração do proxy reverso para balanceamento de carga.
- **ConfigMaps e Secrets**: Armazenamento de variáveis de ambiente e dados sensíveis.
- **Horizontal Pod Autoscaler (HPA)**: Escalabilidade automática baseada no uso de CPU.

## Pré-requisitos

- Um cluster Kubernetes funcional.
- `kubectl` configurado e apontando para o cluster correto.
- O **Metrics Server** instalado no cluster para que o HPA funcione corretamente. Caso não esteja instalado, execute o comando abaixo:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### 1. Criar o Namespace

É uma boa prática isolar os recursos em namespaces. Neste caso, todos os recursos serão criados no namespace `ms`.

```bash
kubectl create namespace ms
```

### 1. Marcao o Node que queira subir a aplicação

```bash
kubectl label nodes <nome-do-node> service=microservico
```

### 3. Aplicar ConfigMaps e Secrets

Antes de aplicar os Deployments, é necessário garantir que os **ConfigMaps** e **Secrets** estejam disponíveis, pois eles fornecem variáveis de ambiente e dados sensíveis para os pods.

```bash
kubectl apply -f postgres-configmap.yaml -n ms
kubectl apply -f postgres-secret.yaml -n ms
kubectl apply -f nginx-configmap.yaml -n ms
```

### 4. Criar o Persistent Volume (PV) e Persistent Volume Claim (PVC)

O banco de dados PostgreSQL requer armazenamento persistente. Primeiro, aplique o PV e o PVC.

```bash
kubectl apply -f postgres-pv.yaml -n ms
kubectl apply -f postgres-pvc.yaml -n ms
```

### 5. Aplicar o Deployment e Service do PostgreSQL

Agora que o armazenamento está configurado, aplique o Deployment e o Service do PostgreSQL.

```bash
kubectl apply -f postgres-deploy.yaml -n ms
kubectl apply -f postgres-svc-clusterip.yaml -n ms
```

### 6. Aplicar o Backend

Com o banco de dados disponível, aplique o Deployment e o Service do backend.

```bash
kubectl apply -f backend-deploy.yaml -n ms
kubectl apply -f backend-svc-clusterip.yaml -n ms
```

### 7. Aplicar o Frontend

Agora, aplique o Deployment e o Service do frontend.

```bash
kubectl apply -f frontend-deploy.yaml -n ms
kubectl apply -f frontend-svc-clusterip.yaml -n ms
```

### 8. Aplicar o NGINX

O NGINX atuará como um proxy reverso para o frontend e backend. Aplique o Deployment e o Service do NGINX.

```bash
kubectl apply -f nginx-deploy.yaml -n ms
kubectl apply -f nginx-loadBalancer.yaml -n ms
```

### 9. Aplicar o Horizontal Pod Autoscaler (HPA)

Por fim, aplique o HPA para o backend, garantindo que ele escale automaticamente com base no uso de CPU.

```bash
kubectl apply -f backend-hpa.yaml -n ms
```

## Verificação dos Recursos

Após aplicar todos os manifestos, você pode verificar se os recursos foram criados corretamente usando os seguintes comandos:

### Verificar os Pods

```bash
kubectl get pods -n ms
```

### Verificar os Services

```bash
kubectl get svc -n ms
```

### Verificar os ConfigMaps e Secrets

```bash
kubectl get configmaps -n ms
kubectl get secrets -n ms
```

### Verificar o HPA

```bash
kubectl get hpa -n ms
```

### Verificar o Status dos Deployments

```bash
kubectl get deployments -n ms
```

## Boas Práticas

1. **Versionamento de Imagens**: Sempre utilize tags de versão específicas para as imagens Docker, em vez de `latest`, para garantir que você tenha controle sobre as versões que estão sendo implantadas.
   
2. **Namespaces**: Utilize namespaces para isolar diferentes ambientes (produção, desenvolvimento, etc.) ou diferentes componentes da aplicação.

3. **Gerenciamento de Secrets**: Nunca armazene dados sensíveis diretamente nos manifestos. Utilize o recurso de **Secrets** do Kubernetes para armazenar informações como senhas e chaves de API.

4. **Escalabilidade**: Utilize o **Horizontal Pod Autoscaler (HPA)** para garantir que sua aplicação escale automaticamente com base na demanda de recursos.

5. **Monitoramento**: Certifique-se de que o **Metrics Server** está instalado e funcionando corretamente para que o HPA possa monitorar o uso de CPU e memória ou um pod terceiro como Datadog.

6. **Persistência de Dados**: Para serviços que requerem persistência de dados, como o PostgreSQL, utilize **Persistent Volumes (PV)** e **Persistent Volume Claims (PVC)** para garantir que os dados não sejam perdidos em caso de falha de um pod.

## Troubleshooting

### Verificar Logs de um Pod

Se algum pod não estiver funcionando como esperado, você pode verificar os logs com o seguinte comando:

```bash
kubectl logs <nome-do-pod> -n ms
```

### Descrever um Pod

Para obter mais detalhes sobre o estado de um pod, incluindo eventos e erros, use o comando `describe`:

```bash
kubectl describe pod <nome-do-pod> -n ms
```

### Verificar Eventos do Cluster

Os eventos podem fornecer informações úteis sobre erros e problemas de configuração:

```bash
kubectl get events -n ms
```

# Referências

## PUC Minas
- Site oficial: [PUC Minas](https://www.pucminas.br/)
- Informações sobre cursos e programas de extensão, graduação, pós-graduação e pesquisa.

## Flask
- Site oficial: [Flask](https://flask.palletsprojects.com/)
- Documentação e recursos para desenvolvimento de aplicações web com o micro framework Flask.

## React
- Site oficial: [React](https://react.dev/)
- Biblioteca JavaScript para criar interfaces de usuário, focada em componentes e alta performance.

## Docker
- Site oficial: [Docker](https://www.docker.com/)
- Plataforma para desenvolvimento, envio e execução de aplicações em contêineres, facilitando a portabilidade entre ambientes.

## Docker Compose
- Site oficial: [Docker Compose](https://docs.docker.com/compose/)
- Ferramenta para definir e gerenciar ambientes de aplicações multi-contêineres com um arquivo `docker-compose.yml`.

## Kubernetes
- Site oficial: [Kubernetes](https://kubernetes.io/)
- Sistema open-source para automatizar a implantação, escalonamento e gerenciamento de aplicações em contêineres.


