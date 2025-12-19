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

        self.layout = QVBoxLayout()
        self.form = QFormLayout()

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

        self.setLayout(self.layout)

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

    # ===============================
    # Crear inputs automáticamente
    # ===============================
    def crear_inputs(self):
        for col in self.columnas_modelo:

            # CATEGÓRICAS → ComboBox
            if col in self.cat_features:
                combo = QComboBox()
                combo.setEditable(True)  # permite escribir si no está en la lista
                self.form.addRow(QLabel(col), combo)
                self.inputs[col] = combo

            # NUMÉRICAS → LineEdit
            elif col in self.num_features:
                line = QLineEdit()
                self.form.addRow(QLabel(col), line)
                self.inputs[col] = line

    # ===============================
    # Predicción
    # ===============================
    def predecir(self):
        try:
            datos = {}

            for col, widget in self.inputs.items():
                if isinstance(widget, QComboBox):
                    datos[col] = widget.currentText()
                else:
                    datos[col] = float(widget.text())

            df = pd.DataFrame([datos])
            df = df.reindex(columns=self.columnas_modelo, fill_value=0)

            pred = self.modelo.predict(df)[0]

            if hasattr(self.modelo, "predict_proba"):
                proba = self.modelo.predict_proba(df)[0][1]
                self.label_resultado.setText(
                    f"Resultado: {'APROBADO ✅' if pred == 1 else 'NO APROBADO ❌'} "
                    f"(Probabilidad: {proba:.2%})"
                )
            else:
                self.label_resultado.setText(
                    f"Resultado: {'APROBADO ✅' if pred == 1 else 'NO APROBADO ❌'}"
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
