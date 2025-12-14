# Testes com grpcurl

Documentação dos testes realizados aos serviços gRPC utilizando grpcurl.

## Pré-requisitos
```bash
# Instalar grpcurl (Mac)
brew install grpcurl

# Servidores devem estar a correr
python servers/run_both.py
```

## Testes Realizados

### 1. Emissão de Credencial de Voto (AR)

**Comando:**
```bash
grpcurl -plaintext -proto protos/voter.proto \
  -d '{"citizen_card_number": "123456787"}' \
  localhost:9093 voting.VoterRegistrationService/IssueVotingCredential
```

**Resultado:**
```json
{
  "isEligible": true,
  "votingCredential": "CRED-DEF-456"
}
```

---

### 2. Obter Lista de Candidatos (AV)

**Comando:**
```bash
grpcurl -plaintext -proto protos/voting.proto \
  localhost:9091 voting.VotingService/GetCandidates
```

**Resultado:**
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "Maria Silva"
    },
    {
      "id": 2,
      "name": "João Santos"
    },
    {
      "id": 3,
      "name": "Ana Costa"
    },
    {
      "id": 4,
      "name": "Pedro Oliveira"
    }
  ]
}
```

---

### 3. Submeter Voto com Credencial Válida (AV)

**Comando:**
```bash
grpcurl -plaintext -proto protos/voting.proto \
  -d '{"voting_credential": "CRED-ABC-123", "candidate_id": 1}' \
  localhost:9091 voting.VotingService/Vote
```

**Resultado:**
```json
{
  "success": true,
  "message": "Voto registado com sucesso em Maria Silva"
}
```

---

### 4. Submeter Voto com Credencial Inválida (AV)

**Comando:**
```bash
grpcurl -plaintext -proto protos/voting.proto \
  -d '{"voting_credential": "INVALID-XXX", "candidate_id": 1}' \
  localhost:9091 voting.VotingService/Vote
```

**Resultado:**
```json
{
  "success": false,
  "message": "Credencial de voto inválida"
}
```

---

### 5. Obter Resultados da Votação (AV)

**Comando:**
```bash
grpcurl -plaintext -proto protos/voting.proto \
  localhost:9091 voting.VotingService/GetResults
```

**Resultado:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Maria Silva",
      "votes": 1
    },
    {
      "id": 2,
      "name": "João Santos",
      "votes": 0
    },
    {
      "id": 3,
      "name": "Ana Costa",
      "votes": 0
    },
    {
      "id": 4,
      "name": "Pedro Oliveira",
      "votes": 0
    }
  ]
}
```

---

## Notas

- Utilizar `-plaintext` para conexões sem TLS (desenvolvimento)
- Os servidores mock devem estar em execução
- Credenciais válidas aceites: `CRED-ABC-123`, `CRED-DEF-456`, `CRED-GHI-789`
- Cada credencial só pode ser usada uma vez