"""
Script para executar ambos os servidores simultaneamente
"""

import subprocess
import sys
import os
import time

def run_servers():
    """Executa AR e AV em processos separados"""
    
    print("🚀 Iniciando servidores mock...\n")
    
    # Inicia servidor AR
    ar_process = subprocess.Popen(
        [sys.executable, "servers/voter_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    time.sleep(1)
    
    # Inicia servidor AV
    av_process = subprocess.Popen(
        [sys.executable, "servers/voting_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    print("✅ Ambos os servidores iniciados!")
    print("   AR: localhost:9093")
    print("   AV: localhost:9091")
    print("\n⏸️  Pressione Ctrl+C para parar ambos\n")
    
    try:
        # Monitora output de ambos
        while True:
            # Output AR
            line = ar_process.stdout.readline()
            if line:
                print(f"[AR] {line.strip()}")
            
            # Output AV
            line = av_process.stdout.readline()
            if line:
                print(f"[AV] {line.strip()}")
            
            # Verifica se processos terminaram
            if ar_process.poll() is not None or av_process.poll() is not None:
                break
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n⏹️  A parar servidores...")
        ar_process.terminate()
        av_process.terminate()
        ar_process.wait()
        av_process.wait()
        print("✅ Servidores parados")


if __name__ == '__main__':
    run_servers()