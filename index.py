import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import yt_dlp
import threading
import re

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Descargar Videos de YouTube")
        self.setGeometry(200, 200, 600, 300)

        # Crear el widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Estilo principal
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-family: Arial, Helvetica, sans-serif;
            }
            QLineEdit {
                background-color: #1E1E1E;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: #FFFFFF;
            }
            QLineEdit:focus {
                border: 1px solid #1DB954;
            }
            QPushButton {
                background-color: #1DB954;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1ED760;
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
            QLabel#status_label {
                font-size: 14px;
                color: #808080;
            }
        """)

        # Etiqueta de título
        self.label = QLabel("Ingrese el enlace del video de YouTube:")
        self.label.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(self.label)

        # Input de URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ejemplo: https://www.youtube.com/watch?v=DAWaJmEtSXw")
        self.layout.addWidget(self.url_input)

        # Botón de descarga
        self.download_button = QPushButton("Descargar Video")
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.download_video)
        self.layout.addWidget(self.download_button)

        # Mensaje de estado
        self.status_label = QLabel("")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

    def download_video(self):
        video_url = self.url_input.text().strip()
        if not video_url:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un enlace válido.")
            return

        # Deshabilitar el botón mientras se descarga
        self.download_button.setEnabled(False)
        self.status_label.setText("Obteniendo título y descargando video...")

        # Descargar el video en un hilo separado
        threading.Thread(target=self._download_video_thread, args=(video_url,)).start()

    def _download_video_thread(self, video_url):
        ydl_opts = {"quiet": True}
        try:
            # Obtener la información del video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                title = info.get("title", "video")
                
                # Acortar el título y limpiar caracteres especiales
                clean_title = re.sub(r'[\\/*?:"<>|]', "", title)  # Elimina caracteres no válidos
                short_title = clean_title[:30]  # Limita el título a 30 caracteres

                # Configurar opciones de descarga
                download_opts = {
                    "format": "best",
                    "outtmpl": f"videos/{short_title}.%(ext)s",  # Guardar en la carpeta "videos"
                }

                # Descargar el video
                with yt_dlp.YoutubeDL(download_opts) as downloader:
                    downloader.download([video_url])

                self.status_label.setText(f"¡Video descargado como: {short_title}!")
        except Exception as e:
            self.status_label.setText("Error al descargar el video.")
            QMessageBox.critical(self, "Error", f"Error al descargar el video:\n{e}")
        finally:
            self.download_button.setEnabled(True)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())
