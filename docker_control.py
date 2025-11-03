import subprocess

#Referenziert die Compose Datei
COMPOSE_FILE = "docker-compose.yml"

def start_containers():
    try:
        result = subprocess.run(
            ["docker-compose", "-f", COMPOSE_FILE, "up", "-d"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Container wurden gestartet.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Fehler beim Starten der Container:")
        print(e.stderr)


def stop_containers():
    try:
        subprocess.run(["docker-compose", "-f", COMPOSE_FILE, "stop"], check=True)
        print("Container wurden gestoppt.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Stoppen: {e}")


def remove_containers(erase_volumes=False):
    try:
        cmd = ["docker-compose", "-f", COMPOSE_FILE, "down"]
        if erase_volumes:
            cmd.append("--volumes")
        subprocess.run(cmd, check=True)
        print("Container wurden gelöscht.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Löschen: {e}")
