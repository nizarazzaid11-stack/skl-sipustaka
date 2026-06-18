# Models tidak digunakan karena menggunakan Raw SQL
# Tabel dibuat manual melalui SQL
from django.db import models

class Buku(models.Model):
    judul = models.CharField(max_length=255)
    pengarang = models.CharField(max_length=255)
    kategori = models.CharField(max_length=100, blank=True, null=True)
    penerbit = models.CharField(max_length=255, blank=True, null=True)
    tahun = models.IntegerField(blank=True, null=True)
    rak = models.CharField(max_length=50, blank=True, null=True)
    stok = models.IntegerField(default=0)

    def __str__(self):
        return self.judul

class Siswa(models.Model):
    nama = models.CharField(max_length=255)
    kelas = models.CharField(max_length=50)
    nis = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nama

class Peminjaman(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField()
    keperluan = models.TextField(blank=True, null=True)
    petugas = models.CharField(max_length=100, default='Budi Siregar')
    sudah_kembali = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.siswa.nama} meminjam {self.buku.judul}"