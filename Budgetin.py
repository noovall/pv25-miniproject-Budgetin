import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi

class BudgetinApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("BudgetinJadi.ui", self)
        self.setFixedSize(self.size())

        self.setStyleSheet("""
            QWidget {
                background-color: #fff;
            }
            QPushButton {
                background-color: #FFA500;
                color: #fff;
                border-radius: 8px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e69500;
            }
            QTableWidget {
                background-color: #fff;
                gridline-color: #FFA500;
                border: 1px solid #FFA500;
            }
            QHeaderView::section {
                background-color: #FFA500;
                color: white;
                padding: 4px;
                border: 1px solid #ddd;
            }
            QLabel {
                color: #000;
            }
        """)

        self.totalBelanja = 0

        self.tombolTambahBarang.clicked.connect(self.tambahBarang)
        self.tombolReset.clicked.connect(self.resetData)
        self.tombolSimpan.clicked.connect(self.simpanData)

    def tambahBarang(self):
        nama = self.NamaBarangLineEdit.text()
        harga_text = self.HargaLineEdit.text()
        jumlah = self.spinBoxJumlah.value()
        kategori = self.comboBoxKategori.currentText()

        # Validasi input
        if not nama or not harga_text or kategori == "-- Pilih --":
            QMessageBox.warning(self, "Input Tidak Lengkap", "Harap isi semua field.")
            return

        try:
            harga = int(harga_text)
        except ValueError:
            QMessageBox.warning(self, "Input Salah", "Harga harus berupa angka.")
            return

        subtotal = harga * jumlah

        try:
            budget = int(self.BudgetlineEdit.text())
        except ValueError:
            QMessageBox.warning(self, "Input Salah", "Budget harus diisi dan berupa angka.")
            return

        if self.totalBelanja + subtotal > budget:
            QMessageBox.warning(self, "Melebihi Budget", "Total belanja melebihi budget!")
            return

        self.totalBelanja += subtotal

        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(nama))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(str(harga)))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(str(jumlah)))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(str(subtotal)))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(kategori))

        self.LabelTotal.setText(str(self.totalBelanja))
        self.hitungSisa()

        self.NamaBarangLineEdit.clear()
        self.HargaLineEdit.clear()
        self.spinBoxJumlah.setValue(1)
        self.comboBoxKategori.setCurrentIndex(0)

    def hitungSisa(self):
        try:
            budget = int(self.BudgetlineEdit.text())
        except ValueError:
            self.LabelSisa.setText("Isi Budget")
            return

        sisa = budget - self.totalBelanja
        self.LabelSisa.setText(str(sisa))

    def resetData(self):
        self.BudgetlineEdit.clear()
        self.NamaBarangLineEdit.clear()
        self.HargaLineEdit.clear()
        self.spinBoxJumlah.setValue(1)
        self.comboBoxKategori.setCurrentIndex(0)
        self.LabelTotal.clear()
        self.LabelSisa.clear()
        self.tableWidget.setRowCount(0)
        self.totalBelanja = 0

    def simpanData(self):
        try:
            with open("daftar_belanja.txt", "w") as file:
                for row in range(self.tableWidget.rowCount()):
                    data = []
                    for col in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, col)
                        data.append(item.text() if item else "")
                    file.write("\t".join(data) + "\n")
            QMessageBox.information(self, "Berhasil", "Data berhasil disimpan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetinApp()
    window.show()
    sys.exit(app.exec_())
