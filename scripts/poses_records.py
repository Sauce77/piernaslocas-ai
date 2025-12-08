import cv2
import mediapipe as mp
import requests
import json
import time

# --- Configuración del Endpoint de Django ---
DJANGO_API_URL = 'http://127.0.0.1:8000/poses/submit/'
# Es buena práctica crear un endpoint específico que espere una lista de frames
SESSION_ID = "sesion_entrenamiento_" + str(int(time.time()))

# --- Parámetros de Lote ---
BATCH_SIZE = 30  # Envío cada 30 frames
pose_batch_buffer = [] # Lista donde se acumularán los datos
frame_counter = 0  # Contador de frames

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def process_and_send_pose_batch():
    global pose_batch_buffer, frame_counter # Necesario para modificar las variables globales
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara.")
        return

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 1. Detección de Pose (Igual que antes)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb.flags.writeable = False
            results = pose.process(frame_rgb)
            frame_rgb.flags.writeable = True 
            frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            
            keypoints_list = []
            if results.pose_landmarks:
                
                # Extracción de Coordenadas (Igual que antes)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    keypoints_list.append({
                        'id': id, 'x': lm.x, 'y': lm.y, 'z': lm.z, 'vis': lm.visibility
                    })
                
                # Dibujar resultados (opcional, pero ayuda a la visualización)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # --- 2. Lógica de Acumulación y Envío en Lote ---
                
                # Almacenar los datos del frame actual en el búfer
                current_frame_data = {
                    "frame_num": frame_counter, # Número del frame dentro de la sesión
                    "timestamp": time.time(),
                    "keypoints_data": keypoints_list
                }
                pose_batch_buffer.append(current_frame_data)
                
                frame_counter += 1
                
                feedback = f"Acumulando... ({len(pose_batch_buffer)}/{BATCH_SIZE})"
                
                # Verificar si el búfer ha alcanzado el tamaño del lote
                if len(pose_batch_buffer) >= BATCH_SIZE:
                    
                    # 3. Construir y Enviar el Payload (Lote)
                    batch_payload = {
                        "session_id": SESSION_ID,
                        "batch_size": BATCH_SIZE,
                        "frames": pose_batch_buffer # Toda la lista de 30 frames
                    }
                    
                    try:
                        # Envío de la petición POST con el lote completo
                        response = requests.post(DJANGO_API_URL, json=batch_payload, timeout=5) 
                        
                        if response.status_code == 201:
                            feedback = f"Lote de {BATCH_SIZE} enviado OK."
                            # ¡Importante! Limpiar el búfer después del envío exitoso
                            pose_batch_buffer = []
                        else:
                            feedback = f"Error {response.status_code} al enviar lote."
                            # Si hay error, puedes optar por limpiar o reintentar
                            
                    except requests.exceptions.RequestException:
                        feedback = "Error de conexión/timeout con Django."
                        
                    # 4. Actualizar el Búfer y el Contador (manejo de errores)
                    cv2.putText(frame, feedback, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Mostrar la vista
            cv2.imshow('OpenCV Batch Detector', frame)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    # 5. Envío de Datos Finales al salir
    # Si quedan frames pendientes en el búfer al cerrar la cámara
    if pose_batch_buffer:
        print(f"Enviando lote final de {len(pose_batch_buffer)} frames...")
        final_payload = {
            "session_id": SESSION_ID,
            "batch_size": len(pose_batch_buffer),
            "frames": pose_batch_buffer
        }
        try:
             requests.post(DJANGO_API_URL, json=final_payload, timeout=5)
        except requests.exceptions.RequestException:
             print("Error al enviar lote final.")


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    process_and_send_pose_batch()