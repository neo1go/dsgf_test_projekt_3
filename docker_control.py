import subprocess
import docker 

client = docker.from_env()

def start_docker():
    subprocess.run(["docker-compose", "up", "-d"], check = True)
    
# Container wird nur gestoppt
def stop_container(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        print(f"Container '{container_name}' wurde gestoppt.")
    except docker.errors.FileNotFoundError:
        print(f"Container '{container_name}' nicht gefunden.")
    except Exception as e:
        print(f"Fehler beim Stooen: {e}")
      
# löscht den ganzen Container        
def remove_container(container_name):
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
        print(f"Container '{container_name}' wurde gelöscht.")
    except docker.errors.NotFound:
        print(f"Container '{container_name}' nicht gefunden.")
    except Exception as e:
        print(f"Fehler beim Löschen: {e}")