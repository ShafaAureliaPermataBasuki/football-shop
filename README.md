Menjawab beberapa pertanyaan berikut pada README.md pada root folder.
SOAL 1:
 Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?

 Jawaban: 
 1. Data delivery memastikan komponen-komponen seperti frontend, backend, database, dan layanan pihak ketiga dapat berkomunikasi dan bertukar informasi secara efektif.
 2. Agar pengguna tidak akan mengalami penundaan, kesalahan, atau ketidakmampuan untuk mengakses informasi yang relevan.
 3. Karena sebagian besar fitur aplikasi sangat bergantung pada data yang diterima. Misalnya, menampilkan daftar produk, memproses pesanan, mengirim notifikasi, atau memperbarui profil pengguna.
 4. Data delivery dapat memastikan bahwa semua bagian sistem memiliki versi data terbaru.
 5. Data delivery memfasilitasi pertukaran data yang diperlukan untuk integrasi dengan pihak ketiga seperti pembayaran gateway, API, dll.
 6. Dapat membantu platform untuk menskalakan dan mempertahankan kinerja tinggi seiring dengan pertumbuhan jumlah pengguna dan volume data.

SOAL 2:
 Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?

 Jawaban:
 JSON lebih baik untuk kebanyakan aplikasi web karena lebih ringan, mudah dibaca manusia, dan mudah diproses oleh JavaScript. JSON lebih populer dibandingkan XML karena sintaksnya sederhana, parsing lebih cepat, dan lebih mudah diintegrasikan dengan teknologi web modern.

SOAL 3:
 Jelaskan fungsi dari method is_valid() pada form  Django dan mengapa kita membutuhkan method tersebut?

 Jawaban:
 Fungsi utama dari is_valid() adalah untuk melakukan validasi data yang disubmit oleh pengguna melalui form. is_valid() sangat dibutuhkan untuk menjaga keamanan data, integritas data, dan pencegahan bug.

SOAL 4:
 Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

Jawaban:
Untuk melindungi aplikasi dari serangan Cross-Site Request Forgery (CSRF). Jika  tidak menambahkan {% csrf_token %} pada form Django, aplikasi Anda akan rentan terhadap serangan CSRF, yang berarti permintaan POST tanpa proteksi, dan akan ditolak secara default oleh Django. Serangan CSRF terjadi ketika penyerang dapat menipu browser pengguna yang sudah terautentikasi ke situs web Anda untuk mengirimkan permintaan HTTP (biasanya POST) yang tidak diinginkan ke situs kita.

SOAL 5:
 Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
 
  Jawaban:
 1. Buat project & app
 2. Tambahkan main ke settings.py — INSTALLED_APPS.
 3. Rancang model Product (main/models.py) dengan atribut
 4. Buat ProductForm (main/forms.py) sebagai ModelForm untuk validasi dan kemudahan form rendering.
 5. Buat views untuk template
 6. Tambahkan 4 views data delivery
 7. Routing: daftarkan semua URL di main/urls.py lalu include('main.urls') di project/urls.py.
 8. Buat templates
 9. Migrate & test lokal:
 10. Deploy ke PWS
 11. Commit & Push ke GitHub

SOAL 6:
 Apakah ada feedback untuk asdos di tutorial 2 yang sudah kalian kerjakan?

 Jawaban:
 Tambahkan contoh Postman step-by-step (cara cek header & body), dan berikan contoh screenshot hasil yang benar.



HASIL TUGAS 3:

http://127.0.0.1:8000/
![alt text](image.png)
![alt text](image-1.png)

http://127.0.0.1:8000/xml/
![alt text](image-2.png)

http://127.0.0.1:8000/json/
![alt text](image-3.png)

http://127.0.0.1:8000/xml/1/
![alt text](image-4.png)

http://127.0.0.1:8000/json/1/
![alt text](image-5.png)