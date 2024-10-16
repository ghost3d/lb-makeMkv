import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
import subprocess
import os

class MKVConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Select an image sequence folder", self)
        self.layout.addWidget(self.label)
        
        self.browseButton = QPushButton("Browse", self)
        self.browseButton.clicked.connect(self.browse)
        self.layout.addWidget(self.browseButton)
        
        self.createMKVButton = QPushButton("Create MKV", self)
        self.createMKVButton.clicked.connect(self.create_mkv)
        self.layout.addWidget(self.createMKVButton)
        
        self.closeButton = QPushButton("Close", self)
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)
        
        self.setLayout(self.layout)
        self.setWindowTitle('MKV Converter')
        self.show()
        
    def browse(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.folder_path:
            self.label.setText(f"Selected folder: {self.folder_path}")
        
    def create_mkv(self):
        if hasattr(self, 'folder_path'):
            # Find the first image file in the folder to determine the base name
            for file_name in os.listdir(self.folder_path):
                if file_name.endswith('.png'):
                    base_name = file_name.rsplit('.', 1)[0][:-4]  # Remove the frame number and extension
                    break
            else:
                self.label.setText("No PNG files found in the selected folder.")
                return
            
            output_file = os.path.join(self.folder_path, f"{base_name}.mkv")
            command = f"ffmpeg -framerate 24 -i {self.folder_path}/{base_name}%04d.png -c:v libx264 {output_file}"
            subprocess.run(command, shell=True)
            self.label.setText("MKV file created successfully!")
        else:
            self.label.setText("Please select a folder first.")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MKVConverter()
    sys.exit(app.exec_())