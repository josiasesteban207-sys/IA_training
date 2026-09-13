from dataclasses import dataclass

from typing import Any


@dataclass
class PyTorchTrainingResult:

    modelo: Any

    predicciones: Any

    historial: list[dict[str, float]]

    dispositivo: str

    estado: str = "completado"


class PyTorchTrainingEngine:

    def __init__(self):

        try:

            import torch

        except ImportError as error:

            raise RuntimeError(

                "PyTorch no está instalado."

            ) from error

        self.torch = torch

        self.dispositivo = self._detectar_dispositivo()

        self.modelo = None

    # =========================================
    # DETECTAR GPU / CPU
    # =========================================

    def _detectar_dispositivo(self):

        if self.torch.cuda.is_available():

            return self.torch.device(

                "cuda"

            )

        return self.torch.device(

            "cpu"

        )

    # =========================================
    # ENTRENAR
    # =========================================

    def entrenar(

    self,

    modelo,

    X_train,

    y_train,

    X_test,

    y_test,

    epochs=10,

    learning_rate=0.001,

    callback_progreso=None

):

    torch = self.torch

    # =====================================
    # MOVER MODELO AL DISPOSITIVO
    # =====================================

    modelo = modelo.to(

        self.dispositivo

    )

    self.modelo = modelo

    # =====================================
    # CONVERTIR DATOS
    # =====================================

    X_train = torch.tensor(

        X_train,

        dtype=torch.float32,

        device=self.dispositivo

    )

    y_train = torch.tensor(

        y_train,

        dtype=torch.long,

        device=self.dispositivo

    )

    X_test = torch.tensor(

        X_test,

        dtype=torch.float32,

        device=self.dispositivo

    )

    # =====================================
    # LOSS
    # =====================================

    criterio = (

        torch.nn.CrossEntropyLoss()

    )

    # =====================================
    # OPTIMIZADOR
    # =====================================

    optimizador = (

        torch.optim.Adam(

            modelo.parameters(),

            lr=learning_rate

        )

    )

    historial = []

    # =====================================
    # ENTRENAMIENTO
    # =====================================

    modelo.train()

    for epoch in range(

        epochs

    ):

        optimizador.zero_grad()

        # Forward

        salida = modelo(

            X_train

        )

        # Loss

        loss = criterio(

            salida,

            y_train

        )

        # Backpropagation

        loss.backward()

        # Actualizar pesos

        optimizador.step()

        # =================================
        # REGISTRO
        # =================================

        loss_actual = float(

            loss.item()

        )

        registro = {

            "epoch": float(

                epoch + 1

            ),

            "loss": loss_actual

        }

        historial.append(

            registro

        )

        # =================================
        # CALLBACK DE PROGRESO
        # =================================

        if callback_progreso:

            callback_progreso(

                epoch=epoch + 1,

                epochs_total=epochs,

                metricas={

                    "loss": loss_actual

                }

            )

    # =====================================
    # EVALUACIÓN
    # =====================================

    modelo.eval()

    with torch.no_grad():

        salida = modelo(

            X_test

        )

        predicciones = torch.argmax(

            salida,

            dim=1

        )

    return PyTorchTrainingResult(

        modelo=modelo,

        predicciones=(

            predicciones

            .cpu()

            .numpy()

        ),

        historial=historial,

        dispositivo=str(

            self.dispositivo

        ),

        estado="completado"

    )