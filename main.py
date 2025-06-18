import cv2
import numpy as np
import os
from tkinter import Tk, filedialog

# --- Seleziona cartelle ---
Tk().withdraw()
images_folder = filedialog.askdirectory(title="Seleziona la cartella con le immagini")
masks_folder = filedialog.askdirectory(title="Seleziona la cartella per salvare/caricare le maschere")

if not images_folder or not masks_folder:
    print("Cartella non selezionata. Esco.")
    exit()

# --- Parametri ---
brush_size = 10
drawing = False
erase_mode = False

scale = 1.0
offset_x = 0
offset_y = 0
panning = False
pan_start = (0, 0)

cursor_x, cursor_y = -1, -1

def draw_circle(event, x, y, flags, param):
    global drawing, erase_mode, scale, offset_x, offset_y, panning, pan_start, cursor_x, cursor_y

    cursor_x, cursor_y = x, y

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x_corr = int((x - offset_x) / scale)
            y_corr = int((y - offset_y) / scale)
            if 0 <= x_corr < mask.shape[1] and 0 <= y_corr < mask.shape[0]:
                if erase_mode:
                    cv2.circle(mask, (x_corr, y_corr), brush_size, (0), -1)
                else:
                    cv2.circle(mask, (x_corr, y_corr), brush_size, (255), -1)
        elif panning:
            offset_x = x - pan_start[0]
            offset_y = y - pan_start[1]

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        panning = True
        pan_start = (x - offset_x, y - offset_y)
    elif event == cv2.EVENT_RBUTTONUP:
        panning = False

# --- Elaborazione immagini ---
image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

index = 0
while index < len(image_files):
    img_name = image_files[index]
    img_path = os.path.join(images_folder, img_name)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Impossibile leggere {img_name}")
        index += 1
        continue

    mask_path = os.path.join(masks_folder, img_name)

    if os.path.exists(mask_path):
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None or mask.shape != img.shape[:2]:
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            print(f"Maschera incompatibile. Nuova creata per: {img_name}")
        else:
            print(f"Maschera caricata: {mask_path}")
    else:
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        print(f"Nessuna maschera trovata. Nuova creata per: {img_name}")

    scale = 1.0
    offset_x = 0
    offset_y = 0

    cursor_x, cursor_y = -1, -1

    window_name = f"{img_name} ({index+1}/{len(image_files)})"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_circle)

    while True:
        img_resized = cv2.resize(img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        mask_resized = cv2.resize(mask, (img_resized.shape[1], img_resized.shape[0]), interpolation=cv2.INTER_NEAREST)
        mask_color = cv2.merge([mask_resized]*3)
        overlay = cv2.addWeighted(img_resized, 0.7, mask_color, 0.3, 0)

        canvas = np.zeros_like(overlay)
        h, w = overlay.shape[:2]

        x1, y1 = max(offset_x, 0), max(offset_y, 0)
        x2, y2 = min(offset_x + w, w), min(offset_y + h, h)

        sx1, sy1 = max(-offset_x, 0), max(-offset_y, 0)
        sx2, sy2 = sx1 + (x2 - x1), sy1 + (y2 - y1)

        canvas[y1:y2, x1:x2] = overlay[sy1:sy2, sx1:sx2]

        # Disegna cursore
        if cursor_x >= 0 and cursor_y >= 0:
            color = (0, 0, 255) if not erase_mode else (0, 255, 255)
            cv2.circle(canvas, (cursor_x, cursor_y), int(brush_size * scale), color, 1)

        mode_text = f"{'ERASER' if erase_mode else 'BRUSH'} | Size: {brush_size} | Zoom: {scale:.2f}x"
        cv2.putText(canvas, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow(window_name, canvas)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('+') or key == ord('='):
            brush_size += 2
        elif key == ord('-') and brush_size > 2:
            brush_size -= 2
        elif key == ord('e'):
            erase_mode = not erase_mode
        elif key == ord('z'):
            scale *= 1.2
        elif key == ord('x'):
            scale /= 1.2
            if scale < 0.2:
                scale = 0.2
        elif key == ord('r'):
            scale = 1.0
            offset_x, offset_y = 0, 0
        elif key == ord('c'):
            if cursor_x >= 0 and cursor_y >= 0:
                x_corr = int((cursor_x - offset_x) / scale)
                y_corr = int((cursor_y - offset_y) / scale)
                if 0 <= x_corr < mask.shape[1] and 0 <= y_corr < mask.shape[0]:
                    if erase_mode:
                        cv2.circle(mask, (x_corr, y_corr), brush_size, (0), -1)
                    else:
                        cv2.circle(mask, (x_corr, y_corr), brush_size, (255), -1)
        elif key == ord('s'):
            cv2.imwrite(mask_path, mask)
            print(f"Maschera salvata: {mask_path}")
        elif key == ord('q'):
            break
        elif key == ord('w'):
            if index > 0:
                index -= 2  # vai indietro di una immagine netta
                break
            else:
                print("Already at the first image.")
        elif key == 27:
            print("\nSei sicuro di voler uscire? (y/n): ", end='', flush=True)
            cv2.destroyAllWindows()
            answer = input().strip().lower()
            if answer in ['y', 'yes']:
                exit()
            else:
                cv2.namedWindow(window_name)
                cv2.setMouseCallback(window_name, draw_circle)

    cv2.destroyWindow(window_name)
    index += 1

print("Fatto!")
