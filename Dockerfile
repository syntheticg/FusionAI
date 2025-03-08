# pakai python terbaru
FROM python:3.12  

# set workdir
WORKDIR /app  

# copy semua file ke dalam container
COPY . .  

# set environment variable agar g4f baca dari folder yang bisa diakses
ENV G4F_COOKIES_DIR="/app/har_and_cookies"  

# buat folder dan pastikan memiliki izin akses
RUN mkdir -p /app/har_and_cookies && chmod -R 777 /app/har_and_cookies  

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# gunakan port default railway
ENV PORT=3000  
EXPOSE $PORT  

# jalankan server
CMD ["python", "main.py"]
