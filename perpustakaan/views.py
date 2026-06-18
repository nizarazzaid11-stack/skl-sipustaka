from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages


# ─────────────────────────── DASHBOARD ───────────────────────────

def dashboard(request):
    with connection.cursor() as cur:
        cur.execute("SELECT COALESCE(SUM(stok), 0) FROM buku")
        total_buku = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM buku")
        total_judul = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam'")
        sedang_dipinjam = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dikembalikan'")
        sudah_dikembalikan = cur.fetchone()[0]

        cur.execute("SELECT judul, stok FROM buku ORDER BY id")
        stok_buku = cur.fetchall()

        cur.execute("""
            SELECT status, COUNT(*) FROM peminjaman GROUP BY status
        """)
        rows = cur.fetchall()
        ringkasan = {r[0]: r[1] for r in rows}

    max_stok = max((s[1] for s in stok_buku), default=1) or 1

    return render(request, 'perpustakaan/dashboard.html', {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'stok_buku': stok_buku,
        'max_stok': max_stok,
        'ringkasan': ringkasan,
    })


# ─────────────────────────── BUKU ───────────────────────────

KATEGORI_CHOICES = ['Novel', 'Sejarah', 'Pendidikan']
RAK_CHOICES = ['Rak A-01', 'Rak A-02', 'Rak A-03', 'Rak A-04', 'Rak A-05']


def buku_list(request):
    with connection.cursor() as cur:
        cur.execute("SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok FROM buku ORDER BY id")
        buku_list = cur.fetchall()
    return render(request, 'perpustakaan/buku_list.html', {'buku_list': buku_list})


def buku_tambah(request):
    errors = {}
    data = {}
    if request.method == 'POST':
        data = request.POST
        judul      = data.get('judul', '').strip()
        pengarang  = data.get('pengarang', '').strip()
        kategori   = data.get('kategori', '').strip()
        penerbit   = data.get('penerbit', '').strip()
        tahun      = data.get('tahun_terbit', '').strip()
        rak        = data.get('rak', '').strip()
        stok       = data.get('stok', '').strip()
        deskripsi  = data.get('deskripsi', '').strip()

        if not judul:       errors['judul'] = 'Judul wajib diisi.'
        if not pengarang:   errors['pengarang'] = 'Pengarang wajib diisi.'
        if not kategori:    errors['kategori'] = 'Kategori wajib dipilih.'
        if not penerbit:    errors['penerbit'] = 'Penerbit wajib diisi.'
        if not tahun:       errors['tahun_terbit'] = 'Tahun terbit wajib diisi.'
        elif not tahun.isdigit(): errors['tahun_terbit'] = 'Tahun harus angka.'
        if not rak:         errors['rak'] = 'Rak wajib dipilih.'
        if not stok:        errors['stok'] = 'Stok wajib diisi.'
        elif not stok.isdigit(): errors['stok'] = 'Stok harus angka.'

        if not errors:
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [judul, pengarang, kategori, penerbit, int(tahun), rak, int(stok), deskripsi])
            messages.success(request, 'Buku berhasil ditambahkan.')
            return redirect('buku_list')

    return render(request, 'perpustakaan/buku_form.html', {
        'form_title': 'Tambah Buku',
        'kategori_choices': KATEGORI_CHOICES,
        'rak_choices': RAK_CHOICES,
        'errors': errors,
        'data': data,
        'action': 'tambah',
    })


def buku_detail(request, pk):
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM buku WHERE id = %s", [pk])
        row = cur.fetchone()
        if not row:
            messages.error(request, 'Buku tidak ditemukan.')
            return redirect('buku_list')
        cols = [d[0] for d in cur.description]
        buku = dict(zip(cols, row))
    return render(request, 'perpustakaan/buku_detail.html', {'buku': buku})


