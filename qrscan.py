import sqlite3
import cv2
from pyzbar.pyzbar import decode
import json
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('medicine_database.db')
cursor = conn.cursor()

def check_medicine_availability(medication_name, dosage, quantity):
    cursor.execute("SELECT * FROM medicines WHERE name=? AND dosage=?", (medication_name, dosage))
    medicine = cursor.fetchone()
    if medicine:
        expiry_date = datetime.strptime(medicine[3], '%d/%m/%Y').date()
        if expiry_date >= datetime.now().date() and int(medicine[5]) >= int(quantity):
            new_quantity = int(medicine[5]) - int(quantity)
            cursor.execute("UPDATE medicines SET amount_available=? WHERE id=?", (new_quantity, medicine[0]))
            conn.commit()
            return True, medicine
    return False, None

def scan_qr_code():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    while True:
        # Read a frame from the camera
        _, frame = cap.read()
        
        # Decode QR codes
        decoded_objects = decode(frame)
        
        # Display the frame
        cv2.imshow('QR Scanner', frame)
        
        # Check if a QR code is detected
        if decoded_objects:
            # Get the data from the QR code
            data = decoded_objects[0].data.decode('utf-8')
            
            # Release the camera and close the window
            cap.release()
            cv2.destroyAllWindows()
            
            return data
        
        # Check for exit key (ESC)
        if cv2.waitKey(1) == 27:
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

# Example usage
qr_data = scan_qr_code()
print("QR Data:", qr_data)

total_cost = 0  # Initialize total cost

if qr_data:
    data = json.loads(qr_data)

    # Extract information
    patient_name = data["Patient Name"]
    doctor_name = data["Doctor Name"]
    medications = data["Medications"]

    # Iterate through medications
    for medication in medications:
        medication_name = medication["Medication Name"]
        dosage = medication["Dosage"]
        quantity = medication["Quantity"]

        available, medicine = check_medicine_availability(medication_name, dosage, quantity)
        if available:
            print(f"Medicine Available: {medicine[1]} - Dosage: {medicine[2]} - Amount: {medicine[5]} - Expiry Date: {medicine[3]}")
            # Calculate cost and add to total
            price_per_quantity = medicine[6]
            total_cost += int(quantity) * price_per_quantity
        else:
            if medicine is None:
                print(f"No medicine found for: {medication_name}, Dosage: {dosage}")
            else:
                expiry_date = datetime.strptime(medicine[3], '%d/%m/%Y').date()
                if expiry_date <= datetime.now().date():
                    print(f"Medicine Expired: {medication_name}, Dosage: {dosage}")
                elif int(medicine[5]) >= int(quantity):
                    print(f"Medicine Less Quantity: {medication_name}, Dosage: {dosage}")
                else:
                    print(f"Medicine Unavailable: {medication_name}, Dosage: {dosage}")

if not qr_data:
    print("No QR Code detected.")

print(f"Total Cost of Available Medicine: {total_cost}")
