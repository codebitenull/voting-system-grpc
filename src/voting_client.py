"""
Cliente gRPC para Autoridade de Votação (AV)
Serviço: VotingService
"""

import grpc
import sys
import os

# Adiciona o diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from generated import voting_pb2
from generated import voting_pb2_grpc


class VotingClient:
    """Cliente para o serviço de votação"""
    
    def __init__(self, host='localhost', port=9091):
        """
        Inicializa o cliente gRPC
        
        Args:
            host: Endereço do servidor (default: localhost)
            port: Porta do servidor (default: 9091)
        """
        self.address = f'{host}:{port}'
        self.channel = None
        self.stub = None
    
    def connect(self):
        """Estabelece conexão com o servidor"""
        self.channel = grpc.insecure_channel(self.address)
        self.stub = voting_pb2_grpc.VotingServiceStub(self.channel)
        print(f"✓ Conectado ao serviço de votação em {self.address}")
    
    def disconnect(self):
        """Fecha a conexão"""
        if self.channel:
            self.channel.close()
            print("✓ Desconectado do serviço de votação")
    
    def get_candidates(self):
        """
        Obtém lista de candidatos
        
        Returns:
            list: Lista de tuplas (id, name)
        """
        try:
            request = voting_pb2.GetCandidatesRequest()
            response = self.stub.GetCandidates(request)
            
            candidates = [(c.id, c.name) for c in response.candidates]
            return candidates
            
        except grpc.RpcError as e:
            print(f"✗ Erro gRPC: {e.code()}: {e.details()}")
            return []
    
    def vote(self, voting_credential, candidate_id):
        """
        Submete um voto
        
        Args:
            voting_credential: Credencial de voto obtida da AR
            candidate_id: ID do candidato
            
        Returns:
            tuple: (success, message)
        """
        try:
            request = voting_pb2.VoteRequest(
                voting_credential=voting_credential,
                candidate_id=candidate_id
            )
            
            response = self.stub.Vote(request)
            return response.success, response.message
            
        except grpc.RpcError as e:
            print(f"✗ Erro gRPC: {e.code()}: {e.details()}")
            return False, str(e.details())
    
    def get_results(self):
        """
        Obtém resultados da votação
        
        Returns:
            list: Lista de tuplas (id, name, votes)
        """
        try:
            request = voting_pb2.GetResultsRequest()
            response = self.stub.GetResults(request)
            
            results = [(r.id, r.name, r.votes) for r in response.results]
            return results
            
        except grpc.RpcError as e:
            print(f"✗ Erro gRPC: {e.code()}: {e.details()}")
            return []


def main():
    """Função de teste do cliente"""
    print("=== Cliente de Votação ===\n")
    
    # Cria e conecta cliente
    client = VotingClient()
    client.connect()
    
    # 1. Obtém candidatos
    print("\n📋 Lista de Candidatos:")
    candidates = client.get_candidates()
    for cid, name in candidates:
        print(f"   [{cid}] {name}")
    
    # 2. Testa votação com credencial válida
    print("\n🗳️  Testando voto com credencial válida:")
    success, msg = client.vote("CRED-ABC-123", 1)
    print(f"   {'✓' if success else '✗'} {msg}")
    
    # 3. Testa votação com credencial inválida
    print("\n🗳️  Testando voto com credencial inválida:")
    success, msg = client.vote("INVALID-123", 1)
    print(f"   {'✓' if success else '✗'} {msg}")
    
    # 4. Obtém resultados
    print("\n📊 Resultados:")
    results = client.get_results()
    for cid, name, votes in results:
        print(f"   [{cid}] {name}: {votes} votos")
    
    # Desconecta
    client.disconnect()


if __name__ == "__main__":
    main()