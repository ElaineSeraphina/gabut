import time
import os

# Mendefinisikan path file
file1 = "/storage/emulated/0/Proxy/file_proxy.txt"
file2 = "/storage/emulated/0/Proxy/proxy.txt"

# Fungsi untuk memeriksa apakah file baru diperbarui
def is_file_updated(file_path, last_modified_time):
    return os.path.getmtime(file_path) > last_modified_time

# Fungsi untuk membaca konten file dan mengembalikan baris sebagai set (menghapus duplikat secara otomatis)
def read_file(file_path):
    with open(file_path, 'r') as f:
        return set(f.readlines())

# Fungsi untuk menulis konten yang telah diperbarui (tanpa duplikat)
def write_to_file(file_path, content):
    with open(file_path, 'w') as f:
        f.writelines(content)

# Fungsi untuk memeriksa apakah konten di proxy.txt sudah sama dengan file_proxy.txt
def is_content_same(file_path1, file_path2):
    # Membaca konten kedua file
    content1 = read_file(file_path1)
    content2 = read_file(file_path2)
    
    # Membandingkan apakah konten sudah sama
    return content1 == content2

# Menyimpan waktu terakhir file diperiksa
last_modified_time_file1 = os.path.getmtime(file1)

# Menunggu hingga file_proxy.txt diperbarui dan menulis ulang ke proxy.txt
print("Menunggu pembaruan pada file_proxy.txt... Script akan terus berjalan sampai dihentikan.")
while True:
    try:
        # Memeriksa apakah file_proxy.txt telah diperbarui
        if is_file_updated(file1, last_modified_time_file1):
            print("file_proxy.txt diperbarui, mulai menulis ulang ke proxy.txt...")

            # Membaca konten dari kedua file (file_proxy.txt dan proxy.txt)
            file1_content = read_file(file1)
            file2_content = read_file(file2)

            # Menggabungkan konten dan menghilangkan duplikat (hanya menyimpan data yang unik)
            unique_content = file2_content.union(file1_content)

            # Mengecek apakah konten yang digabungkan berbeda dengan yang ada di proxy.txt
            if unique_content != file2_content:
                # Menulis kembali konten unik ke proxy.txt
                write_to_file(file2, sorted(list(unique_content)))  # Menyortir jika diperlukan
                print("Data berhasil ditulis ulang ke proxy.txt tanpa duplikat.")
            else:
                print("Konten proxy.txt sudah terbaru, tidak perlu pembaruan.")

            # Memperbarui waktu terakhir file diperiksa
            last_modified_time_file1 = os.path.getmtime(file1)
        
        # Tunggu sebentar sebelum memeriksa lagi
        time.sleep(5)  # Memeriksa setiap 5 detik
    except KeyboardInterrupt:
        print("\nScript dihentikan oleh pengguna.")
        break