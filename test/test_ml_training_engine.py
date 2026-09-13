from sklearn.datasets import (

    load_iris

)

from sklearn.model_selection import (

    train_test_split

)

from sklearn.metrics import (

    accuracy_score

)

from core.ml_training_engine import (

    MLTrainingEngine

)


def main():

    print(

        "\n🧠 AI TRAINER"

    )

    print(

        "🟢 ML TRAINING ENGINE"

    )

    print(

        "=" * 60

    )

    # =====================================
    # CARGAR DATASET
    # =====================================

    dataset = load_iris()

    X = dataset.data

    y = dataset.target

    # =====================================
    # DIVIDIR DATASET
    # =====================================

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42,

            stratify=y

        )

    )

    print(

        "\n📊 Dataset cargado"

    )

    print(

        f"Entrenamiento: "

        f"{len(X_train)} muestras"

    )

    print(

        f"Prueba: "

        f"{len(X_test)} muestras"

    )

    # =====================================
    # CREAR ENGINE
    # =====================================

    engine = MLTrainingEngine()

    # =====================================
    # ENTRENAR
    # =====================================

    resultado = engine.entrenar(

        tipo_tarea="clasificacion",

        X_train=X_train,

        y_train=y_train,

        X_test=X_test,

        y_test=y_test

    )

    # =====================================
    # EVALUAR
    # =====================================

    accuracy = accuracy_score(

        y_test,

        resultado.predicciones

    )

    # =====================================
    # RESULTADOS
    # =====================================

    print(

        "\n🚀 ENTRENAMIENTO COMPLETADO"

    )

    print(

        f"Estado: "

        f"{resultado.estado}"

    )

    print(

        f"Modelo: "

        f"{type(resultado.modelo).__name__}"

    )

    print(

        f"Accuracy: "

        f"{accuracy:.2%}"

    )


if __name__ == "__main__":

    main()