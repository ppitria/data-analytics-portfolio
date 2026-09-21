from menu.cari_pegawai import cari_pegawai
from menu.update_data_pegawai import update_nama
from menu.etl import etl

def menu():
    print("="*15, " SISTEM SIMULASI KEPEGAWAIAN & ETL ", "="*15)
    print("1. Cari Pegawai")
    print("2. Update Data Pegawai")
    print("3. ETL Table Analytic")
    print("4. Dashboard & Laporan")
    print("0. KELUAR")

def main():
    while True:
        menu()
        pilihan = input("Masukkan Pilihan Menu: ")

        if pilihan == "1":
            cari_pegawai()
        elif pilihan == "2":
            update_nama()
        elif pilihan == "3":
            etl()
        elif pilihan == "4":
            dashboard_laporan()
        elif pilihan == "0":
            break
        else:
            print("Tidak valid")
            continue


if __name__ == "__main__":
    main()