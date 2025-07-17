FROM python:3.10-slim

WORKDIR /app

# Copy và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tạo thư mục lưu ảnh
RUN mkdir -p uploads

# Copy mã nguồn
COPY server.py .

# Expose cổng Flask sẽ chạy
EXPOSE 8080

# Chạy Flask app
CMD ["python", "server.py"]
