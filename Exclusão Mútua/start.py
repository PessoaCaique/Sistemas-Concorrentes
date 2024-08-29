import subprocess
import time

# Inicia o coordenador em um novo terminal
subprocess.Popen(['start', 'cmd', '/k', 'python coordenador.py'], shell=True)
time.sleep(2)  # Aguarda o coordenador iniciar

# Inicia os processos em ordem aleatória em novos terminais
subprocess.Popen(['start', 'cmd', '/k', 'python processo.py'], shell=True)


