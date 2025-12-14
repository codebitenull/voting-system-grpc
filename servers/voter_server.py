"""
Servidor mock da Autoridade de Registo (AR)
Simula emissão de credenciais de voto
"""

from concurrent import futures
import grpc
import sys
import os
import random

# Adiciona path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from generated import voter_pb2
from generated import voter_pb2_grpc


class VoterRegistrationService(voter_pb2_grpc.VoterRegistrationServiceServicer):
    """Implementação do serviço de registo"""
    
    def __init__(self):
        # Credenciais válidas (70% de probabilidade)
        self.valid_credentials = [
            "CRED-ABC-123",
            "CRED-DEF-456", 
            "CRED-GHI-789"
        ]
        self.used_credentials = set()
    
    def IssueVotingCredential(self, request, context):
        """Emite credencial de voto"""
        
        cc_number = request.citizen_card_number
        print(f"📋 Pedido de credencial para CC: {cc_number}")
        
        # 70% chance de credencial válida
        if random.random() < 0.7:
            # Escolhe credencial válida não usada
            available = [c for c in self.valid_credentials if c not in self.used_credentials]
            
            if available:
                credential = random.choice(available)
                self.used_credentials.add(credential)
                is_eligible = True
                print(f"   ✅ Credencial válida emitida: {credential}")
            else:
                # Todas já foram usadas, gera nova
                credential = f"CRED-{random.randint(100,999)}-{random.randint(100,999)}"
                is_eligible = True
                print(f"   ✅ Nova credencial gerada: {credential}")
        else:
            # Credencial inválida
            credential = f"INVALID-{random.randint(1000,9999):04X}"
            is_eligible = False
            print(f"   ⚠️  Credencial inválida: {credential}")
        
        return voter_pb2.VoterResponse(
            is_eligible=is_eligible,
            voting_credential=credential
        )


def serve():
    """Inicia o servidor"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    voter_pb2_grpc.add_VoterRegistrationServiceServicer_to_server(
        VoterRegistrationService(), server
    )
    
    server.add_insecure_port('[::]:9093')
    server.start()
    
    print("🚀 Servidor AR (Autoridade de Registo) iniciado")
    print("   Porta: 9093")
    print("   Pressione Ctrl+C para parar\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n⏹️  Servidor parado")
        server.stop(0)


if __name__ == '__main__':
    serve()