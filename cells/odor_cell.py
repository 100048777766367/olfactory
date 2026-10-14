import math
import random
import json
import os

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-max(min(x, 500), -500)))

class OdorCell:
    def __init__(self, receptor_id, n_chemical_features=4, storage_dir="synapses"):
        self.id = receptor_id
        self.n_chem = n_chemical_features
        self.storage_path = os.path.join(storage_dir, f"{self.id}.json")
        self.os_dir = storage_dir
        
        self.affinity = []
        self.bias = 0.0
        self.last_molecule = []
        
        self.load_self()

    def load_self(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                if len(data.get("affinity", [])) == self.n_chem:
                    self.affinity = data["affinity"]
                    self.bias = data.get("bias", 0.0)
                    return
            except Exception:
                pass

        # TỰ KHỞI SINH: Tạo ái lực hóa học ngẫu nhiên
        self.affinity = [random.uniform(-0.8, 0.8) for _ in range(self.n_chem)]
        self.bias = random.uniform(-0.2, 0.2)
        self.save_self()

    # LIÊN KẾT HÓA HỌC: Đo mức độ bám dính của phân tử mùi vào thụ thể
    def bind(self, molecule_vector):
        self.last_molecule = molecule_vector
        # Ái lực liên kết: sum(affinity * molecule_features) + bias
        binding_energy = sum(self.affinity[i] * molecule_vector[i] for i in range(self.n_chem)) + self.bias
        activation = sigmoid(binding_energy)
        return round(activation, 4)

    # ĐIỀU CHỈNH THÍCH NGHI MÙI (Nhận đạo hàm từ Não để nhận diện mùi chuẩn hơn)
    def adapt_from_brain_gradient(self, grad, lr=0.05):
        if self.last_molecule:
            for i in range(self.n_chem):
                self.affinity[i] += lr * grad * self.last_molecule[i]
            self.bias += lr * grad
            self.save_self()

    def save_self(self):
        os.makedirs(self.os_dir, exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({"affinity": [round(a, 4) for a in self.affinity], "bias": round(self.bias, 4)}, f, indent=4)
