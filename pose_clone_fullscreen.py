import cv2
import mediapipe as mp
import numpy as np

class AdvancedPoseClone:
    def __init__(self):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1,
            smooth_landmarks=True
        )
        
        # Smoothing variables
        self.prev_landmarks = None
        self.smoothing_factor = 0.6  
        
        # Define connection pairs for the skeleton (BODY)
        self.body_connections = [
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), # Arms
            (11, 23), (12, 24), (23, 24),                     # Torso
            (23, 25), (25, 27), (24, 26), (26, 28)            # Legs
        ]

        # Define Face features 
        self.face_features = [
            [1, 2, 3],       # Left Eye curve
            [4, 5, 6],       # Right Eye curve
            [9, 10],         # Mouth (Left to Right)
            [0, 0]           # Nose dot
        ]

    def get_smooth_landmarks(self, current_landmarks, image_shape):
        h, w, _ = image_shape
        smooth_points = {}
        
        if current_landmarks:
            for idx, landmark in enumerate(current_landmarks.landmark):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                
                # Apply smoothing
                if self.prev_landmarks and idx in self.prev_landmarks:
                    prev_x, prev_y = self.prev_landmarks[idx]
                    cx = int(self.smoothing_factor * cx + (1 - self.smoothing_factor) * prev_x)
                    cy = int(self.smoothing_factor * cy + (1 - self.smoothing_factor) * prev_y)
                
                smooth_points[idx] = (cx, cy)
            
            self.prev_landmarks = smooth_points
            return smooth_points
        return None

    def draw_neon_character(self, img, landmarks, color, thickness=2, offset_x=0):
        if not landmarks:
            return

        # Overlay layer for the glow
        overlay = np.zeros_like(img)
        
        # 1. DRAW BODY
        for start_idx, end_idx in self.body_connections:
            if start_idx in landmarks and end_idx in landmarks:
                pt1 = list(landmarks[start_idx])
                pt2 = list(landmarks[end_idx])
                
                pt1[0] += offset_x
                pt2[0] += offset_x
                
                cv2.line(overlay, tuple(pt1), tuple(pt2), color, thickness)
                cv2.circle(overlay, tuple(pt1), thickness + 1, (255, 255, 255), -1)

        # 2. DRAW FACE
        for feature in self.face_features:
            points = []
            for idx in feature:
                if idx in landmarks:
                    pt = list(landmarks[idx])
                    pt[0] += offset_x 
                    points.append(pt)
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    cv2.line(overlay, tuple(points[i]), tuple(points[i+1]), color, thickness + 1)
            elif len(points) == 1:
                cv2.circle(overlay, tuple(points[0]), thickness + 3, (255, 255, 255), -1)

        # Create Glow Effect
        blur = cv2.GaussianBlur(overlay, (45, 45), 0)
        img[:] = cv2.addWeighted(img, 1.0, overlay, 1.0, 0) 
        img[:] = cv2.addWeighted(img, 1.0, blur, 1.3, 0)    

    def run(self):
        cap = cv2.VideoCapture(0)
        hue = 0
        
        window_name = 'Advanced Pose Clone'
        
        # --- WINDOW SETUP ---
        # 1. Create a "Normal" window (allows resizing/maximizing)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        # 2. Set specific size (1280x720 is a good "Medium-Large" HD size)
        cv2.resizeWindow(window_name, 1280, 720)
        
        print("Running in Resizable Window mode. Press 'q' to exit.")

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue

            # Flip and Darken
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            frame = cv2.convertScaleAbs(frame, alpha=0.7, beta=0)

            # Process
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

            # Smooth Landmarks
            landmarks = self.get_smooth_landmarks(results.pose_landmarks, frame.shape)
            
            # Color Generation
            hue = (hue + 1) % 180
            neon_color_hsv = np.uint8([[[hue, 255, 255]]])
            neon_color_bgr = cv2.cvtColor(neon_color_hsv, cv2.COLOR_HSV2BGR)[0][0]
            color_tuple = (int(neon_color_bgr[0]), int(neon_color_bgr[1]), int(neon_color_bgr[2]))

            if landmarks:
                # 1. Draw YOU
                self.draw_neon_character(frame, landmarks, color_tuple, thickness=3)
                
                # 2. Draw CLONE
                mirror_landmarks = {}
                center_x = w // 2
                
                for idx, (x, y) in landmarks.items():
                    dist = x - center_x
                    mirror_x = center_x - dist
                    # Offset logic: 25% of current width
                    offset = int(w * 0.25) 
                    mirror_landmarks[idx] = (mirror_x + offset, y)

                # Clone Color
                clone_hue = (hue + 90) % 180
                clone_hsv = np.uint8([[[clone_hue, 255, 255]]])
                clone_bgr = cv2.cvtColor(clone_hsv, cv2.COLOR_HSV2BGR)[0][0]
                clone_color = (int(clone_bgr[0]), int(clone_bgr[1]), int(clone_bgr[2]))
                
                self.draw_neon_character(frame, mirror_landmarks, clone_color, thickness=3)

            cv2.putText(frame, "NEON CLONE", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow(window_name, frame)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = AdvancedPoseClone()
    app.run()