from pathlib import Path

import torch
import torch.nn as nn

from torch.utils.data import (
    DataLoader,
    TensorDataset
)


class SimpleNeuralNetwork(nn.Module):

    def __init__(
        self,
        input_size,
        num_classes
    ):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(
                input_size,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                32
            ),

            nn.ReLU(),

            nn.Linear(
                32,
                num_classes
            )

        )

    def forward(self, x):

        return self.network(x)


class DLTrainer:

    def __init__(self):

        self.device = torch.device(

            "cuda"
            if torch.cuda.is_available()
            else "cpu"

        )

        print(
            "\n🚀 DISPOSITIVO SELECCIONADO:"
        )

        print(
            self.device
        )

        if torch.cuda.is_available():

            print(
                "🎮 GPU:",
                torch.cuda.get_device_name(0)
            )

        else:

            print(
                "💻 CUDA no disponible."
            )

            print(
                "Se utilizará CPU."
            )

    def entrenar(

        self,

        X,

        y,

        nombre_modelo=(
            "models/modelo_dl.pth"
        ),

        epochs=20,

        batch_size=16

    ):

        print(
            "\n" + "=" * 50
        )

        print(
            "🚀 INICIANDO DEEP LEARNING"
        )

        print(
            "=" * 50
        )

        # Convertir datos

        X_tensor = torch.tensor(

            X,

            dtype=torch.float32

        )

        y_tensor = torch.tensor(

            y,

            dtype=torch.long

        )

        # Dataset

        dataset = TensorDataset(

            X_tensor,

            y_tensor

        )

        loader = DataLoader(

            dataset,

            batch_size=batch_size,

            shuffle=True

        )

        # Crear modelo

        input_size = X.shape[1]

        num_classes = len(
            set(y)
        )

        model = SimpleNeuralNetwork(

            input_size,

            num_classes

        )

        model = model.to(

            self.device

        )

        # Función de pérdida

        criterion = (
            nn.CrossEntropyLoss()
        )

        # Optimizador

        optimizer = (
            torch.optim.Adam(

                model.parameters(),

                lr=0.001

            )
        )

        # Entrenamiento

        for epoch in range(

            epochs

        ):

            total_loss = 0

            for (

                inputs,

                labels

            ) in loader:

                inputs = inputs.to(

                    self.device

                )

                labels = labels.to(

                    self.device

                )

                # Limpiar gradientes

                optimizer.zero_grad()

                # Forward

                outputs = model(

                    inputs

                )

                # Calcular pérdida

                loss = criterion(

                    outputs,

                    labels

                )

                # Backpropagation

                loss.backward()

                # Actualizar pesos

                optimizer.step()

                total_loss += (

                    loss.item()

                )

            if (

                epoch + 1
            ) % 5 == 0:

                print(

                    f"Epoch "
                    f"{epoch + 1}/"
                    f"{epochs} "
                    f"- Loss: "
                    f"{total_loss:.4f}"

                )

        # Crear carpeta

        Path(

            nombre_modelo

        ).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        # Guardar modelo

        torch.save(

            model.state_dict(),

            nombre_modelo

        )

        print(

            "\nModelo PyTorch guardado en:"
        )

        print(

            nombre_modelo

        )

        return {

            "modelo": nombre_modelo,

            "dispositivo": str(

                self.device

            ),

            "epochs": epochs

        }