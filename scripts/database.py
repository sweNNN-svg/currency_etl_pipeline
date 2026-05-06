from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):
    """
    Veritabanı adaptörleri için soyut baz sınıf (Interface).
    Bu sınıf, projenin hangi veritabanını kullandığından bağımsız
    olarak sahip olması gereken yetenekleri tanımlar.
    """

    @abstractmethod
    def connect(self):
        """Her adaptör kendi bağlantı mantığını kurmalıdır."""
        pass

    # Opsiyonel: Eğer tüm veritabanlarında ortak olacak metodlar
    # eklemek istersen buraya tanımlayabilirsin.
