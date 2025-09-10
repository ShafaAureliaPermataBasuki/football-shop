# Football Shop

Aplikasi ini adalah tugas PWS berbasis Django untuk mengelola produk pada toko olahraga.  
Deploy URL: [https://shafa-aurelia-footballshop.pbp.cs.ui.ac.id](https://shafa-aurelia-footballshop.pbp.cs.ui.ac.id)

---

## Jawaban Pertanyaan

### 1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

1. Membuat virtual environment dan meng-install dependensi (`django`, `gunicorn`, dll).
1.a. Buat virtualenv & mengaktifkannya
1.b. Install dependensi yang dibutuhkan karena isolasi dependency; gunicorn diperlukan saat deploy PWS
2. Membuat project Django (`footballshop`) dan app (`main`). 
3. Menambahkan app `main` ke `INSTALLED_APPS` di `settings.py`.
4. Membuat model `Product` pada `main/models.py` dengan field `name`, `price`, `description`, `thumbnail`, `category`, `is_featured`, `size`, `rating`, dan `stock`.
5. Membuat migration (`python manage.py makemigrations` dan `python manage.py migrate`).
6. Mendaftarkan model ke `admin.py` agar bisa diakses melalui `/admin`.
7. Membuat view `index` di `views.py` dan template `index.html` untuk menampilkan informasi app, nama, dan kelas.
8. Mengatur routing pada `urls.py` (global `footballshop/urls.py` dan `main/urls.py`).
9. Menambahkan konfigurasi `ALLOWED_HOSTS`, `STATIC_ROOT`, dan environment variable di `settings.py`.
10. Menulis `requirements.txt` (termasuk `gunicorn`) dan `.gitignore`.
11. Push ke GitHub (`origin`) dan deploy ke PWS (`pws`) dengan `git push`.
12. Mengecek aplikasi di URL deployment, memastikan `/` dan `/admin` berjalan dengan benar.
13. Tunggu status Running, buka https://<username>-footballshop.pbp.cs.ui.ac.id/ dan /admin. Jika 404: cek ALLOWED_HOSTS, urls.py include, dan struktur repo (manage.py di root).

### 2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
[Client Browser]
     |
     |  GET /            (1) user buka home
     v
[DNS / Load Balancer / PWS]
     |
     v
[Gunicorn / ASGI server]  -- menjalankan footballshop.wsgi / ASGI app
     |
     v
footballshop/urls.py  --(routing tingkat global)--> include('main.urls') or admin/
     |
     v
main/urls.py  --(mapping path)--> views.index(request)
     |
     v
main/views.py  --(logic)--> 
     - (opsional) query database via main.models.Product.objects...
     - siapkan context dict
     - render template: render(request, 'main/index.html', context)
     |
     v
main/templates/main/index.html  --(template engine)--> HTML final
     |
     v
[Gunicorn] -> [HTTP Response HTML] -> [Client Browser]

Penjelasan hubungan:
urls.py = dispatcher → cocokkan URL → pilih view.
views.py = controller/handler → menerima HttpRequest, melakukan logika & memanggil models bila perlu.
models.py = definisi data/ORM → Product.objects.filter(...) diminta oleh view untuk data.
templates/*.html = presentasi → menerima context dari view, menghasilkan HTML.
settings.py mengatur di mana templates dicari, bagaimana database terhubung, dan host yang diizinkan — sehingga seluruh chain bisa bekerja.

### 3. Jelaskan peran settings.py dalam proyek Django!
settings.py adalah pusat konfigurasi Django. Fungsi utamanya:
- Menentukan aplikasi aktif (INSTALLED_APPS).
- Konfigurasi database (DATABASES) — dimana migrasi akan diaplikasikan.
- Konfigurasi template (TEMPLATES) dan direktori template.
- ALLOWED_HOSTS — host/domain yang diizinkan (penting untuk produksi).
- SECRET_KEY, DEBUG — pengaturan keamanan & mode debug.
- STATIC_URL / STATIC_ROOT, MEDIA_URL / MEDIA_ROOT — pengaturan assets.
- WSGI_APPLICATION / ASGI_APPLICATION — entry point server.
- MIDDLEWARE — pipeline request/response (security, csrf, auth).
- LOGGING — konfigurasi log.
Tanpa pengaturan ini, routing, DB, template, dan server tidak akan bekerja konsisten di lingkungan development/production.

### 4. Bagaimana cara kerja migrasi database di Django?
1. Definisi model → Mengubah/buat class models.Model.
2. makemigrations → Django membandingkan model saat ini dengan snapshot terakhir, membuat file migration (app/migrations/0001_...py) berisi operasi (CreateModel, AddField, dll).
3. migrate → menjalankan operasi migration tersebut di database target (menciptakan tabel/kolom/constraint). Django menyimpan yang sudah dieksekusi di tabel django_migrations.
4. Commit migration file ke VCS supaya tim & server deploy memiliki langkah yang sama.
5. Rollback & versi → kamu bisa migrate ke state tertentu (python manage.py migrate appname 0001), migration memiliki dependency jadi urutan tetap.
6. Di deployment → biasanya proses deploy menjalankan python manage.py migrate otomatis atau kamu panggil sendiri; cek logs untuk melihat output migration.
7. Best practices: review migration, commit file migration, backup DB sebelum migrasi besar, hindari berkonflik pada branch berbeda tanpa menyelesaikan migration.

### 5. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
- Batteries-included: banyak fitur siap pakai (ORM, auth, form, admin) → mahasiswa cepat lihat hasil nyata.
- Admin otomatis: UI langsung untuk data model → memberi feedback cepat dan memudahkan debugging.
- Keamanan bawaan: CSRF, XSS protections, password hashing → ajarkan praktik aman sejak awal.
- Struktur & konvensi: memaksa pemisahan concerns (models, views, templates) → baik untuk belajar arsitektur.
- ORM memudahkan konsep mapping objek-relasional tanpa menulis SQL kompleks.
- Dokumentasi & komunitas besar → banyak resource belajar.
- Cepat prototyping: buat MVP web dari ide ke implementasi dalam hitungan jam.
- Sebagai perbandingan: framework micro seperti Flask bagus untuk memahami detail HTTP, tapi butuh wiring manual banyak hal — Django mengurangi boilerplate sehingga fokus pada konsep inti.

### 6. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
Hal yang sudah baik
Tutorial menyediakan langkah deploy ke PWS — sangat membantu.

Saran perbaikan (prioritas tinggi)
- Sertakan contoh requirements.txt contoh yang berisi minimal: django, gunicorn, asgiref, sqlparse. (Masalah gunicorn: not found muncul karena ini terlewat.)
- Jelaskan struktur repo contoh (visual tree): tunjukkan posisi manage.py, folder project, app, requirements, README. Banyak mahasiswa salah folder sehingga PWS gagal detect.
- Beri contoh .gitignore dan perintah git rm --cached untuk kasus file yang terlanjur ter-push (env, db.sqlite3).
- Buat tabel troubleshooting singkat (error log → kemungkinan penyebab → solusi). Contoh:
sh: gunicorn: not found → tambahkan gunicorn ke requirements.
404 root & /admin → cek ALLOWED_HOSTS, urls.py include, atau struktur repo.
Authentication failed saat git push pws → jelaskan bahwa harus pakai credentials PWS (dan cara regenerate).
- Jelaskan branch yang harus dipush ke PWS (master vs main) dan contoh perintah git remote set-url pws ....
- Tambahkan contoh .env.prod & langkah setting Environs di PWS, plus contoh cara mengambil PROJECT COMMAND.
- Contoh cara baca logs PWS: tunjuk baris-baris penting (migrations ran, gunicorn listening, stacktrace).
Contoh settings.py produksi minimal (ALLOWED_HOSTS, STATIC_ROOT, penggunaan env vars).
- Berikan script checklist final (command checklist sebelum push ke PWS): makemigrations, migrate, collectstatic, git add ., commit, push pws master.

## Author
- Nama: Shafa Aurelia Permata Basuki  
- NPM: 2406432236  
- Kelas: PBP C

