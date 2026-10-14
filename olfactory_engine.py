import json
import time
import os
from cells.odor_cell import OdorCell

class OlfactoryEngine:
    def __init__(self):
        # 2 Thụ thể mùi độc lập: 1 chuyên bắt mùi dinh dưỡng, 1 chuyên bắt mùi độc tố/khí độc
        self.cell_nutrient = OdorCell("o_nutrient", n_chemical_features=4)
        self.cell_toxin = OdorCell("o_toxin", n_chemical_features=4)

    # 1. CHIỀU XUÔI: HÍT MÙI -> PHÁT XUNG THẦN KINH KHỨU GIÁC
    def sniff_and_emit(self, odor_molecule):
        # odor_molecule là vector hóa học 4 chiều: [Kích thước, Độ phân cực, Nhóm lưu huỳnh, Độ bay hơi]
        nutrient_intensity = self.cell_nutrient.bind(odor_molecule)
        toxin_intensity = self.cell_toxin.bind(odor_molecule)

        features = [nutrient_intensity, toxin_intensity]
        timestamp = int(time.time())

        packet_forward = {
            "contract": "bodhi.olfactory.v1",
            "source": "olfactory_nose",
            "timestamp": timestamp,
            "features": features,
            "chemical_signature": odor_molecule
        }

        with open("synapse_forward.json", "w") as f:
            json.dump(packet_forward, f, indent=4)

        print("-" * 50)
        print(f"👃 [MŨI VỪA HÍT MÙI] Dấu vân tay hóa học: {odor_molecule}")
        print(f"   Xung Thần Kinh -> [Dinh dưỡng/Thơm: {nutrient_intensity}, Độc tố/Khét: {toxin_intensity}]")
        if toxin_intensity > 0.7:
            print("🚨 [CẢNH BÁO KHÍ ĐỘC] PHÁT HIỆN HỢP CHẤT ĐỘC HẠI HOẶC KHÍ CHÁY KHÉT!")
        print("-" * 50)
        return packet_forward

    # 2. CHIỀU NGƯỢC (SPLIT LEARNING): NÃO PHẢN HỒI ĐIỀU CHỈNH ĐỘ NHẠY MÙI
    def absorb_brain_feedback(self, backward_file="verified_backward.json"):
        if not os.path.exists(backward_file):
            print("🍃 [MÔI TRƯỜNG TĨNH] Chưa có xung đạo hàm phản hồi từ Não.")
            return

        try:
            with open(backward_file, "r") as f:
                data = json.load(f)
            grads = data.get("gradients_for_eye", [0.0, 0.0])
            print(f"⚡ [NHẬN ĐẠO HÀM TỪ NÃO] Gradient = {grads}")

            self.cell_nutrient.adapt_from_brain_gradient(grads[0])
            self.cell_toxin.adapt_from_brain_gradient(grads[1])
            print("🔧 [TIẾN HÓA] Mũi đã tự vặn lại ái lực liên kết thụ thể khứu giác!")
        except Exception as e:
            print(f"⚠️ Lỗi đọc xung đạo hàm: {e}")

if __name__ == "__main__":
    nose = OlfactoryEngine()
    nose.absorb_brain_feedback()

    # Thử nghiệm hít một phân tử mùi khét cháy / amoniac độc hại (Nhiều lưu huỳnh, độ phân cực cao)
    phan_tu_khi_doc = [0.9, 0.85, 0.95, 0.7]
    nose.sniff_and_emit(phan_tu_khi_doc)
