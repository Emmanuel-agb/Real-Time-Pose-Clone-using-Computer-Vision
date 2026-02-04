# Neon Digital Twin: Real-Time Pose Clone 🚀

A real-time Computer Vision application that generates a "Digital Twin" with a neon aesthetic. This project utilizes **MediaPipe** for body tracking and **OpenCV** for custom rendering, creating a smoother, production-ready visual experience than standard pose estimation demos.

<img width="1917" height="1037" alt="pose clone" src="https://github.com/user-attachments/assets/56f88c41-56ee-42c6-8760-a486f1af56d5" />

## ✨ Key Features

*   **Custom Smoothing Algorithms:** Implemented Exponential Moving Average (EMA) smoothing to filter out the jitter from raw MediaPipe data, resulting in liquid, organic movement.
*   **Gaussian Bloom Rendering:** Replaced flat skeleton lines with a custom renderer using additive color blending and Gaussian blurring to achieve a high-fidelity "Neon" glow.
*   **Full Facial Tracking:** Maps eyes and mouth in real-time, allowing the clone to mimic expressions (unlike standard body-only trackers).
*   **Dynamic Mirroring:** Uses coordinate geometry transformations to create an interactive clone that moves relative to the user's center.

## 🛠️ Tech Stack

*   **Python 3.x**
*   **OpenCV (`cv2`)**: Image processing and rendering pipeline.
*   **MediaPipe**: High-fidelity pose estimation.
*   **NumPy**: Vector math and coordinate calculations.

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Emmanuel-agb/Real-Time-Pose-Clone-using-Computer-Vision.git
   cd Real-Time-Pose-Clone-using-Computer-Vision

## 🚀 Usage
Run the main script to start the webcam feed:
python pose_clone_fullscreen.py
Controls: Press q to quit the application.

## 🧠 How it Works
**Pose Extraction:** The script captures video frames and passes them to the MediaPipe Pose solution to extract 33 distinct 3D landmarks.
**Signal Processing:** To prevent "shaking," landmarks are passed through a smoothing function:
$L_{smooth} = \alpha \cdot L_{current} + (1 - \alpha) \cdot L_{prev}$

## Rendering:

* **The User:** Drawn in a cycling neon hue.
* **The Clone:** Calculated by inverting the X-coordinates relative to the frame center and applying an offset. Drawn in a complementary color (shifted 90° on the hue wheel).
* **Post-Processing:** A blurred copy of the overlay is added on top of the original image (cv2.addWeighted) to create the blooming light effect.
