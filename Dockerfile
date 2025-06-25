FROM python:3.13.3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Minecraft-Cult-Website/ /app/

RUN apt-get update

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/
RUN chmod +x entrypoint.sh

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "minecraftcultsite.wsgi:application"]

ENTRYPOINT ["/app/entrypoint.sh"]

