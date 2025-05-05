# Currency ETL Projesi

Bu proje, TRY bazlı döviz kurlarını her saat başı otomatik olarak çekip dönüştüren ve PostgreSQL veritabanına yükleyen bir ETL pipeline'ıdır. Airflow ile zamanlanmış, Grafana ile görselleştirilmiş, Docker Compose ile konteynerleştirilmiştir.

## Yapı

Proje şu adımları içerir:

1. `main.py`: API'den döviz verisini çeker, JSON olarak `data/currency.json` dosyasına kaydeder.
2. `convert.py`: JSON verisini `data/currency.csv` olarak CSV formatına dönüştürür.
3. `transform.py`: CSV verisini normalize eder, temizler, long formata çevirir ve `data/currency-v3.csv` dosyasına yazar.
4. `load.py`: `currency-v3.csv` dosyasındaki veriyi PostgreSQL veritabanındaki `exchange_rates` tablosuna yükler.

Tüm bu işlemler `currency_etl` adlı bir Airflow DAG'i üzerinden otomatikleştirilmiştir.

## Kullanılan Teknolojiler

- Python
- Apache Airflow
- PostgreSQL
- Grafana
- Docker Compose

## Dosya Yapısı

<pre lang="markdown"> <code> currency_etl/ ├── dags/ # Airflow DAG dosyası │ └── currency_etl_dag.py # Ana DAG tanımı ├── scripts/ # Python scriptleri │ ├── main.py # API'den veri çeker │ ├── convert.py # JSON to CSV │ ├── transform.py # Dataframe işlemleri │ └── load.py # PostgreSQL'e yükler ├── data/ # JSON ve CSV geçici veriler │ ├── currency.json │ └── currency.csv ├── logs/ # Airflow log klasörü ├── grafana-data/ # Grafana volume verisi ├── docker-compose.yml # Tüm servislerin tanımı ├── init.sql # PostgreSQL tablo oluşturur ├── exchange_rates_api_metadata.sql # Ek metadata scripti ├── requirements.txt # Python bağımlılıkları └── .gitignore # Git ignore ayarları </code> </pre>

---

## Başlatmak İçin

```bash
git clone https://github.com/sweNNN-svg/currency_etl_pipeline.git
cd currency_etl_pipeline
docker compose up -d --build
```

---

## Servis Arayüzleri

- **Airflow UI**: [http://localhost:8080](http://localhost:8080)
- **Grafana**: [http://localhost:3000](http://localhost:3000)  
  **Giriş Bilgileri**: `admin / admin`

---

## Airflow DAG Bilgisi

- **DAG Adı**: `currency_etl`
- **Schedule**: `Her saat başı (0 * * * *)`
- **Catchup**: `False`

### Görevler (Tasks):

1. `main_operation`  
   → API'den döviz kuru JSON verisini alır (`main.py`)

2. `convert`  
   → JSON'dan CSV üretir (`convert.py`)

3. `transform_data`  
   → DataFrame'i temizler ve dönüştürür (`transform.py`)

4. `load_to_postgres`  
   → PostgreSQL'e veri yükler (`load.py`)

---

## Notlar

- PostgreSQL container’ı başlarken `init.sql` içeriği ile `currency` veritabanını ve `exchange_rates` tablosunu oluşturur.
- Tüm veriler `data/` klasöründe işlenir ve saklanır.
- Her görev birbirine bağlıdır ve başarısız olursa yeniden denenir (`retry logic` uygulanır).

---

## Özellikler

- Apache Airflow ile otomatik ve zamanlanmış ETL pipeline
- Docker Compose ile tam izole çalışma ortamı
- Pandas ile veri işleme
- PostgreSQL'e veri yazımı
- Grafana ile dashboard izleme (geliştirilmeye açık)

---

## Geliştirme Planı

- PostgreSQL için partitioning destekli yapı
- Streaming veriye geçiş (Kafka, MQTT vs.)
- Redis cache desteği (API rate limit koruması)
- Amazon S3'e veri yedekleme
- Grafana'da otomatik dashboard provisioning

---

## Bağımlılıklar

Tüm bağımlılıklar `requirements.txt` dosyasıyla kurulur:
pandas
requests
psycopg2-binary

> Not: `apache/airflow:2.9.1` imajı, Airflow için gerekli temel bağımlılıkları zaten içerir.

---