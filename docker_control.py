import subprocess

def start_docker():
    subprocess.run(["docker-compose", "up", "-d"], check = True)