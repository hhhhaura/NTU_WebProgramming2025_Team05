FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]