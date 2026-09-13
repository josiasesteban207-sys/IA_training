from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV
)

from sklearn.ensemble import (
    RandomForestClassifier
)


class HyperparameterOptimizer:

    def optimizar_ml(

        self,

        X,

        y,

        metodo="grid",

        cv=3

    ):

        print(
            "\n" + "=" * 60
        )

        print(
            "⚙️ OPTIMIZACIÓN DE HIPERPARÁMETROS"
        )

        print(
            "=" * 60
        )

        # Modelo base

        modelo = (

            RandomForestClassifier(

                random_state=42

            )

        )

        # Espacio de búsqueda

        parametros = {

            "n_estimators": [

                50,

                100,

                200

            ],

            "max_depth": [

                None,

                5,

                10,

                20

            ],

            "min_samples_split": [

                2,

                5,

                10

            ]

        }

        # Elegir estrategia

        if metodo == "grid":

            print(

                "\n🔍 Método:"
                " Grid Search"

            )

            buscador = (

                GridSearchCV(

                    estimator=modelo,

                    param_grid=parametros,

                    cv=cv,

                    scoring="f1_weighted",

                    n_jobs=-1

                )

            )

        else:

            print(

                "\n🎲 Método:"
                " Random Search"

            )

            buscador = (

                RandomizedSearchCV(

                    estimator=modelo,

                    param_distributions=parametros,

                    n_iter=10,

                    cv=cv,

                    scoring="f1_weighted",

                    n_jobs=-1,

                    random_state=42

                )

            )

        # Ejecutar búsqueda

        print(

            "\n🚀 Buscando "
            "mejor configuración..."

        )

        buscador.fit(

            X,

            y

        )

        # Resultado

        print(

            "\n🏆 MEJOR CONFIGURACIÓN"
        )

        print(

            buscador.best_params_

        )

        print(

            "\n📊 Mejor puntuación:"
        )

        print(

            f"{buscador.best_score_ * 100:.2f}%"

        )

        return {

            "modelo":

                buscador.best_estimator_,

            "parametros":

                buscador.best_params_,

            "puntuacion":

                buscador.best_score_

        }