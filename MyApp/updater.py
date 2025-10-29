import os, json, zipfile, shutil, requests, subprocess, sys

# === НАСТРОЙКИ ===
USER = "Pizdissshhh"       # ← Введи сюда свой GitHub логин
REPO = "myapp-updater"      # ← Имя репозитория
BRANCH = "main"

BASE_URL = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}"
VERSION_URL = f"{BASE_URL}/version.json"
ARCHIVE_URL = f"{BASE_URL}/app.zip"

LOCAL_DIR = "app"
LOCAL_VERSION_FILE = os.path.join(LOCAL_DIR, "version.json")

def get_local_version():
    try:
        with open(LOCAL_VERSION_FILE) as f:
            return json.load(f)["version"]
    except:
        return "0.0.0"

def get_remote_version():
    r = requests.get(VERSION_URL, timeout=10)
    r.raise_for_status()
    return json.loads(r.text)["version"]

def download_and_extract():
    print("🔄 Скачиваю новую версию...")
    r = requests.get(ARCHIVE_URL, timeout=60)
    r.raise_for_status()
    with open("update.zip", "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile("update.zip", "r") as zf:
        if os.path.exists("app_new"):
            shutil.rmtree("app_new")
        zf.extractall("app_new")

    # Заменяем старую версию
    if os.path.exists(LOCAL_DIR):
        shutil.rmtree(LOCAL_DIR)
    shutil.move("app_new", LOCAL_DIR)
    os.remove("update.zip")
    print("✅ Обновление завершено.")

def run_app():
    exe = os.path.join(LOCAL_DIR, "main.exe")
    py = os.path.join(LOCAL_DIR, "main.py")

    print("🚀 Запуск программы...")
    if os.path.exists(exe):
        subprocess.Popen([exe])
    elif os.path.exists(py):
        subprocess.Popen(["python", py])
    else:
        print("❌ Не найден main.exe или main.py")

if __name__ == "__main__":
    print("=== Обновление приложения ===")
    local = get_local_version()
    try:
        remote = get_remote_version()
    except Exception as e:
        print("⚠️ Ошибка получения версии:", e)
        run_app()
        sys.exit(0)

    print(f"Локальная версия: {local}")
    print(f"Удалённая версия: {remote}")

    if remote > local:
        download_and_extract()
    else:
        print("✅ Актуальная версия.")

    run_app()
