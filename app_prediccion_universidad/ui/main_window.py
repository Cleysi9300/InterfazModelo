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
        self.tabs.setStyleSheet("""
                  
            QWidget {
                font-family: "Segoe UI";
                font-size: 13px;
                color: #1F1F1F;
                background-color: #FFFFFF;
            }

            /* ==============================
            TÍTULOS
            ============================== */
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

            /* ==============================
            BOTONES
            ============================== */
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

            /* Botón secundario */
            QPushButton#secundario {
                background-color: #CDA34F;
                color: #1F1F1F;
            }

            QPushButton#secundario:hover {
                background-color: #b8933e;
            }

            /* ==============================
            TAB WIDGET (NAVEGACIÓN)
            ============================== */
            QTabWidget::pane {
                border: none;
            }

            QTabBar::tab {
                background: #F4F6F8;
                color: #0B4F95;
                padding: 10px 20px;
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

            /* ==============================
            TARJETAS / CONTENEDORES
            ============================== */
            QFrame#card {
                background-color: #FFFFFF;
                border: 2px solid #0B4F95;
                border-radius: 12px;
                padding: 20px;
            }

            /* ==============================
            FORMULARIOS
            ============================== */
            QLineEdit, QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #B0B0B0;
                border-radius: 6px;
                padding: 6px;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0B4F95;
            }

            /* ==============================
            GROUPBOX (EDA SECCIONES)
            ============================== */
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

            /* ==============================
            TABLAS
            ============================== */
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

            /* ==============================
            SCROLLBARS
            ============================== */
            QScrollBar:vertical {
                background: #F4F6F8;
                width: 12px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #0B4F95;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background: #4A90E2;
            }

            /* ==============================
            RESULTADO MODELO
            ============================== */
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
            
            QComboBox {
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #0B4F95;
            }

            QComboBox:hover {
                border: 1px solid #4A90E2;
            }

            

            """)



        self.tabs.addTab(TabEDA(), "EDA")
        self.tabs.addTab(TabModelo(), "Modelo Predictivo")

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        container.setLayout(layout)

        self.setCentralWidget(container)
        