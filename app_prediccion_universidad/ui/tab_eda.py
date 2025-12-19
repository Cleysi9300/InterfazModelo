import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TabEDA(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        df = pd.read_csv("data/dataset_eda.csv")

        layout.addWidget(QLabel(f"Dataset cargado: {df.shape[0]} filas"))
        layout.addWidget(QLabel(str(df.head())))

        self.setLayout(layout)
