# Burniva Capstone Streamlit Dashboard

Repository ini digunakan untuk menjalankan dashboard Streamlit pada bagian `datascience` dari project Burniva Capstone.

Sebelum membuat environment dan menjalankan dashboard, download terlebih dahulu dataset dari Google Drive berikut:

https://drive.google.com/drive/folders/1GTRb6SjEelh5lidyL6qOW16SoPWKwO9x?usp=sharing

Pastikan file dataset bernama:

```bash
student_mental_health_clean.csv
```

Letakkan file tersebut ke dalam folder:

```bash
burniva-capstone/datascience/dashboard/
```

Struktur file yang dibutuhkan kurang lebih seperti berikut:

```bash
burniva-capstone/
└── datascience/
    ├── requirements.txt
    └── dashboard/
        ├── dashboard.py
        └── student_mental_health_clean.csv
```

## Setup Environment - Anaconda

```bash
git clone https://github.com/mhnaufal1/burniva-capstone.git
cd burniva-capstone/datascience
conda create --name burniva-ds python=3.9
conda activate burniva-ds
pip install -r requirements.txt
```

## Setup Environment - Terminal/Shell

```bash
git clone https://github.com/mhnaufal1/burniva-capstone.git
cd burniva-capstone/datascience
pip install pipenv
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App

Pastikan posisi terminal berada di folder:

```bash
burniva-capstone/datascience
```

Kemudian jalankan aplikasi Streamlit:

```bash
streamlit run dashboard/dashboard.py
```

Atau masuk terlebih dahulu ke folder dashboard:

```bash
cd dashboard
streamlit run dashboard.py
```

## Catatan Penting

Dashboard membutuhkan file dataset `student_mental_health_clean.csv`.

Jika file belum diletakkan di folder `datascience/dashboard`, aplikasi dapat menampilkan error karena dataset tidak ditemukan.
