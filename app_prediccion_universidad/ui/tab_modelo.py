import os
import joblib
import pickle
import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QMessageBox, QFormLayout
)

class TabModelo(QWidget):
    def __init__(self):
        super().__init__()

        from PyQt6.QtWidgets import QHBoxLayout, QFrame

        self.main_layout = QHBoxLayout()
        self.card = QFrame()
        self.card.setObjectName("card")

        self.layout = QVBoxLayout(self.card)
        self.form = QFormLayout()

        self.layout.addLayout(self.form)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.card)
        self.main_layout.addStretch()

        

        # === Cargar artefactos ===
        self.cargar_artifactos()

        # === Inputs dinámicos ===
        self.inputs = {}
        self.crear_inputs()

        self.layout.addLayout(self.form)


        # === Botón predecir ===
        self.btn_predecir = QPushButton("Predecir Resultado")
        self.btn_predecir.clicked.connect(self.predecir)
        self.layout.addWidget(self.btn_predecir)

        # === Resultado ===
        self.label_resultado = QLabel("Resultado: ---")
        self.layout.addWidget(self.label_resultado)

        self.setLayout(self.main_layout)
        self.aplicar_estilos()



    # ===============================
    # Cargar modelo y metadatos
    # ===============================
    def cargar_artifactos(self):
        self.modelo = joblib.load("model/modelo_XGBOOST.joblib")

        with open("model/columnas_modelo.pkl", "rb") as f:            
            self.columnas_modelo = pickle.load(f)

        with open("model/cat_features.pkl", "rb") as f:
            self.cat_features = pickle.load(f)

        with open("model/num_features.pkl", "rb") as f:
            self.num_features = pickle.load(f)
         # === Dataset de referencia ===
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "dataset_eda.csv")
        self.df_ref = pd.read_csv(data_path)

    # ===============================
    # Crear inputs automáticamente
    # ===============================
    def crear_inputs(self):
        for col in self.columnas_modelo:

            # ============================
            # VARIABLES CATEGÓRICAS
            # ============================
            if col in self.cat_features:
                combo = QComboBox()

                valores = (
                    self.df_ref[col]
                    .dropna()
                    .astype(str)
                    .sort_values()
                    .unique()
                    .tolist()
                )

                combo.addItems(valores)
                combo.setCurrentIndex(-1)  # nada seleccionado

                self.form.addRow(QLabel(col), combo)
                self.inputs[col] = combo

            # ============================
            # VARIABLES NUMÉRICAS
            # ============================
            elif col in self.num_features:
                line = QLineEdit()
                line.setPlaceholderText("Ingrese valor numérico")
                self.form.addRow(QLabel(col), line)
                self.inputs[col] = line


    # ===============================
    # Predicción
    # ===============================
    def predecir(self):
        try:
            datos = {}

            for col, widget in self.inputs.items():

                # ============================
                # CATEGÓRICAS
                # ============================
                if isinstance(widget, QComboBox):
                    valor = widget.currentText()
                    if valor == "":
                        raise ValueError(f"Seleccione un valor para {col}")
                    datos[col] = valor

                # ============================
                # NUMÉRICAS
                # ============================
                else:
                    if widget.text().strip() == "":
                        raise ValueError(f"Ingrese un valor para {col}")

                    valor = float(widget.text())

                    # Validaciones específicas
                    if col == "EDAD" and not (15 <= valor <= 80):
                        raise ValueError("La edad debe estar entre 15 y 80 años")

                    if col in ["ANIOS_POST_BACH", "TASA_APR_COLEGIO"] and valor < 0:
                        raise ValueError(f"{col} no puede ser negativo")

                    datos[col] = valor

            # DataFrame final
            df = pd.DataFrame([datos])
            df = df.reindex(columns=self.columnas_modelo, fill_value=0)

            # Predicción
            pred = self.modelo.predict(df)[0]

            if hasattr(self.modelo, "predict_proba"):
                proba = self.modelo.predict_proba(df)[0][1]
            else:
                proba = None

            self.mostrar_resultado(pred, proba)

        except Exception as e:
            QMessageBox.critical(self, "Error de validación", str(e))
    
    def mostrar_resultado(self, pred, proba=None):
        if pred == 1:
            color = "green"
            texto = "APROBADO ✅"
        else:
            color = "red"
            texto = "NO APROBADO ❌"

        if proba is not None:
            texto += f" (Probabilidad: {proba:.2%})"

        self.label_resultado.setText(texto)

        self.label_resultado.setStyleSheet(
            f"""
            color: {color};
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            background-color: #f4f6f8;
            border-radius: 8px;
            """
        )


    def aplicar_estilos(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
            }

            QFrame#card {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 20px;
                min-width: 500px;
                max-width: 650px;
            }

            QLabel {
                font-weight: 600;
                color: #333333;
            }

            QLineEdit, QComboBox {
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #cccccc;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #4a90e2;
            }

            QPushButton {
                background-color: #4a90e2;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #357abd;
            }
        """)
