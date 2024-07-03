from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog, QComboBox, QGroupBox, QGridLayout, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image  # Импорт библиотеки PIL для обработки изображений
from image_processor import ImageProcessor  # Импорт класса ImageProcessor из вашего модуля
from image_loader import ImageLoader  # Импорт класса ImageLoader из вашего модуля

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Приложение для обработки изображений")
        self.setGeometry(100, 100, 1024, 768)  # Установка заголовка окна и размеров

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(800, 600)  # Фиксированный размер для отображения изображения

        # Кнопки загрузки и захвата изображений
        load_button = QPushButton("Загрузить изображение", self)
        load_button.clicked.connect(self.load_image)
        load_button.setStyleSheet("background-color: lightblue; font-size: 14px; padding: 10px;")

        capture_button = QPushButton("Захватить изображение", self)
        capture_button.clicked.connect(self.capture_image)
        capture_button.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 10px;")

        # Группа кнопок для операций обработки изображения
        self.negative_checkbox = QCheckBox("Отобразить негатив", self)
        self.negative_checkbox.stateChanged.connect(self.toggle_negative)
        self.negative_checkbox.setStyleSheet("background-color: orange; font-size: 14px; padding: 10px;")

        brightness_button = QPushButton("Увеличить яркость", self)
        brightness_button.clicked.connect(self.increase_brightness)
        brightness_button.setStyleSheet("background-color: yellow; font-size: 14px; padding: 10px;")

        circle_button = QPushButton("Нарисовать круг", self)
        circle_button.clicked.connect(self.draw_circle)
        circle_button.setStyleSheet("background-color: lightcoral; font-size: 14px; padding: 10px;")

        reset_button = QPushButton("Сбросить изображение", self)
        reset_button.clicked.connect(self.reset_image)
        reset_button.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 10px;")

        # Комбо-бокс для выбора цветового канала
        self.channel_combo = QComboBox(self)
        self.channel_combo.addItems(["R", "G", "B"])
        self.channel_combo.currentTextChanged.connect(self.show_channel)
        self.channel_combo.setStyleSheet("font-size: 14px; padding: 10px;")
        self.channel_combo.setCurrentText("R")  # Установка значения по умолчанию на канал R

        # Организация кнопок в группы
        load_capture_layout = QHBoxLayout()
        load_capture_layout.addWidget(load_button)
        load_capture_layout.addWidget(capture_button)

        process_layout = QVBoxLayout()
        process_layout.addWidget(self.negative_checkbox)
        process_layout.addWidget(brightness_button)
        process_layout.addWidget(circle_button)
        process_layout.addWidget(reset_button)
        process_layout.addWidget(self.channel_combo)

        load_capture_group = QGroupBox("Загрузка и захват")
        load_capture_group.setLayout(load_capture_layout)

        process_group = QGroupBox("Обработка изображения")
        process_group.setLayout(process_layout)

        # Основной макет окна
        main_layout = QGridLayout()
        main_layout.addWidget(load_capture_group, 0, 0)
        main_layout.addWidget(process_group, 0, 1)
        main_layout.addWidget(self.label, 1, 0, 1, 2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.image_processor = None
        self.current_image = None
        self.operations = []

    def load_image(self):
        """Загрузка изображения из файла с помощью ImageLoader."""
        image_path = ImageLoader.load_image_from_file()
        if image_path:
            self.image_processor = ImageProcessor(image_path=image_path)
            self.current_image = self.image_processor.image
            self.display_image(self.current_image)

    def capture_image(self):
        """Захват изображения с камеры с помощью ImageLoader."""
        image_path = ImageLoader.capture_image_from_camera()
        if image_path:
            self.image_processor = ImageProcessor(image_path=image_path)
            self.current_image = self.image_processor.image
            self.display_image(self.current_image)

    def toggle_negative(self, state):
        """Переключение операции 'Отобразить негатив'."""
        if self.image_processor:
            if state == Qt.Checked:
                operation = {'type': 'negative'}
                self.operations.append(operation)
            else:
                self.remove_operation('negative')

            self.apply_operations_and_display()

    def increase_brightness(self):
        """Увеличение яркости изображения."""
        if self.image_processor:
            factor, ok = QInputDialog.getDouble(self, "Увеличение яркости", "Введите коэффициент яркости:", min=1.0, max=5.0)
            if ok:
                operation = {'type': 'brightness', 'factor': factor}
                self.operations.append(operation)
                self.apply_operations_and_display()

    def draw_circle(self):
        """Нарисовать круг на изображении."""
        if self.image_processor:
            x, ok_x = QInputDialog.getInt(self, "Нарисовать круг", "Введите координату X:")
            if ok_x:
                y, ok_y = QInputDialog.getInt(self, "Нарисовать круг", "Введите координату Y:")
                if ok_y:
                    radius, ok_radius = QInputDialog.getInt(self, "Нарисовать круг", "Введите радиус:")
                    if ok_radius:
                        operation = {'type': 'circle', 'x': x, 'y': y, 'radius': radius}
                        self.operations.append(operation)
                        self.apply_operations_and_display()

    def show_channel(self):
        """Отобразить определённый цветовой канал изображения."""
        if self.image_processor:
            channel = self.channel_combo.currentText()
            self.operations = [{'type': 'channel', 'channel': channel}]  # Заменить операции только на текущий канал
            self.apply_operations_and_display()

    def apply_operations_and_display(self):
        """Применить текущие операции к изображению и отобразить его."""
        if self.image_processor:
            self.image_processor.reset_to_original()
            self.image_processor.apply_operations(self.operations)
            self.current_image = self.image_processor.image
            self.display_image(self.current_image)

    def remove_operation(self, operation_type):
        """Удалить определённый тип операции из списка операций."""
        self.operations = [op for op in self.operations if op['type'] != operation_type]

    def display_image(self, image):
        """Отобразить обработанное изображение на QLabel."""
        image = image.convert("RGB")  # Преобразовать в режим RGB для совместимости с QImage
        image = self.resize_image(image, 1024, 768)  # Изменить размер изображения
        qimage = QImage(image.tobytes(), image.width, image.height, image.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        scaled_pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        self.label.setAlignment(Qt.AlignCenter)

    def resize_image(self, image, max_width, max_height):
        """Изменить размер изображения, сохраняя пропорции."""
        width, height = image.size
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_size = (int(width * ratio), int(height * ratio))
            image = image.resize(new_size, Image.ANTIALIAS)
        return image

    def reset_image(self):
        """Сбросить изображение до его исходного состояния."""
        if self.image_processor:
            self.operations = []  # Очистить список операций
            self.image_processor.reset_to_original()  # Сбросить процессор изображения до исходного
            self.current_image = self.image_processor.image
            self.display_image(self.current_image)
            self.negative_checkbox.setChecked(False)  # Снять отметку с 'Отобразить негатив'
            self.channel_combo.setCurrentText("R")  # Установить комбо-бокс каналов на канал 'R' по умолчанию

if __name__ == "__main__":
    app = QApplication([])  # Создание экземпляра приложения
    main_window = MainWindow()  # Создание экземпляра основного окна
    main_window.show()  # Отображение основного окна
    app.exec_()  # Запуск главного цикла приложения
