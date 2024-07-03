import torch
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw

class ImageProcessor:
    def __init__(self, image_path=None, image=None):
        """
        Инициализация объекта ImageProcessor для работы с изображениями.

        Args:
            image_path (str, optional): Путь к изображению для загрузки. Defaults to None.
            image (PIL.Image.Image, optional): Объект изображения. Defaults to None.
        """
        self.image_path = image_path
        self.image = image if image is not None else Image.open(image_path)
        self.original_image = self.image.copy()  # Копия оригинального изображения для сброса изменений

    def apply_operations(self, operations):
        """
        Применение операций к изображению.

        Args:
            operations (list): Список операций для применения.
        """
        for operation in operations:
            if operation['type'] == 'negative':
                self.image = self.show_negative()
            elif operation['type'] == 'brightness':
                factor = operation['factor']
                self.image = self.increase_brightness(factor)
            elif operation['type'] == 'circle':
                x = operation['x']
                y = operation['y']
                radius = operation['radius']
                self.image = self.draw_circle(x, y, radius)
            elif operation['type'] == 'channel':
                channel = operation['channel']
                self.image = self.get_channel(channel)

    def show_negative(self):
        """
        Преобразование изображения в негатив.

        Returns:
            PIL.Image.Image: Негативное изображение.
        """
        img_array = np.array(self.image)
        img_tensor = torch.from_numpy(img_array).float()
        negative_tensor = 255 - img_tensor
        negative_image = Image.fromarray(negative_tensor.byte().numpy())
        return negative_image

    def increase_brightness(self, factor):
        """
        Увеличение яркости изображения.

        Args:
            factor (float): Фактор увеличения яркости.

        Returns:
            PIL.Image.Image: Изображение с увеличенной яркостью.
        """
        enhancer = ImageEnhance.Brightness(self.image)
        brightened_image = enhancer.enhance(factor)
        return brightened_image

    def draw_circle(self, x, y, radius):
        """
        Нарисовать круг на изображении.

        Args:
            x (int): Координата X центра круга.
            y (int): Координата Y центра круга.
            radius (int): Радиус круга.

        Returns:
            PIL.Image.Image: Изображение с нарисованным кругом.
        """
        draw = ImageDraw.Draw(self.image)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline='red', width=5)
        return self.image

    def get_channel(self, channel):
        """
        Получить отдельный цветовой канал изображения.

        Args:
            channel (str): Канал 'R', 'G' или 'B'.

        Returns:
            PIL.Image.Image: Изображение с выбранным цветовым каналом.
        """
        channels = {'R': 0, 'G': 1, 'B': 2}
        img_array = np.array(self.image)
        channel_img = np.zeros_like(img_array)
        channel_img[:, :, channels[channel]] = img_array[:, :, channels[channel]]
        return Image.fromarray(channel_img)

    def reset_to_original(self):
        """
        Сброс изображения к оригинальному состоянию.
        """
        self.image = self.original_image.copy()  # Сброс к оригинальному изображению
