from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Buku
    path('buku/', views.buku_list, name='buku_list'),
    path('buku/tambah/', views.buku_tambah, name='buku_tambah'),
    path('buku/<int:pk>/', views.buku_detail, name='buku_detail'),
    path('buku/<int:pk>/edit/', views.buku_edit, name='buku_edit'),
    path('buku/<int:pk>/hapus/', views.buku_hapus, name='buku_hapus'),

    # Siswa
    path('user/', views.siswa_list, name='siswa_list'),
    path('user/tambah/', views.siswa_tambah, name='siswa_tambah'),
    path('user/<int:pk>/', views.siswa_detail, name='siswa_detail'),
    path('user/<int:pk>/edit/', views.siswa_edit, name='siswa_edit'),
    path('user/<int:pk>/hapus/', views.siswa_hapus, name='siswa_hapus'),

    # Peminjaman
    path('peminjaman/', views.peminjaman_list, name='peminjaman_list'),
    path('peminjaman/tambah/', views.peminjaman_tambah, name='peminjaman_tambah'),
    path('peminjaman/<int:pk>/kembalikan/', views.peminjaman_kembalikan, name='peminjaman_kembalikan'),
]
