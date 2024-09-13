# Temel imaj olarak bir Ubuntu imajı kullanın
FROM ubuntu:20.04

# Gereken bağımlılıkları yükleyin
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg

# Microsoft'un GPG anahtarını ekleyin
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Microsoft SQL Server ODBC sürücüsünün depo listesini ekleyin
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Paketleri güncelleyin ve ODBC Driver 17'yi yükleyin
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Uygulama bağımlılıklarını yükleyin ve uygulama kodunu kopyalayın (örneğin, Python uygulaması için)
# WORKDIR /app
# COPY . /app
# RUN pip install -r requirements.txt

# Uygulamanızı başlatma komutunu belirtin
# CMD ["python", "app.py"]