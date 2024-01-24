# Используйте базовый образ Python
FROM python:3.9

# Создайте и установите рабочую директорию
WORKDIR /opt/app

# Скопируйте все файлы из текущего каталога в контейнер
COPY . .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Откройте порт, на котором будет работать FastAPI
EXPOSE 8000

# Запустите ваше приложение (пример - файл main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
