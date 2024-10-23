import cv2
from simple_facerec import SimpleFacerec

def process_video(image_path, video_path, output_path="output.mp4"):
    sfr = SimpleFacerec()
    sfr.load_encoding_image(image_path)

    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        face_locations, face_names, res = sfr.detect_known_faces(frame)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top, right, bottom, left = map(int, [top, right, bottom, left])
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            label = name if name else "Unknown"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)
            label_y = max(top - 10, 10)
            cv2.rectangle(frame, (left, label_y - label_size[1] - 5), 
                          (left + label_size[0] + 5, label_y + 5), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, label, (left, label_y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)

        if res:
            out.write(frame)

    cap.release()
    out.release()

    return output_path
