# Отдельный образ для сборки Python прилоложения
FROM api_2025:1.0 

RUN pip install flask
RUN pip install connexion
RUN pip install connexion[swagger-ui]
RUN pip install connexion[flask]
RUN pip install connexion[uvicorn]

COPY ./src /app/src
COPY ./main.py /app/main.py
COPY ./swagger.yaml /app/swagger.yaml

# Точка запуска
CMD ["python", "main.py"]





