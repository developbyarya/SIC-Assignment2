import serial
import cv2
import numpy as np

# Open serial port (Adjust COMx and baudrate)
ser = serial.Serial('COMx', 115200, timeout=1)

jpeg_data = bytearray()

while True:
    byte = ser.read(1)  # Read one byte at a time

    if not byte:
        continue  # No data, skip

    jpeg_data += byte

    # Check for start and end of JPEG frame
    if jpeg_data[:2] == b'\xFF\xD8' and jpeg_data[-2:] == b'\xFF\xD9':
        # Convert bytes to numpy array
        img_array = np.frombuffer(jpeg_data, dtype=np.uint8)
        
        # Decode to OpenCV image
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if frame is not None:
            cv2.imshow("ESP32-CAM Serial Stream", frame)
            cv2.waitKey(1)  # Display the frame
        
        jpeg_data = bytearray()  # Reset buffer after displaying
