from connection import conn
from query import CHECK_NIP, U_NAMA

# ============================================================================
# UPDATE NAMA
# ============================================================================

def update_nama():
    nip = input("Masukkan NIP pegawai: ").strip()
    
    cur = conn.cursor()
    cur.execute(CHECK_NIP, (nip,))
    pegawai = cur.fetchone()

    if not pegawai:
        print("Pegawai tidak ditemukan.")
        cur.close()
        return

    print(f"\nPegawai ditemukan: {pegawai[1]}")
    nama_baru = input("Nama baru: ")

    if nama_baru == "":
        print("Nama tidak boleh kosong")

    cur.execute(U_NAMA, (nama_baru, nip))

    conn.commit()
    print("\nNama berhasil diperbarui")
