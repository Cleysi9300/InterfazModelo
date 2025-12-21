from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget
)

from ui.tab_eda import TabEDA
from ui.tab_modelo import TabModelo
from ui.tab_perfil_est import TabPerfilEst


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ==============================
        # Ventana principal
        # ==============================
        self.setWindowTitle("Sistema de Predicción Universitaria")
        self.setGeometry(100, 100, 1100, 700)

        # ==============================
        # Tabs
        # ==============================
        self.tabs = QTabWidget()

        # ==============================
        # Estilos globales
        # ==============================
        self.tabs.setStyleSheet("""
            QWidget {
                font-family: "Segoe UI";
                font-size: 13px;
                color: #1F1F1F;
                background-color: #FFFFFF;
            }

            QLabel {
                color: #0B4F95;
            }

            QLabel#tituloPrincipal {
                font-size: 20px;
                font-weight: bold;
                color: #0B4F95;
            }

            QLabel#subtitulo {
                font-size: 14px;
                font-weight: bold;
                color: #CDA34F;
            }

            QPushButton {
                background-color: #0B4F95;
                color: white;
                border-radius: 8px;
                padding: 8px 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #4A90E2;
            }

            QPushButton:pressed {
                background-color: #083b70;
            }

            QPushButton#secundario {
                background-color: #CDA34F;
                color: #1F1F1F;
            }

            QPushButton#secundario:hover {
                background-color: #b8933e;
            }

            QTabWidget::pane {
                border: none;
            }

            QTabBar::tab {
                background: #F4F6F8;
                color: #0B4F95;
                padding: 10px 22px;
                margin-right: 3px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: bold;
            }

            QTabBar::tab:selected {
                background: #0B4F95;
                color: white;
            }

            QTabBar::tab:hover {
                background: #4A90E2;
                color: white;
            }

            QFrame#card {
                background-color: #FFFFFF;
                border: 2px solid #0B4F95;
                border-radius: 12px;
                padding: 20px;
            }

            QLineEdit, QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #B0B0B0;
                border-radius: 6px;
                padding: 6px;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0B4F95;
            }

            QGroupBox {
                border: 2px solid #0B4F95;
                border-radius: 10px;
                margin-top: 12px;
                font-weight: bold;
                color: #0B4F95;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 4px 10px;
                background-color: #FFFFFF;
            }

            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F4F6F8;
                gridline-color: #D0D0D0;
            }

            QHeaderView::section {
                background-color: #0B4F95;
                color: white;
                padding: 6px;
                border: none;
                font-weight: bold;
            }

            QScrollBar:vertical {
                background: #F4F6F8;
                width: 12px;
            }

            QScrollBar::handle:vertical {
                background: #0B4F95;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background: #4A90E2;
            }

            QLabel#resultadoAprobado {
                background-color: #E6F4EA;
                color: #1E7E34;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }

            QLabel#resultadoReprobado {
                background-color: #FDECEA;
                color: #B02A37;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }
        """)

        # ==============================
        # Crear instancias de los tabs
        # ==============================
        self.tab_eda = TabEDA()
        self.tab_modelo = TabModelo()
        self.tab_perfil = TabPerfilEst()

        # ==============================
        # Agregar tabs
        # ==============================
        self.tabs.addTab(self.tab_eda, "EDA")
        self.tabs.addTab(self.tab_modelo, "Modelo Predictivo")
        self.tabs.addTab(self.tab_perfil, "Perfil Estadístico")

        # ==============================
        # Conectar tabs entre sí
        # ==============================
        self.tab_modelo.tab_perfil = self.tab_perfil
        self.tab_modelo.tabs_widget = self.tabs

        # ==============================
        # Layout central
        # ==============================
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.tabs)

        self.setCentralWidget(container)
