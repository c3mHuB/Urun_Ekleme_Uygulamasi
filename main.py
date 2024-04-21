import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from urun_ekle import *

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()


#veri tabanı işlemleri
import sqlite3

baglanti = sqlite3.connect("urunler.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute("create table if not exists urun (urunkodu int,urunadi text,birimfiyat int,stokmiktari int,urunaciklamasi text,marka text,katagori text)")
baglanti.commit()


def kayit_ekle():
    try:
        urunkodu = int(ui.lneurunkodu.text())
        urunadi = ui.lneurunadi.text()
        birimfiyat = int(ui.lnebirimfiyat.text())
        stokmiktari = int(ui.lnestokmiktar.text())
        urunacik = ui.lneurunaciklamasi.text()
        marka = ui.cmbmarka.currentText()
        katagori = ui.cmbkatagori.currentText()

        ekle = "insert into urun (urunkodu,urunadi,birimfiyat,stokmiktari,urunaciklamasi,marka,katagori) values(?,?,?,?,?,?,?)"
        islem.execute(ekle,(urunkodu,urunadi,birimfiyat,stokmiktari,urunacik,marka,katagori))
        baglanti.commit()
        kayit_listele()
        ui.statusbar.showMessage("kayit ekleme işlemi basarili",2000)
    except Exception as error:
        ui.statusbar.showMessage("kayit ekleme işlemi basarisiz , hata ciktisi == "+str(error))

def kayit_listele():
    ui.tbllist.clear()
    ui.tbllist.setHorizontalHeaderLabels(("Ürün Kodu","Ürün Adi","Birim Fiyati","Stok Miktari","Ürün Aciklamasi","Markasi","Katagorisi"))

    sorgu = "select * from urun"
    islem.execute(sorgu)

    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tbllist.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))


def KgL(): #katagoriye göre listeleme
    list_kat = ui.cmbkat.currentText()

    sorgu = "select * from urun where katagori = ?"
    islem.execute(sorgu,(list_kat,))
    ui.tbllist.clear()
    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tbllist.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))


def ks(): #kayit sil
    silmsg = QMessageBox.question(pencere,"Silme Onayi","silmek istediğinizden emin misiniz ???",QMessageBox.Yes | QMessageBox.No)

    if silmsg == QMessageBox.Yes:
        secKayit = ui.tbllist.selectedItems()
        silKayit = secKayit[0].text()

        sorgu = "delete from urun where urunkodu = ?"
        try:
            islem.execute(sorgu,(silKayit,))
            baglanti.commit()
            kayit_listele()
            ui.statusbar.showMessage("Kayit Silindi")
        except Exception as error:
            ui.statusbar.showMessage("kayit silinirken sorunla karsilasildi , hata ciktisi == "+str(error))
    
    else:
        ui.statusbar.showMessage("silme işlemi iptal edildi")


def kg(): #kayit guncelle
    guncmsg = QMessageBox.question(pencere,"Güncelleme Onayi","güncellemek istediğinizden emin misiniz ???",QMessageBox.Yes | QMessageBox.No)

    if guncmsg == QMessageBox.Yes:
        try:
            UrunKodu = ui.lneurunkodu.text()
            UrunAdi = ui.lneurunadi.text()
            BirimFiyat = ui.lnebirimfiyat.text()
            StokMiktar = ui.lnestokmiktar.text()
            UrunAciklama = ui.lneurunaciklamasi.text()
            Marka = ui.cmbmarka.currentText()
            Katagori = ui.cmbkatagori.currentText()

            if UrunAdi ==  "" and BirimFiyat == "" and StokMiktar == "" and UrunAciklama == "" and Marka == "":
                islem.execute("update urun set katagori = ? where urunkodu = ?",(Katagori,UrunKodu))
            elif UrunAdi ==  "" and BirimFiyat == "" and StokMiktar == "" and UrunAciklama == "" and Katagori == "":
                islem.execute("update urun set marka = ? where urunkodu = ?",(Marka,UrunKodu))
            elif UrunAdi ==  "" and BirimFiyat == "" and StokMiktar == "" and Marka == "" and Katagori == "":
                islem.execute("update urun set urunaciklamasi = ? where urunkodu = ?",(UrunAciklama,UrunKodu))
            elif UrunAdi ==  "" and BirimFiyat == "" and UrunAciklama == "" and Marka == "" and Katagori == "":
                islem.execute("update urun set stokmiktari = ? where urunkodu = ?",(StokMiktar,UrunKodu))
            elif UrunAdi ==  "" and StokMiktar == "" and UrunAciklama == "" and Marka == "" and Katagori == "":
                islem.execute("update urun set birimfiyat = ? where urunkodu = ?",(BirimFiyat,UrunKodu))
            elif BirimFiyat ==  "" and StokMiktar == "" and UrunAciklama == "" and Marka == "" and Katagori == "":
                islem.execute("update urun set urunadi = ? where urunkodu = ?",(UrunAdi,UrunKodu))

            else:
                islem.execute("update urun set urunadi = ? , birimfiyat = ? , stokmiktari = ? , urunaciklamasi = ? , marka = ? , katagori = ? where urunkodu = ?",(UrunAdi,BirimFiyat,StokMiktar,UrunAciklama,Marka,Katagori,UrunKodu))
            baglanti.commit()
            kayit_listele()
            ui.statusbar.showMessage("kayit başari ile güncellendi")
        except Exception as error:
            ui.statusbar.showMessage("kayit güncellemede hata meydana geldi , hata ciktisi == "+str(error))
    else:
        ui.statusbar.showMessage("güncelleme iptal edildi")




#butonlar
ui.btekle.clicked.connect(kayit_ekle)
ui.btnlist.clicked.connect(kayit_listele)
ui.btnkatlist.clicked.connect(KgL)
ui.btnsil.clicked.connect(ks)
ui.btngunc.clicked.connect(kg)
sys.exit(uygulama.exec_())