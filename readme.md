# Sistema de Votação Eletrónica - Cliente gRPC

Aplicação cliente Python com interface gráfica para integração com sistema de votação eletrónica baseado em gRPC.

## 📋 Descrição

Este projeto implementa uma aplicação cliente que integra dois serviços gRPC independentes:

1. **Autoridade de Registo (AR)** - Emissão de credenciais de voto
2. **Autoridade de Votação (AV)** - Gestão de candidatos, votação e resultados

A aplicação possui interface gráfica (tkinter) que permite:
- ✅ Registo de eleitores com emissão de credencial
- ✅ Consulta da lista de candidatos
- ✅ Submissão de votos com validação de credencial
- ✅ Visualização de resultados em tempo real

## 🛠️ Tecnologias

- **Python 3.11**
- **gRPC / Protocol Buffers**
- **tkinter** (interface gráfica)

## 📁 Estrutura do Projeto
```
voting-system-grpc/
├── protos/
│   ├── voter.proto          # Definição serviço AR
│   └── voting.proto         # Definição serviço AV
├── generated/               # Código Python gerado (auto-gerado)
├── src/
│   ├── voter_client.py      # Cliente AR
│   ├── voting_client.py     # Cliente AV
│   └── gui_app.py           # Aplicação GUI principal
├── screenshots/             # Capturas de ecrã
├── requirements.txt         # Dependências Python
├── servers/
│   ├── voter_server.py       
│   ├──	voting_server.py 
│	└──	run_both.py        
├── README.md
├── setup.py
└── test_services.py
```
## 🖥️ Servidores Mock (para testes locais)

Este repositório inclui servidores mock Python que simulam a AR e AV para testes locais.

### Executar servidores mock

**Opção 1: Ambos simultaneamente**
```bash
python servers/run_both.py
```

**Opção 2: Separadamente**

Terminal 1 (AR):
```bash
python servers/voter_server.py
```

Terminal 2 (AV):
```bash
python servers/voting_server.py
```

Os servidores ficam disponíveis em:
- AR: `localhost:9093`
- AV: `localhost:9091`


## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- pip (gestor de pacotes Python)

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/codebitenull/voting-system-grpc.git
cd voting-system-grpc
```

### Passo 2: Criar ambiente virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Gerar código Python a partir dos ficheiros .proto
```bash
# Windows
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/voter.proto ./protos/voting.proto

# Linux/Mac
python3 -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/voter.proto ./protos/voting.proto
```

Este comando gera os seguintes ficheiros em `generated/`:
- `voter_pb2.py`
- `voter_pb2_grpc.py`
- `voting_pb2.py`
- `voting_pb2_grpc.py`

### Passo 5: Executar a aplicação

#### Aplicação GUI (principal)
```bash
# Windows
python src\gui_app.py

# Linux/Mac
python3 src/gui_app.py
```

#### Testes individuais dos clientes

**Cliente AR (Autoridade de Registo):**
```bash
python src\voter_client.py
```

**Cliente AV (Autoridade de Votação):**
```bash
python src\voting_client.py
```

## 🔧 Configuração dos Servidores

A aplicação conecta-se aos seguintes endpoints por defeito:

- **Autoridade de Registo:** `localhost:9093`
- **Autoridade de Votação:** `localhost:9091`

Para alterar os endereços, edite os ficheiros em `src/`:
```python
# Exemplo em voter_client.py
client = VoterRegistrationClient(host='localhost', port=9093)
```

## 📝 Testes com grpcurl

### Obter credencial de voto
```bash
grpcurl -insecure -proto protos/voter.proto -d "{\"citizen_card_number\": \"123456789\"}" localhost:9093 voting.VoterRegistrationService/IssueVotingCredential
```

### Obter lista de candidatos
```bash
grpcurl -insecure -proto protos/voting.proto localhost:9091 voting.VotingService/GetCandidates
```

### Submeter voto com credencial válida
```bash
grpcurl -insecure -proto protos/voting.proto -d "{\"voting_credential\": \"CRED-ABC-123\", \"candidate_id\": 1}" localhost:9091 voting.VotingService/Vote
```

### Obter resultados
```bash
grpcurl -insecure -proto protos/voting.proto localhost:9091 voting.VotingService/GetResults
```

## 🎯 Casos de Uso

### CU1: Registar Eleitor
**Descrição:** O eleitor fornece o número do Cartão de Cidadão e recebe uma credencial de voto se for elegível.

**Fluxo:**
1. Inserir número CC
2. Clicar "Obter Credencial de Voto"
3. Sistema contacta AR via gRPC
4. Credencial exibida se eleitor elegível

### CU2: Consultar Candidatos
**Descrição:** Visualizar lista de candidatos disponíveis para votação.

**Fluxo:**
1. Clicar "Carregar Lista de Candidatos"
2. Sistema contacta AV via gRPC
3. Candidatos exibidos como opções de voto

### CU3: Submeter Voto
**Descrição:** Eleitor seleciona candidato e submete voto usando credencial válida.

**Fluxo:**
1. Selecionar candidato
2. Clicar "SUBMETER VOTO"
3. Confirmar escolha
4. Sistema valida credencial e regista voto via gRPC

### CU4: Visualizar Resultados
**Descrição:** Consultar contagem de votos em tempo real.

**Fluxo:**
1. Clicar "Atualizar Resultados"
2. Sistema obtém contagem via gRPC
3. Resultados exibidos em tabela

## ⚠️ Limitações Conhecidas

1. **Mock de credenciais:** O serviço AR emite credenciais válidas apenas 70% das vezes (comportamento de teste)
2. **Credenciais aceites:** Apenas `CRED-ABC-123`, `CRED-DEF-456`, `CRED-GHI-789` são aceites pela AV
3. **Persistência:** Os votos são mantidos em memória - reiniciar o servidor AV apaga os dados
4. **Segurança:** Comunicação sem TLS (desenvolvimento apenas)
5. **Voto único:** Após usar credencial, não é possível votar novamente na mesma sessão

## 📚 Referências

- **Repositório de servidores mock:** https://github.com/arsenioreis/VotingSystem.git
- **Documentação gRPC Python:** https://grpc.io/docs/languages/python/
- **Protocol Buffers (proto3):** https://developers.google.com/protocol-buffers/docs/proto3

## 👤 Autor

Artur Miranda 
Nº al77703 
Mestrado em Engenharia Informática e da Web  
UTAD| 2025-2026

## 📄 Licença

Projeto académico - Integração de Sistemas