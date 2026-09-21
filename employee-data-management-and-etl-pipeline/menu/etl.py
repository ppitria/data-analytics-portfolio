from connection import conn
from query import *
from datetime import date
from psycopg2.extras import execute_batch

cur = conn.cursor()
TODAY = date.today()

# ============================================================================
# MAPPING GENERASI
# ============================================================================

def get_generasi(tahun):
    if tahun <= 1964:
        return 'Baby Boomers (1946-1964)'
    elif tahun <= 1980:
        return 'Gen X (1965-1980)'
    elif tahun <= 1996:
        return 'Milenial (1981-1996)'
    else:
        return 'Gen Z (1997-2012)'

# ============================================================================
# MAPPING KELOMPOK UMUR
# ============================================================================

def get_kelompok_umur(umur):
    if umur > 60:
        return '>60'
    elif umur >= 51:
        return '51 - 60'
    elif umur >= 41:
        return '41 - 50'
    elif umur >= 31:
        return '31 - 40'
    elif umur >= 21:
        return '21 - 30'

    return '18 - 20'


# ============================================================================
# MAPPING KELOMPOK MASA KERJA
# ============================================================================

def get_kelompok_masa_kerja(masa_kerja):
    if masa_kerja <= 5:
        return '1 - 5'
    elif masa_kerja <= 10:
        return '6 - 10'
    elif masa_kerja <= 15:
        return '11 - 15'
    elif masa_kerja <= 20:
        return '16 - 20'
    elif masa_kerja <= 25:
        return '21 - 25'
    elif masa_kerja <= 30:
        return '26 - 30'
    elif masa_kerja > 30:
        return '> 30'

# ============================================================================
# EXTRACT TRANSFORM LOAD
# ============================================================================

def etl_data_pegawai(kinerja_dict, cuti_dict, mutasi_dict):
    try:
        print("Memulai ETL data analytic kepegawaian...")

        # EXTRACT
        cur.execute(GET_DATA_PEGAWAI)
        rows = cur.fetchall()

        # TRANSFORM
        transformed = []

        for row in rows:
            (
                pegawai_id,
                nip,
                nama_lengkap,
                jenis_kelamin,
                tanggal_lahir,
                tanggal_masuk,
                status_pegawai,
                jenis_asn,
                nama_agama,
                nama_pendidikan,
            
                nama_jabatan,
                jenis_jabatan,
                golongan,
                nama_pangkat,
                nama_instansi,
                jenis_instansi,
                provinsi

            ) = row

            umur = (TODAY.year - tanggal_lahir.year - ((TODAY.month, TODAY.day) < (tanggal_lahir.month, tanggal_lahir.day)))
            tahun_lahir = tanggal_lahir.year
            tahun_masuk = tanggal_masuk.year

            kelompok_umur = get_kelompok_umur(umur)
            generasi = get_generasi(tahun_lahir)
            masa_kerja = TODAY.year - tahun_masuk
            kelompok_masa_kerja = get_kelompok_masa_kerja(masa_kerja)
            agama = nama_agama
            pendidikan = nama_pendidikan

            jabatan = nama_jabatan
            instansi = nama_instansi

            rata_rata_kinerja, predikat_kinerja_terakhir = kinerja_dict.get(pegawai_id, (0, 'Belum Ada'))
            jumlah_cuti = cuti_dict.get(pegawai_id, 0)
            pernah_mutasi = mutasi_dict.get(pegawai_id, False)

            transformed.append(
                (
                    pegawai_id,
                    nip,
                    nama_lengkap,
                    jenis_kelamin,
                    
                    umur,
                    kelompok_umur,
                    generasi,

                    tahun_lahir,
                    tahun_masuk,
                    masa_kerja,
                    kelompok_masa_kerja,

                    status_pegawai,
                    jenis_asn,
                    agama,
                    pendidikan,

                    jabatan,
                    jenis_jabatan,
                    golongan,
                    nama_pangkat,
                    instansi,
                    jenis_instansi,
                    provinsi,

                    predikat_kinerja_terakhir,
                    rata_rata_kinerja,
                    jumlah_cuti,
                    pernah_mutasi
                )
            )

        # LOAD
        if transformed:
            execute_batch(
                cur,
                I_DATA,
                transformed,
                page_size=1000
            )
        else:
            print("Tidak ada data")
        
        conn.commit()

        print(f"{len(transformed)} row berhasil diproses, ETL sukses")
    
    except Exception as e:
        conn.rollback()
        print(f"ETL gagal: {e}")

def etl():
    cur.execute(GET_KINERJA)
    kinerja_dict = {
        row[0]: (row[1], row[2])
        for row in cur.fetchall()
    }

    cur.execute(GET_CUTI)
    cuti_dict = dict(cur.fetchall())

    cur.execute(GET_MUTASI)
    mutasi_dict = dict(cur.fetchall())

    etl_data_pegawai(kinerja_dict, cuti_dict, mutasi_dict)

    cur.close()
    conn.close()