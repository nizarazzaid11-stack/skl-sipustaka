from django.contrib import admin
from .models import Buku, Siswa, Peminjaman

admin.site.register(Buku)
admin.site.register(Siswa)
admin.site.register(Peminjaman)