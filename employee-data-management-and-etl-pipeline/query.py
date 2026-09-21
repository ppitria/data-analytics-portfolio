# ===== NIP PEGAWAI
CARI_PEGAWAI = """
    SELECT 
        p.nip,
        p.nama_lengkap,
        p.tempat_lahir,
        p.tanggal_lahir,
        p.jenis_kelamin,
        p.jenis_asn,
        a.nama_agama,
        pd.jenjang,
        i.nama_instansi,
        j.nama_jabatan,
        pk.nama_pangkat,
        p.tanggal_masuk,
        p.status_pegawai,
        p.alamat
    FROM operational.pegawai p
    JOIN operational.agama a
        ON p.agama_id = a.agama_id
    JOIN operational.pendidikan pd
        ON p.pendidikan_terakhir_id = pd.pendidikan_id
    JOIN operational.instansi i
        ON p.instansi_id = i.instansi_id
    JOIN operational.jabatan j
        ON p.jabatan_id = j.jabatan_id
    JOIN operational.pangkat pk
        ON p.pangkat_id = pk.pangkat_id
    WHERE p.nip = %s;
"""

# ===== UPDATE DATA
CHECK_NIP = """
        SELECT nip, nama_lengkap 
        FROM operational.pegawai
        WHERE nip = %s;
    """

# NAMA
U_NAMA = """
    UPDATE operational.pegawai
    SET nama_lengkap = %s, updated_at = CURRENT_TIMESTAMP
    WHERE nip = %s
"""

# ===== ETL ANALYTIC KEPEGAWAIAN
GET_DATA_PEGAWAI = """
    SELECT
        p.pegawai_id,
        p.nip,
        p.nama_lengkap,
        p.jenis_kelamin,
        p.tanggal_lahir,
        p.tanggal_masuk,
        p.status_pegawai,
        p.jenis_asn,
        a.nama_agama,
        pd.jenjang,
    
        j.nama_jabatan,
        j.jenis_jabatan,
        pk.golongan,
        pk.nama_pangkat,
        i.nama_instansi,
        i.jenis_instansi,
        i.provinsi

    FROM operational.pegawai p

    JOIN operational.agama a
        ON p.agama_id = a.agama_id
        
    JOIN operational.pendidikan pd
        ON p.pendidikan_terakhir_id = pd.pendidikan_id

    JOIN operational.jabatan j
        ON p.jabatan_id = j.jabatan_id

    JOIN operational.pangkat pk
        ON p.pangkat_id = pk.pangkat_id

    JOIN operational.instansi i
        ON p.instansi_id = i.instansi_id;
"""

GET_KINERJA = """
    SELECT
        pegawai_id,
        ROUND(AVG(nilai), 2) AS rata_rata,
        (
            SELECT predikat
            FROM operational.kinerja k2
            WHERE k2.pegawai_id = k1.pegawai_id
            ORDER BY periode DESC
            LIMIT 1
        ) AS predikat_terakhir
    FROM operational.kinerja k1
    GROUP BY pegawai_id;
"""

GET_CUTI = """
    SELECT
        pegawai_id,
        COUNT(*) AS jumlah_cuti
    FROM operational.cuti
    WHERE status = 'Disetujui'
    GROUP BY pegawai_id;
"""

GET_MUTASI = """
    SELECT DISTINCT
        pegawai_id,
        TRUE
    FROM operational.mutasi
"""

I_DATA = """
    INSERT INTO warehouse.analytic_kepegawaian (
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
        pernah_mutasi,
        tanggal_snapshot
    )
    VALUES (
        %s,%s,%s,%s, %s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,CURRENT_TIMESTAMP
    )
"""
