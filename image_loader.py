import cv2  # Импорт библиотеки OpenCV для работы с камерой
from PyQt5.QtWidgets import QFileDialog, QMessageBox  # Импорт необходимых классов из PyQt5


class ImageLoader:
    @staticmethod
    def load_image_from_file():
        """
        Метод для загрузки изображения из файла с использованием диалога QFileDialog.

        Returns:
            str or None: Путь к выбранному файлу изображения или None в случае ошибки.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Images (*.png *.jpg *.jpeg)",
                                                   options=options)
        if file_path:
            return file_path
        else:
            QMessageBox.warning(None, "Error", "Failed to load image.")
            return None

    @staticmethod
    def capture_image_from_camera():
        """
        Метод для захвата изображения с веб-камеры с использованием OpenCV.

        Returns:
            str or None: Путь к сохранённому изображению или None в случае ошибки.
        """
        cap = cv2.VideoCapture(0)  # Инициализация захвата видео с камеры
        if not cap.isOpened():  # Проверка успешности открытия камеры
            QMessageBox.warning(None, "Error", "Failed to connect to webcam.")
            return None

        ret, frame = cap.read()  # Захват кадра с камеры
        if ret:  # Если захват прошёл успешно
            cap.release()  # Освобождение ресурсов камеры
            cv2.imwrite("captured_image.jpg", frame)  # Сохранение изображения в файл
            return "captured_image.jpg"
        else:  # Если захват не удался
            cap.release()  # Освобождение ресурсов камеры
            QMessageBox.warning(None, "Error", "Failed to capture image.")
            return None