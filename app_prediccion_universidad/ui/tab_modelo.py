import os
import joblib
import pickle
import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QMessageBox, QFormLayout,
    QHBoxLayout, QFrame
)


class TabModelo(QWidget):
    def __init__(self):
        super().__init__()

        # ===============================
        # Layout principal centrado
        # ===============================
        self.main_layout = QHBoxLayout()
        self.card = QFrame()
        self.card.setObjectName("card")

        self.layout = QVBoxLayout(self.card)
        self.form = QFormLayout()

        self.layout.addLayout(self.form)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.card)
        self.main_layout.addStretch()

        # ===============================
        # Cargar artefactos
        # ===============================
        self.cargar_artifactos()

        # ===============================
        # Inputs dinámicos (TODOS COMBO)
        # ===============================
        self.inputs = {}
        self.crear_inputs()

        # ===============================
        # Botón predecir
        # ===============================
        self.btn_predecir = QPushButton("Predecir Resultado")
        self.btn_predecir.clicked.connect(self.predecir)
        self.layout.addWidget(self.btn_predecir)

        # ===============================
        # Resultado
        # ===============================
        self.label_resultado = QLabel("Resultado: ---")
        self.layout.addWidget(self.label_resultado)

        self.setLayout(self.main_layout)
        self.aplicar_estilos()

    # ==================================================
    # Cargar modelo y metadatos
    # ==================================================
    def cargar_artifactos(self):
        self.modelo = joblib.load("model/modelo_XGBOOST.joblib")

        with open("model/columnas_modelo.pkl", "rb") as f:
            self.columnas_modelo = pickle.load(f)

        with open("model/cat_features.pkl", "rb") as f:
            self.cat_features = pickle.load(f)

        with open("model/num_features.pkl", "rb") as f:
            self.num_features = pickle.load(f)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "dataset_eda.csv")
        self.df_ref = pd.read_csv(data_path)


    # ==================================================
    # Crear ComboBox numérico inteligente
    # ==================================================
    def _crear_combo_numerico(self, col):
        combo = QComboBox()

        valores = (
            self.df_ref[col]
            .dropna()
            .astype(int)
            .sort_values()
            .unique()
            .tolist()
        )

        # Si hay demasiados valores → rangos
        if len(valores) > 20:
            min_v, max_v = min(valores), max(valores)
            paso = max(1, (max_v - min_v) // 6)

            rangos = [
                f"{i} - {min(i + paso - 1, max_v)}"
                for i in range(min_v, max_v + 1, paso)
            ]
            combo.addItems(rangos)
            combo.setProperty("es_rango", True)
        else:
            combo.addItems([str(v) for v in valores])
            combo.setProperty("es_rango", False)

        combo.setCurrentIndex(-1)
        return combo

    # ==================================================
    # Crear inputs automáticamente
    # ==================================================
    def crear_inputs(self):
        for col in self.columnas_modelo:

            # ----------------------------
            # CATEGÓRICAS
            # ----------------------------
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
                combo.setCurrentIndex(-1)

                self.form.addRow(QLabel(col), combo)
                self.inputs[col] = combo

            # ----------------------------
            # NUMÉRICAS (también ComboBox)
            # ----------------------------
            elif col in self.num_features:
                combo = self._crear_combo_numerico(col)
                self.form.addRow(QLabel(col), combo)
                self.inputs[col] = combo

    # ==================================================
    # Predicción
    # ==================================================
    def predecir(self):
        try:
            datos = {}

            for col, widget in self.inputs.items():
                texto = widget.currentText()

                if texto == "":
                    raise ValueError(f"Seleccione un valor para {col}")

                # Rango → tomar valor inicial
                if widget.property("es_rango"):
                    valor = int(texto.split("-")[0].strip())
                else:
                    # numérico o categórico
                    if col in self.num_features:
                        valor = float(texto)
                    else:
                        valor = texto

                datos[col] = valor

            df = pd.DataFrame([datos])
            df = df.reindex(columns=self.columnas_modelo, fill_value=0)

            pred = self.modelo.predict(df)[0]

            if hasattr(self.modelo, "predict_proba"):
                proba = self.modelo.predict_proba(df)[0][1]
            else:
                proba = None

            self.mostrar_resultado(pred, proba)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ==================================================
    # Mostrar resultado
    # ==================================================
    def mostrar_resultado(self, pred, proba=None):
        if pred == 1:
            color = "#1E7E34"
            texto = "APROBADO ✅"
        else:
            color = "#B02A37"
            texto = "NO APROBADO ❌"

        if proba is not None:
            texto += f"  (Probabilidad: {proba:.2%})"

        self.label_resultado.setText(texto)
        self.label_resultado.setStyleSheet(
            f"""
            background-color: #f4f6f8;
            color: {color};
            font-size: 16px;
            font-weight: bold;
            padding: 12px;
            border-radius: 8px;
            """
        )

    # ==================================================
    # Estilos
    # ==================================================
    def aplicar_estilos(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
            }

            QFrame#card {
                background-color: #ffffff;
                border-radius: 14px;
                padding: 24px;
                min-width: 520px;
                max-width: 650px;
                border: 2px solid #0B4F95;
            }

            QLabel {
                font-weight: 600;
                color: #0B4F95;
            }

            QComboBox {
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #0B4F95;
            }

            QComboBox:hover {
                border: 1px solid #4A90E2;
            }

            QPushButton {
                background-color: #0B4F95;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #4A90E2;
            }
        """)
