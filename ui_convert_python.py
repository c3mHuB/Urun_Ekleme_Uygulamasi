from PyQt5 import uic

with open("urun_ekle.py","w",encoding="utf-8") as fout:
    uic.compileUi("urun_ekle.ui",fout)