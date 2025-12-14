"""
Cliente gRPC para Autoridade de Registo (AR)
Serviço: VoterRegistrationService
"""

import grpc
import sys
import os

# Adiciona o diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from generated import voter_pb2
from generated import voter_pb2_grpc


class VoterRegistrationClient:
    """Cliente para o serviço de registo de eleitores"""
    
    def __init__(self, host='localhost', port=9093):
        """
        Inicializa o cliente gRPC
        
        Args:
            host: Endereço do servidor (default: localhost)
            port: Porta do servidor (default: 9093)
        """
        self.address = f'{host}:{port}'
        self.channel = None
        self.stub = None
    
    def connect(self):
        """Estabelece conexão com o servidor"""
        # Cria canal inseguro (sem TLS) para desenvolvimento
        self.channel = grpc.insecure_channel(self.address)
        self.stub = voter_pb2_grpc.VoterRegistrationServiceStub(self.channel)
        print(f"✓ Conectado ao serviço de registo em {self.address}")
    
    def disconnect(self):
        """Fecha a conexão"""
        if self.channel:
            self.channel.close()
            print("✓ Desconectado do serviço de registo")
    
    def issue_voting_credential(self, citizen_card_number):
        """
        Solicita credencial de voto
        
        Args:
            citizen_card_number: Número do cartão de cidadão
            
        Returns:
            tuple: (is_eligible, voting_credential)
        """
        try:
            # Cria o pedido
            request = voter_pb2.VoterRequest(
                citizen_card_number=citizen_card_number
            )
            
            # Faz a chamada gRPC
            response = self.stub.IssueVotingCredential(request)
            
            return response.is_eligible, response.voting_credential
            
        except grpc.RpcError as e:
            print(f"✗ Erro gRPC: {e.code()}: {e.details()}")
            return False, None


def main():
    """Função de teste do cliente"""
    print("=== Cliente de Registo de Eleitores ===\n")
    
    # Cria e conecta cliente
    client = VoterRegistrationClient()
    client.connect()
    
    # Testa com alguns números de CC
    test_cards = ["123456789", "987654321", "111222333"]
    
    for cc in test_cards:
        print(f"\n📋 Testando CC: {cc}")
        is_eligible, credential = client.issue_voting_credential(cc)
        
        if is_eligible:
            print(f"   ✓ Elegível! Credencial: {credential}")
        else:
            print(f"   ✗ Não elegível. Credencial inválida: {credential}")
    
    # Desconecta
    client.disconnect()


if __name__ == "__main__":
    main()