# HastaVyakta: Intelligent Recognition and Analysis of Bharatanatyam Mudras

**HastaVyakta** is an AI-powered tool that identifies and interprets **Samyuta Hastas** (two-hand gestures) from Bharatanatyam dance. The system uses deep learning to analyze hasta images and return rich cultural insights such as the hasta name, its meaning, shloka (verse), correct hand positioning, and various viniyogas (usages).

---

## 🔍 Features

- 🎯 Recognizes 24 Samyuta Hastas of Bharatanatyam
- 📷 Accepts image input for detection
- 🧠 Powered by CNN-based deep learning and YOLOv8
- 📖 Returns:
  - Hasta Name
  - Meaning
  - Sanskrit Shloka
  - Correct Hand Positioning
  - Viniyogas (Usages)

---

## 🛠️ Tech Stack

- **Python**
- **YOLOv8 / YOLOv5**
- **OpenCV**
- **TensorFlow / PyTorch**
- **Roboflow** (for dataset labeling)
- **Google Colab** (for training and evaluation)

---

## 🧪 Dataset

- 24 Samyuta Hastas  
- 50 images per hasta (original)  
- Augmented 5× → 1600 images total  
- Manually labeled using Roboflow  
- Images captured with white background for contrast

---

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/Dishapadre/HastaVyakta.git
   cd HastaVyakta
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the detection module or notebook as per project setup.

---

## 📚 Output Example

If "Anjali Hasta" is detected:
- **Name**: Anjali
- **Meaning**: Salutation
- **Shloka**: *"Anjalih sannyasta-hastayoh..."*
- **Viniyogas**:
  - Prayer
  - Respect
  - Greetings

---

## 🌱 Future Scope

- Extend to **Asamyuta Hastas** (single-hand gestures)
- Add **real-time webcam detection**
- Deploy full **web or mobile application**
- Provide **pose correction feedback** for dance learners

---

## 👩‍💻 Author

**Disha Padre**  
[GitHub Profile](https://github.com/Dishapadre)

---

## 📄 License

This project is for academic and research purposes only. Proper citation required if reused.
