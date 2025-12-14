"""
Script de setup para gerar código gRPC
Facilita a geração dos ficheiros Python a partir dos .proto
"""

import subprocess
import sys
import os

def fix_imports():
    """Corrige imports nos ficheiros gerados"""
    
    print("\n🔧 Corrigindo imports...")
    
    fixes = [
        ('generated/voter_pb2_grpc.py', 'import voter_pb2', 'from generated import voter_pb2'),
        ('generated/voting_pb2_grpc.py', 'import voting_pb2', 'from generated import voting_pb2')
    ]
    
    for filepath, old, new in fixes:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            
            if old in content:
                content = content.replace(old, new)
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"   ✅ {filepath}")

def generate_grpc_code():
    """Gera código Python a partir dos ficheiros .proto"""
    
    print("🔧 Gerando código gRPC a partir dos ficheiros .proto...\n")
    
    # Verifica se grpcio-tools está instalado
    try:
        import grpc_tools
    except ImportError:
        print("❌ grpcio-tools não está instalado!")
        print("   Execute: pip install grpcio-tools\n")
        sys.exit(1)
    
    # Cria diretório generated se não existir
    os.makedirs("generated", exist_ok=True)
    
    # Cria __init__.py
    with open("generated/__init__.py", "w") as f:
        f.write("# Código gerado automaticamente\n")
    
    # Comando para gerar código
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        "-I./protos",
        "--python_out=./generated",
        "--grpc_python_out=./generated",
        "./protos/voter.proto",
        "./protos/voting.proto"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Código gerado com sucesso!")
        print("\nFicheiros criados em generated/:")
        print("   - voter_pb2.py")
        print("   - voter_pb2_grpc.py")
        print("   - voting_pb2.py")
        print("   - voting_pb2_grpc.py")
        
        # Corrige imports automaticamente
        fix_imports()
        
        print("\n✨ Setup completo! Pode executar a aplicação.\n")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar código: {e}")
        print(f"   Output: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    generate_grpc_code()