def buku_edit(request, pk):
    errors = {}
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM buku WHERE id = %s", [pk])
        row = cur.fetchone()
        if not row:
            messages.error(request, 'Buku tidak ditemukan.')
            return redirect('buku_list')
        cols = [d[0] for d in cur.description]
        buku = dict(zip(cols, row))

    if request.method == 'POST':
        data = request.POST
        judul      = data.get('judul', '').strip()
        pengarang  = data.get('pengarang', '').strip()
        kategori   = data.get('kategori', '').strip()
        penerbit   = data.get('penerbit', '').strip()
        tahun      = data.get('tahun_terbit', '').strip()
        rak        = data.get('rak', '').strip()
        stok       = data.get('stok', '').strip()
        deskripsi  = data.get('deskripsi', '').strip()

        if not judul:       errors['judul'] = 'Judul wajib diisi.'
        if not pengarang:   errors['pengarang'] = 'Pengarang wajib diisi.'
        if not kategori:    errors['kategori'] = 'Kategori wajib dipilih.'
        if not penerbit:    errors['penerbit'] = 'Penerbit wajib diisi.'
        if not tahun:       errors['tahun_terbit'] = 'Tahun terbit wajib diisi.'
        elif not tahun.isdigit(): errors['tahun_terbit'] = 'Tahun harus angka.'
        if not rak:         errors['rak'] = 'Rak wajib dipilih.'
        if not stok:        errors['stok'] = 'Stok wajib diisi.'
        elif not stok.isdigit(): errors['stok'] = 'Stok harus angka.'

        if not errors:
            with connection.cursor() as cur:
                cur.execute("""
                    UPDATE buku SET judul=%s, pengarang=%s, kategori=%s, penerbit=%s,
                    tahun_terbit=%s, rak=%s, stok=%s, deskripsi=%s WHERE id=%s
                """, [judul, pengarang, kategori, penerbit, int(tahun), rak, int(stok), deskripsi, pk])
            messages.success(request, 'Buku berhasil diperbarui.')
            return redirect('buku_list')

        buku.update({'judul': judul, 'pengarang': pengarang, 'kategori': kategori,
                     'penerbit': penerbit, 'tahun_terbit': tahun, 'rak': rak,
                     'stok': stok, 'deskripsi': deskripsi})

    return render(request, 'perpustakaan/buku_form.html', {
        'form_title': 'Edit Buku',
        'kategori_choices': KATEGORI_CHOICES,
        'rak_choices': RAK_CHOICES,
        'errors': errors,
        'data': buku,
        'action': 'edit',
        'pk': pk,
    })


def buku_hapus(request, pk):
    with connection.cursor() as cur:
        cur.execute("SELECT judul FROM buku WHERE id = %s", [pk])
        row = cur.fetchone()
        if not row:
            messages.error(request, 'Buku tidak ditemukan.')
            return redirect('buku_list')
    if request.method == 'POST':
        with connection.cursor() as cur:
            cur.execute("DELETE FROM buku WHERE id = %s", [pk])
        messages.success(request, 'Buku berhasil dihapus.')
        return redirect('buku_list')
    return render(request, 'perpustakaan/buku_hapus.html', {'judul': row[0], 'pk': pk})


# ─────────────────────────── SISWA ───────────────────────────

def siswa_list(request):
    with connection.cursor() as cur:
        cur.execute("SELECT id, nama, kelas, nis, is_active FROM siswa ORDER BY id")
        siswa_list = cur.fetchall()
    return render(request, 'perpustakaan/siswa_list.html', {'siswa_list': siswa_list})


