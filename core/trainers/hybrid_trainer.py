from pathlib import Path

import numpy as np

import torch
import torch.nn as nn

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

import joblib


class FeatureExtractor(nn.Module):

    def __init__(
        self,
        input_size
    ):

        super().__init__()

        self.features = nn.Sequential(

            nn.Linear(
                input_size,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                32
            ),

            nn.ReLU()

        )

        self.classifier = nn.Linear(

            32,

            3

        )

    def forward(
        self,
        x
    ):

        features = self.features(
            x
        )

        output = self.classifier(
            features
        )

        return output


class HybridTrainer:

    def __init__(self):

        self.device = torch.device(

            "cuda"
            if torch.cuda.is_available()
            else "cpu"

        )

        print(
            "\n🔥 MOTOR HÍBRIDO"
        )

        print(
            f"Dispositivo DL: "
            f"{self.device}"
        )

    def entrenar(

        self,

        X,

        y,

        nombre_dl=(
            "models/"
            "modelo_hybrid_dl.pth"
        ),

        nombre_ml=(
            "models/"
            "modelo_hybrid_ml.pkl"
        ),

        epochs=20

    ):

        print(
            "\n" + "=" * 50
        )

        print(
            "🔥 INICIANDO ENTRENAMIENTO HÍBRIDO"
        )

        print(
            "=" * 50
        )

        # ==================================
        # PARTE 1
        # DEEP LEARNING
        # ==================================

        print(
            "\n🚀 FASE 1"
        )

        print(
            "Extrayendo características "
            "con PyTorch..."
        )

        X_tensor = torch.tensor(

            X,

            dtype=torch.float32

        ).to(

            self.device

        )

        y_tensor = torch.tensor(

            y,

            dtype=torch.long

        ).to(

            self.device

        )

        model = FeatureExtractor(

            X.shape[1]

        ).to(

            self.device

        )

        criterion = (

            nn.CrossEntropyLoss()

        )

        optimizer = (

            torch.optim.Adam(

                model.parameters(),

                lr=0.001

            )

        )

        # Entrenamiento DL

        for epoch in range(

            epochs

        ):

            optimizer.zero_grad()

            outputs = model(

                X_tensor

            )

            loss = criterion(

                outputs,

                y_tensor

            )

            loss.backward()

            optimizer.step()

            if (

                epoch + 1
            ) % 5 == 0:

                print(

                    f"Epoch "
                    f"{epoch + 1}/"
                    f"{epochs} "
                    f"- Loss: "
                    f"{loss.item():.4f}"

                )

        # ==================================
        # EXTRAER FEATURES
        # ==================================

        print(
            "\n🧠 Extrayendo features..."
        )

        with torch.no_grad():

            features = model.features(

                X_tensor

            )

        features = (

            features

            .cpu()

            .numpy()

        )

        # ==================================
        # PARTE 2
        # MACHINE LEARNING
        # ==================================

        print(
            "\n⚡ FASE 2"
        )

        print(
            "Clasificando features "
            "con Scikit-learn..."
        )

        X_train, X_test, y_train, y_test = (

            train_test_split(

                features,

                y,

                test_size=0.2,

                random_state=42

            )

        )

        ml_model = (

            RandomForestClassifier(

                n_estimators=100,

                random_state=42

            )

        )

        ml_model.fit(

            X_train,

            y_train

        )

        predictions = (

            ml_model.predict(

                X_test

            )

        )

        accuracy = (

            accuracy_score(

                y_test,

                predictions

            )

        )

        print(

            f"\n📊 Precisión híbrida:"
            f" {accuracy * 100:.2f}%"

        )

        # ==================================
        # GUARDAR MODELOS
        # ==================================

        Path(

            nombre_dl

        ).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        torch.save(

            model.state_dict(),

            nombre_dl

        )

        joblib.dump(

            ml_model,

            nombre_ml

        )

        print(
            "\n💾 Modelo DL guardado:"
        )

        print(
            nombre_dl
        )

        print(
            "\n💾 Modelo ML guardado:"
        )

        print(
            nombre_ml
        )

        return {

            "precision": accuracy,

            "modelo_dl": nombre_dl,

            "modelo_ml": nombre_ml,

            "dispositivo": str(

                self.device

            )

        }