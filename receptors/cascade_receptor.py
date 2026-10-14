import os, subprocess
OWNER = os.environ.get("REPO_OWNER", "")
PARENT = os.environ.get("REPO_PARENT", "")
UPSTREAM_SEED = "100048777766367"
TARGET_FILE = "synapse_backward.json"

def try_fetch(target):
    if not target: return False
    url = f"https://raw.githubusercontent.com/{target}/neuron/main/synapse_backward.json"
    res = subprocess.run(["curl", "-s", "-f", url, "-o", TARGET_FILE], capture_output=True)
    return res.returncode == 0 and os.path.exists(TARGET_FILE)

def main():
    if OWNER and try_fetch(OWNER): return
    if PARENT and try_fetch(PARENT): return
    if try_fetch(UPSTREAM_SEED): return
    print("🍃 [MÔI TRƯỜNG TĨNH] Chưa thấy xung đạo hàm từ phả hệ.")

if __name__ == "__main__": main()
