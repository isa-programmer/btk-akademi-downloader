# BTK video indirici

Proje [tingirifistik](https://github.com/tingirifistik/BTK_Akademi)'tan ilham alınmıştır.

## Gereksinimler
- python3.11 veya daha yüksek

## Repo kurulumu
```
git clone https://github.com/isa-programmer/btk-akademi-downloader
cd btk-akademi-downloader/src
```

## Venv oluşturma ve kütüphaneleri kurma

```
python3 -m venv venv
source venv/bin/activate  # Linux/Mac için
venv\Scripts\activate  # Windows için
pip install -r requirements.txt
```

Bundan sonra yapmanız gereken şu komutu çalıştırmak

```
bash btk.sh # Linux/Mac için
btk.bat # Windows için
```

Sonrasında gerek talimatlar ile videonuzu indirebilirsiniz

## ACCESS TOKEN hakkında
>BTK sitesine API istekleri atarken bir ACCES TOKEN'e ihtiyacınız olacak

## Yapmanız gerekenler

* BTK hesabınızla tarayıcıya giriş yapmak
* cookie-editor adlı eklentiyi kurmak.
	- [Chrome için](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
	- [Firefox için](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- **access_token** yazan çerez değerinin içindekilerini token.txt dosyasına aynen yapıştırmak
- Ve hazır

>Bu proje GPLv3 lisansı altında yayımlanmıştır ve kullanımda hiçbir sorumluluk kabul edilmez.

Telif hakları [BTK](www.btkakademi.gov.tr)'ya aittir, izinsiz kullanım yasaktır.
