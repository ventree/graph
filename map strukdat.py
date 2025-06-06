import heapq
import itertools
import matplotlib.pyplot as plt

# ===== Struktur Graph Multimoda =====
class MultiModeGraph:
    def __init__(self):
        self.vertices = set()
        self.edges = {}

    def tambah_kota(self, nama):
        self.vertices.add(nama)
        self.edges[nama] = []

    def tambah_jalan(self, dari, ke, waktu_mobil, waktu_motor, waktu_jalan,
                     jarak_mobil, jarak_motor, jarak_jalan):
        bobot = {
            "mobil": {"waktu": waktu_mobil, "jarak": jarak_mobil},
            "motor": {"waktu": waktu_motor, "jarak": jarak_motor},
            "jalan": {"waktu": waktu_jalan, "jarak": jarak_jalan}
        }
        self.edges[dari].append((ke, bobot))
        self.edges[ke].append((dari, bobot))

    def dijkstra(self, awal, tujuan, moda):
        antrian = [(0, 0, awal, [])]
        sudah_dikunjungi = set()

        while antrian:
            waktu, jarak, kota, jalur = heapq.heappop(antrian)
            if kota in sudah_dikunjungi:
                continue
            sudah_dikunjungi.add(kota)
            jalur = jalur + [kota]

            if kota == tujuan:
                return waktu, jarak, jalur

            for tetangga, bobot in self.edges[kota]:
                if tetangga not in sudah_dikunjungi:
                    waktu_tambah = bobot[moda]["waktu"]
                    jarak_tambah = bobot[moda]["jarak"]
                    heapq.heappush(antrian, (waktu + waktu_tambah, jarak + jarak_tambah, tetangga, jalur))

        return float('inf'), float('inf'), []

    def tsp_brute_force(self, moda):
        kota_list = list(self.vertices)
        min_waktu = float('inf')
        min_jarak = float('inf')
        rute_terbaik = None

        start = "Surabaya"
        remaining = [k for k in kota_list if k != start]

        for perm in itertools.permutations(remaining):
            urutan = (start,) + perm
            total_waktu = 0
            total_jarak = 0
            valid = True
            for i in range(len(urutan) - 1):
                tetangga_dict = {n: w for n, w in self.edges[urutan[i]]}
                if urutan[i + 1] in tetangga_dict:
                    total_waktu += tetangga_dict[urutan[i + 1]][moda]["waktu"]
                    total_jarak += tetangga_dict[urutan[i + 1]][moda]["jarak"]
                else:
                    valid = False
                    break
            if valid and total_waktu < min_waktu:
                min_waktu = total_waktu
                min_jarak = total_jarak
                rute_terbaik = urutan

        return min_waktu, min_jarak, rute_terbaik

# ===== Koordinat untuk visualisasi =====
KOTA_POSISI = {
    "Surabaya": (8, 6),
    "Sidoarjo": (8, 5),
    "Gresik": (7, 6),
    "Lamongan": (6, 6),
    "Mojokerto": (7, 5),
    "Jombang": (6, 5),
    "Malang": (9, 4),
    "Blitar": (7, 3),
    "Kediri": (6, 4),
    "Pasuruan": (9, 5),
}

def visualisasi_graph(graf, rute_dijkstra=None, rute_tsp=None):
    plt.figure(figsize=(10, 7))
    ax = plt.gca()
    ax.set_title("Peta Jalur Antar Kota di Jawa Timur", fontsize=14)

    # Gambar semua edge
    for kota in graf.edges:
        for tetangga, _ in graf.edges[kota]:
            if (kota, tetangga) in graf.edges or (tetangga, kota) in graf.edges:
                x1, y1 = KOTA_POSISI[kota]
                x2, y2 = KOTA_POSISI[tetangga]
                plt.plot([x1, x2], [y1, y2], color="gray", linestyle="--", zorder=1)

    # Rute Dijkstra
    if rute_dijkstra:
        for i in range(len(rute_dijkstra) - 1):
            kota1 = rute_dijkstra[i]
            kota2 = rute_dijkstra[i + 1]
            x1, y1 = KOTA_POSISI[kota1]
            x2, y2 = KOTA_POSISI[kota2]
            plt.plot([x1, x2], [y1, y2], color="red", linewidth=2.5, label="Dijkstra Route" if i == 0 else "", zorder=3)

    # Rute TSP
    if rute_tsp:
        for i in range(len(rute_tsp) - 1):
            kota1 = rute_tsp[i]
            kota2 = rute_tsp[i + 1]
            x1, y1 = KOTA_POSISI[kota1]
            x2, y2 = KOTA_POSISI[kota2]
            plt.plot([x1, x2], [y1, y2], color="green", linewidth=2, label="TSP Route" if i == 0 else "", zorder=2)

    # Titik kota
    for kota, (x, y) in KOTA_POSISI.items():
        plt.scatter(x, y, color="skyblue", edgecolor="black", s=300, zorder=4)
        plt.text(x, y, kota, fontsize=9, ha="center", va="center", zorder=5)

    plt.axis('off')
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.tight_layout()
    plt.show()

