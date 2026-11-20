import json
import os
from datetime import datetime
from pathlib import Path
from threading import RLock


# ==========================================
# KEYRADDIIN PERSONAL AI V2.0
# PERSISTENT AI MEMORY SYSTEM
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

MEMORY_FILE = DATA_DIR / "memory.json"

LOCK = RLock()


# CREATE MEMORY DIRECTORY
DATA_DIR.mkdir(parents=True, exist_ok=True)


# INITIALIZE MEMORY FILE
if not MEMORY_FILE.exists():

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:

        json.dump(
            {},
            file,
            indent=4
        )


# LOAD MEMORY
def load_memory():

    with LOCK:

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                return data if isinstance(data, dict) else {}

        except (OSError, json.JSONDecodeError):

            return {}


# SAVE MEMORY
def save_memory(data):

    with LOCK:

        temporary_file = MEMORY_FILE.with_suffix(".tmp")

        with open(
            temporary_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        os.replace(temporary_file, MEMORY_FILE)

        return True


# REMEMBER INFORMATION
def remember(key, value):

    if not key or not value:

        return False

    data = load_memory()

    data[str(key)] = {
        "value": str(value),
        "saved_at": datetime.now().isoformat()
    }

    return save_memory(data)


# RECALL INFORMATION
def recall(key):

    data = load_memory()

    item = data.get(str(key))

    if item:

        return item.get("value")

    return None


# RECALL ALL INFORMATION
def recall_all():

    data = load_memory()

    return {
        key: item.get("value")
        for key, item in data.items()
    }


# FORGET INFORMATION
def forget(key):

    data = load_memory()

    if str(key) not in data:

        return False

    del data[str(key)]

    return save_memory(data)


# CLEAR ALL MEMORY
def clear_memory():

    return save_memory({})


# MEMORY INFORMATION
def memory_info():

    data = load_memory()

    return {
        "total_memories": len(data),
        "status": "active",
        "storage": "JSON",
        "version": "2.0"
    }


print("KEYRADDIIN AI MEMORY SYSTEM LOADED!")