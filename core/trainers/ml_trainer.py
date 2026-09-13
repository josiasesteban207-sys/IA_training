from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import joblib


class MLTrainer:

    def __init__(self):

        self.model = (
            RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
        )

    def entrenar(
        self,
        X,
        y,
        nombre_modelo="modelo_ml.pkl"
    ):

        print("\n" + "=" * 50)

        print(
            "⚡ INICIANDO ENTRENAMIENTO ML"
        )

        print("=" * 50)

        # Dividir datos

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )
        )

        print(
            "\n📚 Datos de entrenamiento:",
            len(X_train)
        )

        print(
            "🧪 Datos de prueba:",
            len(X_test)
        )

        # Entrenar

        print(
            "\n🧠 Entrenando modelo..."
        )

        self.model.fit(
            X_train,
            y_train
        )

        # Predicción

        predicciones = (
            self.model.predict(
                X_test
            )
        )

        # Evaluación

        accuracy = (
            accuracy_score(
                y_test,
                predicciones
            )
        )

        print(
            "\n📊 Precisión:",
            f"{accuracy * 100:.2f}%"
        )

        # Guardar

        joblib.dump(

            self.model,

            nombre_modelo

        )

        print(
            f"\n💾 Modelo guardado en:"
            f" {nombre_modelo}"
        )

        return {

            "accuracy": accuracy,

            "modelo": nombre_modelo

        }