from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import Buku, Siswa, Peminjaman


# =========================
# DASHBOARD
# =========================

def dashboard(request):
    total_buku = Buku.objects.aggregate(
        total=Sum('stok')
    )['total'] or 0

    total_judul = Buku.objects.count()
    total_siswa = Siswa.objects.count()

    sedang_dipinjam = Peminjaman.objects.filter(
        sudah_kembali=False
    ).count()

    sudah_dikembalikan = Peminjaman.objects.filter(
        sudah_kembali=True
    ).count()

    stok_buku = Buku.objects.all()

    return render(request, 'perpustakaan/dashboard.html', {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'total_siswa': total_siswa,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'stok_buku': stok_buku,
    })


# =========================
# BUKU
# =========================

def buku_list(request):
    buku_list = Buku.objects.all().order_by('id')

    return render(
        request,
        'perpustakaan/buku_list.html',
        {
            'buku_list': buku_list
        }
    )


def buku_detail(request, pk):
    buku = get_object_or_404(Buku, pk=pk)

    return render(
        request,
        'perpustakaan/buku_detail.html',
        {
            'buku': buku
        }
    )


def buku_tambah(request):
    if request.method == 'POST':
        Buku.objects.create(
            judul=request.POST.get('judul'),
            pengarang=request.POST.get('pengarang'),
            kategori=request.POST.get('kategori'),
            penerbit=request.POST.get('penerbit'),
            tahun=request.POST.get('tahun') or None,
            rak=request.POST.get('rak'),
            stok=request.POST.get('stok') or 0,
        )

        messages.success(
            request,
            'Buku berhasil ditambahkan.'
        )

        return redirect('buku_list')

    return render(
        request,
        'perpustakaan/buku_form.html',
        {
            'form_title': 'Tambah Buku'
        }
    )


def buku_edit(request, pk):
    buku = get_object_or_404(Buku, pk=pk)

    if request.method == 'POST':
        buku.judul = request.POST.get('judul')
        buku.pengarang = request.POST.get('pengarang')
        buku.kategori = request.POST.get('kategori')
        buku.penerbit = request.POST.get('penerbit')
        buku.tahun = request.POST.get('tahun') or None
        buku.rak = request.POST.get('rak')
        buku.stok = request.POST.get('stok') or 0

        buku.save()

        messages.success(
            request,
            'Buku berhasil diperbarui.'
        )

        return redirect('buku_list')

    return render(
        request,
        'perpustakaan/buku_form.html',
        {
            'form_title': 'Edit Buku',
            'buku': buku,
            'action': 'edit',
        }
    )


def buku_hapus(request, pk):
    buku = get_object_or_404(Buku, pk=pk)

    if request.method == 'POST':
        buku.delete()

        messages.success(
            request,
            'Buku berhasil dihapus.'
        )

        return redirect('buku_list')

    return render(
        request,
        'perpustakaan/buku_hapus.html',
        {
            'buku': buku
        }
    )


# =========================
# SISWA
# =========================

def siswa_list(request):
    siswa_list = Siswa.objects.all().order_by('id')

    return render(
        request,
        'perpustakaan/siswa_list.html',
        {
            'siswa_list': siswa_list
        }
    )


def siswa_detail(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)

    peminjaman = Peminjaman.objects.filter(
        siswa=siswa
    ).select_related('buku')

    return render(
        request,
        'perpustakaan/siswa_detail.html',
        {
            'siswa': siswa,
            'peminjaman': peminjaman,
        }
    )


def siswa_tambah(request):
    if request.method == 'POST':
        Siswa.objects.create(
            nama=request.POST.get('nama'),
            kelas=request.POST.get('kelas'),
            nis=request.POST.get('nis'),
        )

        messages.success(
            request,
            'Siswa berhasil ditambahkan.'
        )

        return redirect('siswa_list')

    return render(
        request,
        'perpustakaan/siswa_form.html',
        {
            'form_title': 'Tambah Siswa'
        }
    )


def siswa_edit(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)

    if request.method == 'POST':
        siswa.nama = request.POST.get('nama')
        siswa.kelas = request.POST.get('kelas')
        siswa.nis = request.POST.get('nis')

        siswa.save()

        messages.success(
            request,
            'Data siswa berhasil diperbarui.'
        )

        return redirect('siswa_list')

    return render(
        request,
        'perpustakaan/siswa_form.html',
        {
            'form_title': 'Edit Siswa',
            'siswa': siswa,
            'action': 'edit',
        }
    )


def siswa_hapus(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)

    if request.method == 'POST':
        siswa.delete()

        messages.success(
            request,
            'Siswa berhasil dihapus.'
        )

        return redirect('siswa_list')

    return render(
        request,
        'perpustakaan/siswa_hapus.html',
        {
            'siswa': siswa
        }
    )


# =========================
# PEMINJAMAN
# =========================

def peminjaman_list(request):
    peminjaman_list = Peminjaman.objects.select_related(
        'siswa',
        'buku'
    ).order_by('-id')

    return render(
        request,
        'perpustakaan/peminjaman_list.html',
        {
            'peminjaman_list': peminjaman_list
        }
    )


def peminjaman_tambah(request):
    siswa_list = Siswa.objects.all()
    buku_list = Buku.objects.filter(stok__gt=0)

    if request.method == 'POST':
        siswa = get_object_or_404(
            Siswa,
            pk=request.POST.get('siswa_id')
        )

        buku = get_object_or_404(
            Buku,
            pk=request.POST.get('buku_id')
        )

        Peminjaman.objects.create(
            siswa=siswa,
            buku=buku,
            tanggal_pinjam=request.POST.get(
                'tanggal_pinjam'
            ),
            tanggal_kembali=request.POST.get(
                'tanggal_kembali'
            ),
            keperluan=request.POST.get(
                'keperluan'
            ),
        )

        buku.stok -= 1
        buku.save()

        messages.success(
            request,
            'Peminjaman berhasil ditambahkan.'
        )

        return redirect('peminjaman_list')

    return render(
        request,
        'perpustakaan/peminjaman_form.html',
        {
            'form_title': 'Tambah Peminjaman',
            'siswa_list': siswa_list,
            'buku_list': buku_list,
        }
    )


def peminjaman_kembalikan(request, pk):
    peminjaman = get_object_or_404(
        Peminjaman,
        pk=pk
    )

    if not peminjaman.sudah_kembali:
        peminjaman.sudah_kembali = True
        peminjaman.save()

        buku = peminjaman.buku
        buku.stok += 1
        buku.save()

    messages.success(
        request,
        'Buku berhasil dikembalikan.'
    )

    return redirect('peminjaman_list')