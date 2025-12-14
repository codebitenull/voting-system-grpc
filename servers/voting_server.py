"""
Servidor mock da Autoridade de Votação (AV)
Simula votação e contagem de votos
"""

from concurrent import futures
import grpc
import sys
import os

# Adiciona path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from generated import voting_pb2
from generated import voting_pb2_grpc


class VotingService(voting_pb2_grpc.VotingServiceServicer):
    """Implementação do serviço de votação"""
    
    def __init__(self):
        # Candidatos
        self.candidates = [
            (1, "Maria Silva"),
            (2, "João Santos"),
            (3, "Ana Costa"),
            (4, "Pedro Oliveira")
        ]
        
        # Credenciais válidas aceites
        self.valid_credentials = {
            "CRED-ABC-123",
            "CRED-DEF-456",
            "CRED-GHI-789"
        }
        
        # Credenciais já usadas
        self.used_credentials = set()
        
        # Contagem de votos
        self.votes = {cid: 0 for cid, _ in self.candidates}
    
    def GetCandidates(self, request, context):
        """Retorna lista de candidatos"""
        print("📋 Pedido de lista de candidatos")
        
        candidates = [
            voting_pb2.Candidate(id=cid, name=name)
            for cid, name in self.candidates
        ]
        
        print(f"   ✅ Enviando {len(candidates)} candidatos")
        
        return voting_pb2.GetCandidatesResponse(candidates=candidates)
    
    def Vote(self, request, context):
        """Processa um voto"""
        credential = request.voting_credential
        candidate_id = request.candidate_id
        
        print(f"🗳️  Pedido de voto:")
        print(f"   Credencial: {credential}")
        print(f"   Candidato: {candidate_id}")
        
        # Valida credencial
        if credential not in self.valid_credentials:
            # Aceita também credenciais que começam com CRED-
            if not credential.startswith("CRED-"):
                print(f"   ❌ Credencial inválida")
                return voting_pb2.VoteResponse(
                    success=False,
                    message="Credencial de voto inválida"
                )
        
        # Verifica se já foi usada
        if credential in self.used_credentials:
            print(f"   ❌ Credencial já utilizada")
            return voting_pb2.VoteResponse(
                success=False,
                message="Esta credencial já foi utilizada"
            )
        
        # Valida candidato
        if candidate_id not in self.votes:
            print(f"   ❌ Candidato inválido")
            return voting_pb2.VoteResponse(
                success=False,
                message="Candidato inexistente"
            )
        
        # Regista voto
        self.used_credentials.add(credential)
        self.votes[candidate_id] += 1
        
        candidate_name = next(name for cid, name in self.candidates if cid == candidate_id)
        print(f"   ✅ Voto registado para {candidate_name}")
        
        return voting_pb2.VoteResponse(
            success=True,
            message=f"Voto registado com sucesso em {candidate_name}"
        )
    
    def GetResults(self, request, context):
        """Retorna resultados da votação"""
        print("📊 Pedido de resultados")
        
        results = [
            voting_pb2.CandidateResult(id=cid, name=name, votes=self.votes[cid])
            for cid, name in self.candidates
        ]
        
        total = sum(self.votes.values())
        print(f"   ✅ Total de votos: {total}")
        
        return voting_pb2.GetResultsResponse(results=results)


def serve():
    """Inicia o servidor"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    voting_pb2_grpc.add_VotingServiceServicer_to_server(
        VotingService(), server
    )
    
    server.add_insecure_port('[::]:9091')
    server.start()
    
    print("🚀 Servidor AV (Autoridade de Votação) iniciado")
    print("   Porta: 9091")
    print("   Pressione Ctrl+C para parar\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n⏹️  Servidor parado")
        server.stop(0)


if __name__ == '__main__':
    serve()