# ===== Data Kota dan Jalur =====
def graf_kota():
    kota_list = [
        "Surabaya", "Sidoarjo", "Gresik", "Lamongan", "Mojokerto",
        "Jombang", "Malang", "Blitar", "Kediri", "Pasuruan"
    ]
    graf = MultiModeGraph()
    for kota in kota_list:
        graf.tambah_kota(kota)

    jalur = [
        ("Surabaya", "Sidoarjo", 0.5, 0.4, 1.5, 25, 20, 15),
        ("Surabaya", "Gresik", 0.6, 0.5, 2.0, 30, 25, 18),
        ("Surabaya", "Mojokerto", 1.0, 0.8, 2.5, 60, 50, 40),
        ("Surabaya", "Pasuruan", 1.2, 1.0, 2.8, 65, 55, 45),
        ("Sidoarjo", "Pasuruan", 0.9, 0.7, 2.2, 40, 35, 30),
        ("Sidoarjo", "Malang", 1.5, 1.3, 3.0, 70, 60, 50),
        ("Sidoarjo", "Mojokerto", 1.0, 0.9, 2.4, 45, 40, 35),
        ("Gresik", "Lamongan", 1.0, 0.8, 2.2, 50, 45, 38),
        ("Lamongan", "Mojokerto", 1.3, 1.1, 2.6, 60, 55, 45),
        ("Mojokerto", "Jombang", 1.2, 1.0, 2.4, 55, 50, 42),
        ("Mojokerto", "Kediri", 1.5, 1.3, 2.8, 70, 60, 50),
        ("Jombang", "Kediri", 1.0, 0.9, 2.2, 45, 40, 35),
        ("Jombang", "Blitar", 1.8, 1.6, 3.4, 80, 70, 60),
        ("Malang", "Blitar", 1.5, 1.3, 3.0, 70, 65, 55),
        ("Malang", "Pasuruan", 1.1, 0.9, 2.5, 50, 45, 40),
        ("Blitar", "Kediri", 1.0, 0.8, 2.1, 40, 35, 30),
        ("Gresik", "Sidoarjo", 1.0, 0.8, 2.0, 45, 40, 30),
        ("Lamongan", "Jombang", 1.4, 1.2, 2.5, 60, 55, 48),
        ("Lamongan", "Kediri", 1.6, 1.4, 2.9, 75, 65, 55),
        ("Pasuruan", "Jombang", 1.7, 1.5, 3.2, 85, 75, 65),
        ("Pasuruan", "Kediri", 1.9, 1.6, 3.5, 90, 80, 70),
        ("Malang", "Jombang", 1.5, 1.3, 3.0, 70, 65, 55),
        ("Malang", "Kediri", 1.7, 1.5, 3.2, 75, 70, 60),
        ("Blitar", "Mojokerto", 2.0, 1.8, 3.6, 90, 85, 75),
        ("Blitar", "Lamongan", 2.1, 1.9, 3.7, 95, 90, 80),
        ("Sidoarjo", "Blitar", 2.2, 2.0, 3.9, 100, 95, 85),
        ("Gresik", "Kediri", 2.3, 2.0, 4.0, 105, 95, 85),
        ("Gresik", "Blitar", 2.4, 2.1, 4.2, 110, 100, 90),
        ("Lamongan", "Pasuruan", 2.5, 2.2, 4.4, 115, 105, 95),
        ("Jombang", "Surabaya", 2.6, 2.3, 4.5, 120, 110, 100)
    ]

    for data in jalur:
        graf.tambah_jalan(*data)

    return graf, kota_list

# ===== Program Utama =====
def main():
    graf, kota_list = graf_kota()

    print("=== RUTE TERCEPAT MENGGUNAKAN DIJKSTRA ===")
    print("Daftar kota:", ', '.join(kota_list))

    moda = input("Pilih transportasi (mobil/motor/jalan): ").strip().lower()
    asal = input("Masukkan kota asal anda: ").strip().title()
    tujuan = input("Masukkan kota tujuan anda: ").strip().title()

    if asal not in kota_list or tujuan not in kota_list:
        print("❌ Nama kota tidak valid.")
        return

    if moda not in ["mobil", "motor", "jalan"]:
        print("❌ Moda transportasi tidak tersedia.")
        return

    waktu, jarak, jalur = graf.dijkstra(asal, tujuan, moda)
    if jalur:
        print(f"\n✅ Rute tercepat dari {asal} ke {tujuan} dengan {moda}:")
        print(" -> ".join(jalur))
        print(f"Total waktu: {waktu:.2f} jam")
        print(f"Total jarak: {jarak:.2f} km\n")
    else:
        print("❌ Tidak ditemukan rute yang valid.\n")

    print("=== RUTE TSP TERBAIK (Semua kota dikunjungi sekali) ===")
    waktu_tsp, jarak_tsp, rute_tsp = graf.tsp_brute_force(moda)
    if rute_tsp:
        print(f"📍 Rute TSP: {' -> '.join(rute_tsp)}")
        print(f"Total waktu: {waktu_tsp:.2f} jam")
        print(f"Total jarak: {jarak_tsp:.2f} km\n")
    else:
        print("❌ Tidak ditemukan rute TSP yang valid.\n")

    # TAMPILKAN GRAF
    visualisasi_graph(graf, rute_dijkstra=jalur, rute_tsp=rute_tsp)

if __name__ == "__main__":
    main()
