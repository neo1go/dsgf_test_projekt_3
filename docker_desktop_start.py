import subprocess
import os

"""
Hiermit wird die Docker Desktop App gestartet, um die Container Erstellung zu gewährleisten.
"""


def docker_app_start():
    docker_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"

    if os.path.exists(docker_path):
        subprocess.Popen([docker_path])
        print("✅ Docker Desktop wurde gestartet.")
    else:
        print("❌ Pfad zu Docker Desktop nicht gefunden.")
