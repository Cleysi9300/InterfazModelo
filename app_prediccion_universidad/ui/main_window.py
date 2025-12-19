from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget
)
from ui.tab_eda import TabEDA
from ui.tab_modelo import TabModelo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Predicción Universitaria")
        self.setGeometry(100, 100, 900, 600)

        self.tabs = QTabWidget()

        self.tabs.addTab(TabEDA(), "EDA")
        self.tabs.addTab(TabModelo(), "Modelo Predictivo")

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        container.setLayout(layout)

        self.setCentralWidget(container)
