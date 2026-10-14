import json, os
RAW = "synapse_backward.json"
VERIFIED = "verified_backward.json"

def verify():
    if not os.path.exists(RAW): return False
    try:
        with open(RAW, "r") as f: data = json.load(f)
        grads = data.get("gradients_for_eye", [])
        if not isinstance(grads, list) or len(grads) < 2: return False
        clean = [max(-5.0, min(5.0, float(g))) for g in grads[:2]]
        with open(VERIFIED, "w") as f:
            json.dump({"gradients_for_eye": clean}, f, indent=4)
        print(f"🛡️ [LỌC THÀNH CÔNG] Đạo hàm an toàn: {clean}")
        return True
    except Exception: return False

if __name__ == "__main__": verify()
