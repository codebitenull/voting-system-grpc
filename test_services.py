"""
Script de teste rápido dos serviços gRPC
Verifica se os servidores AR e AV estão acessíveis
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.voter_client import VoterRegistrationClient
from src.voting_client import VotingClient


def test_voter_service():
    """Testa serviço de registo"""
    print("\n" + "="*60)
    print("TESTE: Autoridade de Registo (AR)")
    print("="*60)
    
    try:
        client = VoterRegistrationClient()
        client.connect()
        
        # Testa emissão de credencial
        print("\n📋 Testando emissão de credencial...")
        is_eligible, credential = client.issue_voting_credential("123456789")
        
        if is_eligible:
            print(f"   ✅ SUCESSO - Credencial: {credential}")
        else:
            print(f"   ⚠️  Credencial inválida recebida: {credential}")
        
        client.disconnect()
        return True
        
    except Exception as e:
        print(f"   ❌ FALHA - {str(e)}")
        return False


def test_voting_service():
    """Testa serviço de votação"""
    print("\n" + "="*60)
    print("TESTE: Autoridade de Votação (AV)")
    print("="*60)
    
    try:
        client = VotingClient()
        client.connect()
        
        # 1. Testa obter candidatos
        print("\n📋 Testando GetCandidates...")
        candidates = client.get_candidates()
        if candidates:
            print(f"   ✅ SUCESSO - {len(candidates)} candidatos:")
            for cid, name in candidates:
                print(f"      [{cid}] {name}")
        else:
            print("   ❌ FALHA - Nenhum candidato retornado")
        
        # 2. Testa votar (credencial válida)
        print("\n🗳️  Testando Vote (credencial válida)...")
        success, msg = client.vote("CRED-ABC-123", 1)
        if success:
            print(f"   ✅ SUCESSO - {msg}")
        else:
            print(f"   ⚠️  {msg}")
        
        # 3. Testa votar (credencial inválida)
        print("\n🗳️  Testando Vote (credencial inválida)...")
        success, msg = client.vote("INVALID-XXX", 1)
        if not success:
            print(f"   ✅ SUCESSO - Credencial rejeitada como esperado")
        else:
            print(f"   ❌ FALHA - Credencial inválida foi aceite!")
        
        # 4. Testa resultados
        print("\n📊 Testando GetResults...")
        results = client.get_results()
        if results is not None:
            print(f"   ✅ SUCESSO - Resultados obtidos:")
            for cid, name, votes in results:
                print(f"      [{cid}] {name}: {votes} votos")
        else:
            print("   ❌ FALHA - Erro ao obter resultados")
        
        client.disconnect()
        return True
        
    except Exception as e:
        print(f"   ❌ FALHA - {str(e)}")
        return False


def main():
    """Executa todos os testes"""
    print("\n🧪 TESTES DE INTEGRAÇÃO - SISTEMA DE VOTAÇÃO")
    print("=" * 60)
    
    # Testa AR
    ar_ok = test_voter_service()
    
    # Testa AV
    av_ok = test_voting_service()
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    print(f"Autoridade de Registo (AR): {'✅ OK' if ar_ok else '❌ FALHOU'}")
    print(f"Autoridade de Votação (AV): {'✅ OK' if av_ok else '❌ FALHOU'}")
    print("="*60 + "\n")
    
    if ar_ok and av_ok:
        print("✨ Todos os testes passaram! Sistema pronto para uso.\n")
        return 0
    else:
        print("⚠️  Alguns testes falharam. Verifique se os servidores estão a correr.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())