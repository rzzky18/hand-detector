# ✋ Hand Gesture Controller – Kontrol Komputer dengan Tangan
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

Proyek Python yang memanfaatkan kamera untuk mendeteksi tangan dan mengubah gesture menjadi kontrol mouse & media seperti klik, scroll, dan volume. Powered by OpenCV dan MediaPipe.

---

## 🎯 Fitur

✅ Deteksi tangan real-time (21 titik landmark)  
🖱️ Kontrol mouse:
- Klik kiri:jari telunjuk & Jari Kelingking terbuka
- Klik kanan: Ibu jari, jari telunjuk & Jari Kelingking terbuka
- Double klik: Ibu Jari & Jari Kelingking terbuka
- Gerakkan kursor: Buka Semua tangan & Gerakkan tangan secara bebas  
🔉 Kontrol volume:
- Volume up/down berdasarkan jarak ibu jari & jari telunjuk  
🖱️ Scroll:
- Scroll up/down dengan gesture jari tertentu  
🧪 Mudah dikembangkan untuk kontrol lanjutan lainnya

---

## 🛠️ Teknologi

- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

---

## 📦 Instalasi

```bash
git clone https://github.com/rzzky18/hand-gesture-controller.git
cd hand-gesture-controller
pip install -r requirements.txt

---

## ▶️ Cara Pakai

python hand_controller.py
Pastikan webcam aktif dan posisikan tangan di area yang jelas.
Gesture akan otomatis dikonversi menjadi aksi komputer.

---

## ⚠️ Catatan

Rekomendasi: Gunakan pencahayaan cukup agar deteksi optimal
Gunakan resolusi webcam minimal 720p untuk hasil terbaik
Beberapa gesture bisa disesuaikan di kodenya

---

##👤 Author
GitHub: @rzzky18
Email: nimeklovt@gmail.com
Projects.co.id: Kyy_18

---

📄 Lisensi
Lisensi proyek ini adalah Apache License 2.0

“Gak perlu mouse lagi, cukup tanganmu!” 🖐️
