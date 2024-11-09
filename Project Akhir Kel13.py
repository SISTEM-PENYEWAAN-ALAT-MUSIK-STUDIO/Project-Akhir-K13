import json
import pwinput
import os
from datetime import datetime, timedelta
from prettytable import PrettyTable

#  file untuk penyimpanan data
USER_FILE = 'User.json'
BARANG_FILE = 'Barang.json'

# Fungsi untuk membaca data pengguna dari file JSON
def baca_users():
    try:
        with open(USER_FILE, 'r') as f:
            return json.load(f)["users"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

#   membaca data produk dari file JSON
def baca_products():
    try:
        with open(BARANG_FILE, 'r') as f:
            return json.load(f)["Barang"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

#  untuk menyimpan data pengguna ke file JSON
def simpan_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump({"users": users}, f, indent=4)

#  untuk menyimpan data produk ke file JSON
def simpan_products(products):
    with open(BARANG_FILE, 'w') as f:
        json.dump({"Barang": products}, f, indent=4)

#   menambah saldo
def tambah_saldo(username):
    users = baca_users()
    for user in users:
        if user["username"] == username:
            try:
                jumlah = int(input("Masukkan jumlah saldo yang ingin ditambahkan: "))
                if jumlah <= 0:
                    print("Jumlah saldo harus positif.")
                    return
                user["saldo"] = int(user["saldo"]) + jumlah
                simpan_users(users)
                print(f"Saldo berhasil ditambahkan. Saldo saat ini: {user['saldo']}")
            except ValueError:
                print("Input tidak valid. Harap masukkan angka.")
            return
    print("Pengguna tidak ditemukan.")

#  mengecek saldo
def cek_saldo(username):
    users = baca_users()
    for user in users:
        if user["username"] == username:
            print(f"Saldo Anda saat ini adalah: {user['saldo']}")
            return
    print("Pengguna tidak ditemukan.")

#  menyewa barang
def sewa_barang(username):
    users = baca_users()
    products = baca_products()

    user = next((u for u in users if u["username"] == username), None)
    if not user:
        print("Pengguna tidak ditemukan.")
        return
    
    lihat_produk()
    pilihan = input("Masukkan nomor barang yang ingin disewa: ").strip()
    produk = next((p for p in products if p["nomor_barang"] == pilihan), None)
    
    if not produk:
        print("Barang tidak ditemukan.")
        return

    try:
        lama_sewa = int(input("Masukkan lama sewa (dalam hari): "))
        if lama_sewa <= 0:
            print("Lama sewa harus lebih dari 0.")
            return
        tanggal_sewa_str = input("Masukkan tanggal sewa (format: DD-MM-YYYY): ").strip()
        tanggal_sewa = datetime.strptime(tanggal_sewa_str, "%d-%m-%Y")
    except ValueError:
        print("Input tidak valid. Harap masukkan angka untuk lama sewa dan format tanggal yang benar.")
        return

    try:
        harga_per_hari = int(produk["harga_per_hari"])
        stok = int(produk["stok"])
        biaya_sewa = harga_per_hari * lama_sewa
    except ValueError:
        print("Data barang tidak valid. Harap periksa harga atau stok.")
        return

    if int(user["saldo"]) < biaya_sewa:
        print("Saldo tidak cukup untuk menyewa barang ini.")
        return
    if stok <= 0:
        print("Stok barang habis.")
        return

    confirm = input("Apakah Anda ingin melanjutkan penyewaan? (iya/tidak): ").strip().lower()
    if confirm != "iya":
        print("Penyewaan dibatalkan.")
        return

    # Update stok dan saldo
    produk["stok"] = str(stok - 1)
    user["saldo"] = str(int(user["saldo"]) - biaya_sewa)
    simpan_products(products)
    simpan_users(users)

    # Cetak struk
    tanggal_pengembalian = tanggal_sewa + timedelta(days=lama_sewa)
    struk(username, produk, lama_sewa, biaya_sewa, tanggal_sewa, tanggal_pengembalian)
    print("Barang berhasil disewa!")

    # untuk mencetak struk
def struk(username, produk, lama_sewa, biaya_sewa, tanggal_sewa, tanggal_pengembalian):
    print("\n--- Struk Penyewaan ---")
    print(f"Nama Penyewa      : {username}")
    print(f"Nama Barang       : {produk['nama_barang']}")
    print(f"Lama Sewa         : {lama_sewa} hari")
    print(f"Total Biaya       : {biaya_sewa}")
    print(f"Tanggal Sewa      : {tanggal_sewa.strftime('%d-%m-%Y')}")
    print(f"Tanggal Kembali   : {tanggal_pengembalian.strftime('%d-%m-%Y')}")
    print("------------------------")

# registrasi penyewa
def registrasi():
    users = baca_users()
    username = input("Masukkan username: ").strip()
    password = pwinput.pwinput("Masukkan password: ").strip()
    
    # Cek apakah username sudah terdaftar
    for user in users:
        if user["username"] == username:
            print("Username sudah digunakan.")
            return
    
    # Tambah user baru
    users.append({"username": username, "password": password, "role": "penyewa", "saldo": 0})
    simpan_users(users)
    print("Registrasi berhasil!")

# login
def login(role):
    users = baca_users()
    username = input("Masukkan username: ").strip()
    password = pwinput.pwinput("Masukkan password: ").strip()
    
    for user in users:
        if user["username"] == username and user["password"] == password and user["role"] == role:
            print(f"Login {role} berhasil!")
            return username
    print("Username atau password salah.")
    return None

# untuk menambah produk (khusus admin)
def tambah_produk():
    products = baca_products()
    nomor_barang = input("Masukkan nomor barang: ").strip()
    nama_barang = input("Masukkan nama barang: ").strip()
    harga_per_hari = input("Masukkan harga per hari: ").strip()
    stok = input("Masukkan stok: ").strip()
    
    products.append({"nomor_barang": nomor_barang, "nama_barang": nama_barang, "harga_per_hari": harga_per_hari, "stok": stok})
    simpan_products(products)
    print("Produk berhasil ditambahkan!")

# untuk menampilkan produk
def lihat_produk():
    products = baca_products()
    table = PrettyTable()
    table.field_names = ["No", "Nama Barang", "Harga per Hari", "Stok"]
    print("\nDaftar Barang:")
    for i, produk in enumerate(products, start=1):
        table.add_row([produk['nomor_barang'], produk['nama_barang'], produk['harga_per_hari'], produk['stok']])
    print(table)

# untuk mengupdate produk
def update_produk():
    products = baca_products()
    lihat_produk()
    
    pilihan = input("Masukkan nomor barang yang ingin diupdate: ").strip()
    for produk in products:
        if produk["nomor_barang"] == pilihan:
            print(f"Update barang {produk['nama_barang']}")
            produk["nama_barang"] = input(f"Nama barang ({produk['nama_barang']}): ").strip() or produk["nama_barang"]
            produk["harga_per_hari"] = input(f"Harga per hari ({produk['harga_per_hari']}): ").strip() or produk["harga_per_hari"]
            produk["stok"] = input(f"Stok ({produk['stok']}): ").strip() or produk["stok"]
            simpan_products(products)
            print("Barang berhasil diperbarui!")
            return
    print("Barang tidak ditemukan.")

# untuk menghapus produk
def delete_produk():
    products = baca_products()
    lihat_produk()
    
    pilihan = input("Masukkan nomor barang yang ingin dihapus: ").strip()
    for i, produk in enumerate(products):
        if produk["nomor_barang"] == pilihan:
            products.pop(i)
            simpan_products(products)
            print("Barang berhasil dihapus!")
            return
    print("Barang tidak ditemukan.")

# untuk mencari barang
def search_barang():
    products = baca_products()
    keyword = input("Masukkan nama barang yang ingin dicari: ").strip().lower()
    table = PrettyTable()
    table.field_names = ["No", "Nama Barang", "Harga per Hari", "Stok"]
    found = False
    for produk in products:
        if keyword in produk['nama_barang'].lower():
            table.add_row([produk['nomor_barang'], produk['nama_barang'], produk['harga_per_hari'], produk['stok']])
            found = True
    if found:
        print(table)
    else:
        print("Barang tidak ditemukan.")

# menu admin
def menu_admin():
    while True:
        print("\n--- Menu Admin ---")
        print("1. Tambah Barang")
        print("2. Lihat Barang")
        print("3. Update Barang")
        print("4. Hapus Barang")
        print("5. Logout")
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            os.system("cls")
            tambah_produk()
        elif pilihan == "2":
            os.system("cls")
            lihat_produk()
        elif pilihan == "3":
            os.system("cls")
            update_produk()
        elif pilihan == "4":
            os.system("cls")
            delete_produk()
        elif pilihan == "5":
            os.system("cls")
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")

# menu penyewa
def menu_penyewa(username):
    while True:
        print("\n--- Menu Penyewa ---")
        print("1. Lihat Barang")
        print("2. Cari Barang")
        print("3. Sewa Barang")
        print("4. Tambah Saldo")
        print("5. Cek Saldo")
        print("6. Logout")
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            os.system("cls")
            lihat_produk()
        elif pilihan == "2":
            os.system("cls")
            search_barang()
        elif pilihan == "3":
            os.system("cls")
            sewa_barang(username)
        elif pilihan == "4":
            os.system("cls")
            tambah_saldo(username)
        elif pilihan == "5":
            os.system("cls")
            cek_saldo(username)
        elif pilihan == "6":
            os.system("cls")
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")

# Main Program
def main():
    try: 
        while True:
            print("\n--- Sistem Penyewaan Alat Musik ---")
            print("1. Login sebagai Admin")
            print("2. Login sebagai Penyewa")
            print("3. Registrasi Penyewa")
            print("4. Keluar")
            pilihan = input("Pilih menu: ").strip()
        
            if pilihan == "1":
                os.system("cls")
                if login("admin"):
                    menu_admin()
            elif pilihan == "2":
                os.system("cls")
                username = login("penyewa")
                if username:
                    menu_penyewa(username)
            elif pilihan == "3":
                os.system("cls")
                registrasi()
            elif pilihan == "4":
                os.system("cls")
                print("Terima kasih telah menggunakan sistem ini.")
                break
            else:
                print("Pilihan tidak valid.")
    except KeyboardInterrupt:
        print("\nTidak boleh menggunakan Ctrl+C")

# Buat admin default jika belum ada
def buat_admin_default():
    users = baca_users()
    admin_ada = any(user["role"] == "admin" for user in users)
    if not admin_ada:
        users.append({"username": "admin", "password": "admin123", "role": "admin"})
        simpan_users(users)

# Eksekusi program utama
buat_admin_default()
main()
