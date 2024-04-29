from sentence_transformers import SentenceTransformer


class BERTAdapter:
    def __init__(self, model_name: str):
        """
        Инициализация адаптера с выбранной моделью SentenceTransformer.

        Args:
            model_name (str): Имя модели для загрузки.
        """
        self.model = SentenceTransformer(model_name)

    def text_to_vector(self, text) -> list:
        """
        Конвертирует текст в векторное представление с использованием загруженной модели SentenceTransformer.

        Args:
            text (str): Текст для конвертации.

        Returns:
            np.ndarray: Векторное представление текста.
        """
        return self.model.encode(text)
