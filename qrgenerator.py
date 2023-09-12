import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QGroupBox, QFormLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import qrcode

class PrescriptionGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.medication_entries = []  # List to store medication entry widgets
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Prescription QR Generator')
        self.setGeometry(100, 100, 800, 600)  # Set a custom window size

        # Create labels and input fields for patient and doctor names
        self.label_patient_name = QLabel('Patient Name:')
        self.entry_patient_name = QLineEdit()
        self.entry_patient_name.setPlaceholderText('Enter patient name')

        self.label_doctor_name = QLabel('Doctor Name:')
        self.entry_doctor_name = QLineEdit()
        self.entry_doctor_name.setPlaceholderText('Enter doctor name')

        # Create a scroll area to contain medication entries
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show vertical scrollbar

        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)

        # Add widgets to layout
        self.scroll_layout.addWidget(self.label_patient_name)
        self.scroll_layout.addWidget(self.entry_patient_name)
        self.scroll_layout.addWidget(self.label_doctor_name)
        self.scroll_layout.addWidget(self.entry_doctor_name)

        # Add initial medication entry
        self.add_medication_entry()

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)

        # Create button layout
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        # Create Generate QR button
        self.generate_button = QPushButton('Generate QR Code')
        self.generate_button.clicked.connect(self.generate_qr)
        button_layout.addWidget(self.generate_button)

        # Create Add Medication button
        self.add_medication_button = QPushButton('Add Medication')
        self.add_medication_button.clicked.connect(self.add_medication_entry)
        button_layout.addWidget(self.add_medication_button)

        # Create a placeholder QR image
        qr_pixmap = QPixmap('placeholder_qr.png')
        self.qr_image = QLabel(self)
        self.qr_image.setPixmap(qr_pixmap)
        self.qr_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.qr_image)

    def add_medication_entry(self):
        group_box = QGroupBox('Medication Details')
    
        # Create labels and input fields for medication details
        label_medication = QLabel('Medication Name:')
        entry_medication = QLineEdit()
        entry_medication.setPlaceholderText('Enter medication name')

        label_dosage = QLabel('Dosage:')
        entry_dosage = QLineEdit()
        entry_dosage.setPlaceholderText('Enter dosage')

        label_quantity = QLabel('Quantity:')
        entry_quantity = QLineEdit()
        entry_quantity.setPlaceholderText('Enter quantity')

        # Create layout for medication entry
        layout = QFormLayout()
        layout.addRow(label_medication, entry_medication)
        layout.addRow(label_dosage, entry_dosage)
        layout.addRow(label_quantity, entry_quantity)

        group_box.setLayout(layout)

        # Add the group box to the scroll layout
        self.scroll_layout.addWidget(group_box)

        # Append entry fields to the medication_entries list
        self.medication_entries.append((entry_medication, entry_dosage, entry_quantity))

    def generate_qr(self):
        # Get patient and doctor names
        patient_name = self.entry_patient_name.text()
        doctor_name = self.entry_doctor_name.text()

        # Prepare data for QR code
        data = {
            "Patient Name": patient_name,
            "Doctor Name": doctor_name,
            "Medications": []
        }

        for entry in self.medication_entries:
            medication_name = entry[0].text()
            dosage = entry[1].text()
            quantity = entry[2].text()

            medication_data = {
                "Medication Name": medication_name,
                "Dosage": dosage,
                "Quantity": quantity
            }

            data["Medications"].append(medication_data)

        # Encode data as JSON
        import json
        json_data = json.dumps(data)

        # Generate QR code
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json_data)
        qr.make(fit=True)

        qr_code = qr.make_image(fill_color="black", back_color="white")
        qr_code.save("generated_qr.png")

        # Update the QR image
        qr_pixmap = QPixmap('generated_qr.png')
        self.qr_image.setPixmap(qr_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PrescriptionGenerator()
    ex.show()
    sys.exit(app.exec_())
