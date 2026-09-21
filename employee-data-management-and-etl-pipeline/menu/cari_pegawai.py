from connection import conn
from query import CARI_PEGAWAI

def get_data_pegawai(nip):
    cur = conn.cursor()
    cur.execute(CARI_PEGAWAI, (nip,))
    pegawai = cur.fetchone()
    cur.close()

    return pegawai

# =====================================================
# CARI PEGAWAI
# =====================================================

def cari_pegawai():
    nip = input("Masukkan NIP pegawai yang akan dicari: ").strip()
    pegawai = get_data_pegawai(nip)

    if pegawai:
        print("="*26, " DATA PEGAWAI ", "="*26)
        print(f"NIP             : {pegawai[0]}")
        print(f"Nama Lengkap    : {pegawai[1]}")
        print(f"Tempat Lahir    : {pegawai[2]}")
        print(f"Tanggal Lahir   : {pegawai[3].strftime('%d-%m-%Y')}")
        print(f"Jenis Kelamin   : {pegawai[4]}")
        print(f"Jenis ASN       : {pegawai[5]}")
        print(f"Agama           : {pegawai[6]}")
        print(f"Pendidikan      : {pegawai[7]}")
        print(f"Instansi        : {pegawai[8]}")
        print(f"Jabatan         : {pegawai[9]}")
        print(f"Pangkat         : {pegawai[10]}")
        print(f"Tanggal Masuk   : {pegawai[11].strftime('%d-%m-%Y')}")
        print(f"Status          : {pegawai[12]}")
        print(f"Alamat          : {pegawai[13]}\n")
    else:
        print("Pegawai Tidak Ditemukan")