def siswa_tambah(request):
    errors = {}
    data = {}
    if request.method == 'POST':
        data = request.POST
        nama      = data.get('nama', '').strip()
        kelas     = data.get('kelas', '').strip()
        nis       = data.get('nis', '').strip()
        is_active = data.get('is_active', 'false')

        if not nama:  errors['nama'] = 'Nama wajib diisi.'
        if not kelas: errors['kelas'] = 'Kelas wajib diisi.'
        if not nis:   errors['nis'] = 'NIS wajib diisi.'
        else:
            with connection.cursor() as cur:
                cur.execute("SELECT id FROM siswa WHERE nis = %s", [nis])
                if cur.fetchone():
                    errors['nis'] = 'NIS sudah terdaftar.'

        if not errors:
            aktif = True if is_active == 'true' else False
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO siswa (nama, kelas, nis, is_active) VALUES (%s, %s, %s, %s)
                """, [nama, kelas, nis, aktif])
            messages.success(request, 'Siswa berhasil ditambahkan.')
            return redirect('siswa_list')

    return render(request, 'perpustakaan/siswa_form.html', {
        'form_title': 'Tambah User',
        'errors': errors,
        'data': data,
        'action': 'tambah',
    })


def siswa_detail(request, pk):
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM siswa WHERE id = %s", [pk])
        row = cur.fetchone()
        if not row:
            messages.error(request, 'Siswa tidak ditemukan.')
            return redirect('siswa_list')
        cols = [d[0] for d in cur.description]
        siswa = dict(zip(cols, row))
        cur.execute("""
            SELECT p.id, b.judul, p.tanggal_pinjam, p.jatuh_tempo, p.status
            FROM peminjaman p JOIN buku b ON p.buku_id = b.id
            WHERE p.siswa_id = %s ORDER BY p.id DESC
        """, [pk])
        peminjaman = cur.fetchall()
    return render(request, 'perpustakaan/siswa_detail.html', {'siswa': siswa, 'peminjaman': peminjaman})


def siswa_edit(request, pk):
    errors = {}
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM siswa WHERE id = %s", [pk])
        row = cur.fetchone()
        if not row:
            messages.error(request, 'Siswa tidak ditemukan.')
            return redirect('siswa_list')
        cols = [d[0] for d in cur.description]
        siswa = dict(zip(cols, row))

    if request.method == 'POST':
        data = request.POST
        nama      = data.get('nama', '').strip()
        kelas     = data.get('kelas', '').strip()
        nis       = data.get('nis', '').strip()
        is_active = data.get('is_active', 'false')

        if not nama:  errors['nama'] = 'Nama wajib diisi.'
        if not kelas: errors['kelas'] = 'Kelas wajib diisi.'
        if not nis:   errors['nis'] = 'NIS wajib diisi.'
        else:
            with connection.cursor() as cur:
                cur.execute("SELECT id FROM siswa WHERE nis = %s AND id != %s", [nis, pk])
                if cur.fetchone():
                    errors['nis'] = 'NIS sudah digunakan siswa lain.'

        if not errors:
            aktif = True if is_active == 'true' else False
            with connection.cursor() as cur:
                cur.execute("""
                    UPDATE siswa SET nama=%s, kelas=%s, nis=%s, is_active=%s WHERE id=%s
                """, [nama, kelas, nis, aktif, pk])
            messages.success(request, 'Data siswa berhasil diperbarui.')
            return redirect('siswa_list')

        siswa.update({'nama': nama, 'kelas': kelas, 'nis': nis, 'is_active': is_active == 'true'})

    return render(request, 'perpustakaan/siswa_form.html', {
        'form_title': 'Edit User',
        'errors': errors,
        'data': siswa,
        'action': 'edit',
        'pk': pk,
    })


def siswa_hapus(request, pk):
    with connection.cursor() as cur:
        cur.execute("SELECT nama FROM siswa WHERE id = %s", [pk])
        row = cur.fetchone()
        if not row:
            messages.error(request, 'Siswa tidak ditemukan.')
            return redirect('siswa_list')
    if request.method == 'POST':
        with connection.cursor() as cur:
            cur.execute("DELETE FROM siswa WHERE id = %s", [pk])
        messages.success(request, 'Siswa berhasil dihapus.')
        return redirect('siswa_list')
    return render(request, 'perpustakaan/siswa_hapus.html', {'nama': row[0], 'pk': pk})


# ─────────────────────────── PEMINJAMAN ───────────────────────────

STATUS_CHOICES = ['Dipinjam', 'Dikembalikan', 'Terlambat']


def peminjaman_list(request):
    with connection.cursor() as cur:
        cur.execute("""
            SELECT p.id, s.nama, b.judul, p.tanggal_pinjam, p.jatuh_tempo,
                   p.keperluan, p.status
            FROM peminjaman p
            JOIN siswa s ON p.siswa_id = s.id
            JOIN buku b ON p.buku_id = b.id
            ORDER BY p.id DESC
        """)
        peminjaman_list = cur.fetchall()
    return render(request, 'perpustakaan/peminjaman_list.html', {'peminjaman_list': peminjaman_list})


def peminjaman_tambah(request):
    errors = {}
    data = {}
    with connection.cursor() as cur:
        cur.execute("SELECT id, nama, kelas FROM siswa WHERE is_active = TRUE ORDER BY nama")
        siswa_list = cur.fetchall()
        cur.execute("SELECT id, judul, stok FROM buku WHERE stok > 0 ORDER BY judul")
        buku_list = cur.fetchall()

    if request.method == 'POST':
        data = request.POST
        siswa_id       = data.get('siswa_id', '').strip()
        buku_id        = data.get('buku_id', '').strip()
        tanggal_pinjam = data.get('tanggal_pinjam', '').strip()
        jatuh_tempo    = data.get('jatuh_tempo', '').strip()
        keperluan      = data.get('keperluan', '').strip()
        status         = data.get('status', 'Dipinjam').strip()

        if not siswa_id:       errors['siswa_id'] = 'Peminjam wajib dipilih.'
        if not buku_id:        errors['buku_id'] = 'Buku wajib dipilih.'
        if not tanggal_pinjam: errors['tanggal_pinjam'] = 'Tanggal pinjam wajib diisi.'
        if not jatuh_tempo:    errors['jatuh_tempo'] = 'Jatuh tempo wajib diisi.'
        if not keperluan:      errors['keperluan'] = 'Keperluan wajib diisi.'

        if not errors:
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status])
            messages.success(request, 'Peminjaman berhasil dicatat.')
            return redirect('peminjaman_list')

    return render(request, 'perpustakaan/peminjaman_form.html', {
        'form_title': 'Tambah Peminjaman',
        'siswa_list': siswa_list,
        'buku_list': buku_list,
        'status_choices': STATUS_CHOICES,
        'errors': errors,
        'data': data,
    })


def peminjaman_kembalikan(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cur:
            cur.execute("UPDATE peminjaman SET status = 'Dikembalikan' WHERE id = %s", [pk])
        messages.success(request, 'Status peminjaman diperbarui menjadi Dikembalikan.')
    return redirect('peminjaman_list')
