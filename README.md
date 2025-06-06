# 🗺️ Multi-Mode Graph Navigator - Jawa Timur

Proyek ini adalah aplikasi simulasi graf multimoda yang menggambarkan jaringan jalur antar kota di Jawa Timur, Indonesia. Program memungkinkan pengguna untuk mencari rute tercepat menggunakan algoritma Dijkstra serta menyelesaikan masalah Traveling Salesman Problem (TSP) secara brute-force, berdasarkan moda transportasi: **mobil**, **motor**, atau **jalan kaki**.

## 🔧 Fitur

- 🔄 **Graf multimoda**: Setiap jalur antar kota memiliki bobot berbeda tergantung moda transportasi.
- 🧭 **Dijkstra Algorithm**: Menentukan rute tercepat antar dua kota.
- 🧳 **TSP Brute Force**: Menemukan rute terbaik untuk mengunjungi semua kota satu kali dari kota asal.
- 📊 **Visualisasi**: Menampilkan jaringan kota dan jalur menggunakan Matplotlib.

## 📦 Struktur Program

- `MultiModeGraph`: Struktur data graf dengan simpul kota dan bobot berdasarkan moda.
- `dijkstra()`: Menemukan rute tercepat antar dua kota.
- `tsp_brute_force()`: Menghitung rute optimal mengunjungi semua kota (berawal dari Surabaya).
- `visualisasi_graph()`: Menampilkan graf secara visual.
- `graf_kota()`: Inisialisasi data kota dan jalur.
- `main()`: Antarmuka berbasis terminal untuk menjalankan simulasi.

## 🚀 Cara Menjalankan

1. Pastikan Python dan pustaka `matplotlib` telah terinstal:

```bash
pip install matplotlib
