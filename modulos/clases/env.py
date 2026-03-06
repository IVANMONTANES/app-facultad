import os
from pathlib import Path
from dotenv import load_dotenv

def load_dotenv_clean() -> None:
    env_file = Path(".env")

    if env_file.exists():
        bytes_archivo = env_file.read_bytes()
        
        # verificamos si existe el bom , en caso de existir lo eliminamos #
        if len(bytes_archivo) >= 3 and bytes_archivo[0] == 239 and bytes_archivo[1] == 187 and bytes_archivo[2] == 191:
            env_file.write_bytes(bytes_archivo[3:])

