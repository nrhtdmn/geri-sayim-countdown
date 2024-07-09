import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QTabWidget, QMessageBox, QAction, QInputDialog, QSpinBox
)
from PyQt5.QtCore import QTimer, QTime, Qt

class ZamanlayiciSekmesi(QWidget):
    def __init__(self, parent=None):
        super(ZamanlayiciSekmesi, self).__init__(parent)
        
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        time_selection_layout = QHBoxLayout()
        self.hour_spinbox = QSpinBox(self)
        self.hour_spinbox.setRange(0, 23)
        self.hour_spinbox.setSuffix(" saat")
        self.hour_spinbox.setFixedSize(100, 40)
        self.hour_spinbox.setStyleSheet("font-size: 18px;")
        
        self.minute_spinbox = QSpinBox(self)
        self.minute_spinbox.setRange(0, 59)
        self.minute_spinbox.setSuffix(" dakika")
        self.minute_spinbox.setFixedSize(100, 40)
        self.minute_spinbox.setStyleSheet("font-size: 18px;")
        
        self.second_spinbox = QSpinBox(self)
        self.second_spinbox.setRange(0, 59)
        self.second_spinbox.setSuffix(" saniye")
        self.second_spinbox.setFixedSize(100, 40)
        self.second_spinbox.setStyleSheet("font-size: 18px;")
        
        time_selection_layout.addWidget(self.hour_spinbox)
        time_selection_layout.addWidget(self.minute_spinbox)
        time_selection_layout.addWidget(self.second_spinbox)
        
        layout.addLayout(time_selection_layout)
        
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Başlat", self)
        self.start_button.setFixedSize(100, 40)
        self.start_button.setStyleSheet("font-size: 18px;")
        self.start_button.clicked.connect(self.start_timer)
        button_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        
        self.stop_button = QPushButton("Durdur", self)
        self.stop_button.setFixedSize(100, 40)
        self.stop_button.setStyleSheet("font-size: 18px;")
        self.stop_button.clicked.connect(self.stop_timer)
        button_layout.addWidget(self.stop_button, alignment=Qt.AlignCenter)
        
        self.reset_button = QPushButton("Sıfırla", self)
        self.reset_button.setFixedSize(100, 40)
        self.reset_button.setStyleSheet("font-size: 18px;")
        self.reset_button.clicked.connect(self.reset_timer)
        button_layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)
        
        layout.addLayout(button_layout)
        
        self.time_label = QLabel("00:00:00.000", self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFixedSize(400, 80)
        self.time_label.setStyleSheet("font-size: 36px; color: blue;")
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(10)  # 10 ms
        
        self.remaining_time = QTime(0, 0, 0, 0)
    
    def start_timer(self):
        hours = self.hour_spinbox.value()
        minutes = self.minute_spinbox.value()
        seconds = self.second_spinbox.value()
        self.remaining_time = QTime(hours, minutes, seconds, 0)
        self.timer.start()
    
    def stop_timer(self):
        self.timer.stop()
    
    def reset_timer(self):
        self.timer.stop()
        self.time_label.setText("00:00:00.000")
    
    def update_timer(self):
        if self.remaining_time == QTime(0, 0, 0, 0):
            self.timer.stop()
            QMessageBox.information(self, "Bilgi", "Zaman doldu!")
        else:
            self.remaining_time = self.remaining_time.addMSecs(-10)
            self.time_label.setText(self.remaining_time.toString("HH:mm:ss.zzz"))

class ZamanlayiciUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Zamanlayıcı Uygulaması')
        self.setGeometry(100, 100, 600, 300)
        
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabBarDoubleClicked.connect(self.sekme_ismini_duzenle)
        self.tab_widget.tabCloseRequested.connect(self.sekme_kapat)
        self.setCentralWidget(self.tab_widget)
        
        self.yeni_zamanlayici_ekle()
        
        menubar = self.menuBar()
        zamanlayici_menu = menubar.addMenu('Zamanlayıcı')
        
        yeni_action = QAction("Yeni Zamanlayıcı Ekle", self)
        yeni_action.setShortcut("Ctrl+N")
        yeni_action.triggered.connect(self.yeni_zamanlayici_ekle)
        zamanlayici_menu.addAction(yeni_action)
        
        sekme_duzenle_action = QAction("Sekme İsmini Düzenle", self)
        sekme_duzenle_action.setShortcut("Ctrl+E")
        sekme_duzenle_action.triggered.connect(self.sekme_ismini_duzenle)
        zamanlayici_menu.addAction(sekme_duzenle_action)
        
        # QSS stili uygula
        self.setStyleSheet(self.qss_stili())
        
        self.show()
    
    def yeni_zamanlayici_ekle(self):
        yeni_sekme = ZamanlayiciSekmesi()
        self.tab_widget.addTab(yeni_sekme, "Zamanlayıcı " + str(self.tab_widget.count() + 1))
    
    def sekme_ismini_duzenle(self, index=None):
        if index is None:
            index = self.tab_widget.currentIndex()
        
        if index >= 0:
            current_name = self.tab_widget.tabText(index)
            yeni_isim, ok = QInputDialog.getText(self, "Sekme İsmini Düzenle", "Yeni isim girin:", text=current_name)
            if ok and yeni_isim:
                self.tab_widget.setTabText(index, yeni_isim)
    
    def sekme_kapat(self, index):
        self.tab_widget.removeTab(index)
    
    def qss_stili(self):
        return """
        QMainWindow {
            background-color: #f0f0f0;
        }
        QTabWidget::pane {
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        QTabBar::tab {
            background: #ddd;
            border: 1px solid #ccc;
            border-bottom: none;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            padding: 5px;
            margin-right: 1px;
        }
        QTabBar::tab:selected {
            background: #f0f0f0;
            border-color: #999;
        }
        QSpinBox, QLabel {
            font-size: 16px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3e8e41;
        }
        """
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    zamanlayici_uygulamasi = ZamanlayiciUygulamasi()
    sys.exit(app.exec_())
