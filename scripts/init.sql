-- 1. Tablo: Döviz Kurları (Ana Veri Tablosu)
CREATE TABLE IF NOT EXISTS exchange_rates (
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate NUMERIC NOT NULL,
    last_updated TIMESTAMP WITH TIME ZONE NOT NULL,
    -- Claude Idempotency Çözümü: Aynı kurun aynı zaman dilimi için tekrar girmesini engeller
    UNIQUE(base_currency, target_currency, last_updated)
);

-- 2. Tablo: API Metadata (Claude'un 'Ölü Şema' dediği yer)
CREATE TABLE IF NOT EXISTS api_metadata (
    id SERIAL PRIMARY KEY,
    fetch_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    base_currency VARCHAR(3),
    status_code INTEGER,
    record_count INTEGER
);

-- 3. Performans: Indexleme (Claude Ölçeklenebilirlik Çözümü)
-- Zaman bazlı analizler çok sık yapılacağı için last_updated üzerine index atıyoruz.
CREATE INDEX IF NOT EXISTS idx_last_updated ON exchange_rates(last_updated);

-- 4. Güvenlik: Kullanıcı Yetkilendirme (Opsiyonel)
-- Docker-compose zaten POSTGRES_USER ile bunu hallediyor ama
-- ekstra kısıtlama istersen buraya ekleme yapılabilir.
