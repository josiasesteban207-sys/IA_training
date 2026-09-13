from core.ml_training_engine import MLTrainingEngine
from core.trainig_mode_selector import (
    TrainingModeSelector,
    TrainingMode
)
from core.device_manager import DeviceManager
from core.device_selector import DeviceSelector
from core.training_coordinator import TrainingCoordinator
from core.evaluation_policy import (
    EvaluationPolicy,
    EvaluationPolicyEngine
)

from core.evaluation_engine import (
    EvaluationEngine
)

from core.task_type_router import (
    TaskTypeRouter
)

from core.model_registry import (
    ModelRegistry
)

from core.checkpoint_manager import (
    CheckpointManager
)
from core.hybrid_training_engine import (
    HybridTrainingEngine
)
from core.training_engine import (
    TrainerEngine
)
from core.training_orchestrator import (
    TrainingOrchestrator
)
from core.training_job_manager import (
    TrainingJobManager
)

from core.pytorch_training_engine import (
    PyTorchTrainingEngine
)

from core.device_selector import (
    DeviceSelector
)
from core.hardware_profiler import (
    HardwareProfiler
)
from core.device_manager import (
    DeviceManager
)
class AITrainerPipeline:

    def __init__(self):
        self.trainer_engine = (
            TrainerEngine()
        )
        self.ml_training_engine = (
            MLTrainingEngine()
        )
        self.mode_selector = (
        TrainingModeSelector()
        )
        self.hardware_profiler = (
            HardwareProfiler()
        )
        # =====================================
        # MODELOS
        # =====================================

        self.model_registry = ModelRegistry()

        self.checkpoint_manager = (
            CheckpointManager()
        )

        self.task_router = TaskTypeRouter()

        # =====================================
        # DISPOSITIVOS
        # =====================================

        self.device_manager = DeviceManager()

        self.device_selector = (
            DeviceSelector(
                self.device_manager
            )
        )

        self.training_coordinator = (
            TrainingCoordinator(
                self.device_manager
            )
        )
        self.training_orchestrator = (
            TrainingOrchestrator(
                self
            )
        )
        
        self.pytorch_training_engine = (
            PyTorchTrainingEngine()
        )
        self.hybrid_training_engine = (
        HybridTrainingEngine(
        self.ml_training_engine,
        self.pytorch_training_engine,
        self.evaluation_engine
        )
        )
        self.device_selector = DeviceSelector(
        self.device_manager
        )
        self.device_manager = DeviceManager()

        self.device_selector = DeviceSelector(
        self.device_manager
        )
        self.job_manager = (
            TrainingJobManager()
        )

        self.evaluation_engine = (
            EvaluationEngine()
        )

        self.policy_engine = (
            EvaluationPolicyEngine()
        )

        self.model_registry = (
            ModelRegistry()
        )

        self.checkpoint_manager = (
            CheckpointManager()
        )

        self.task_router = (
            TaskTypeRouter()
        )
    def ejecutar_ml(

            self,

            tipo_tarea,

            X_train,

            y_train,

            X_test,

            y_test,

            modelo=None,

            politica=None,

            nombre_modelo="Modelo ML",

            dataset_nombre="Dataset",


        ):

    # =====================================
    # 1. VALIDAR TAREA
    # =====================================

    tarea = self.task_router.obtener(

        tipo_tarea

    )

    if tarea.tipo_evaluacion not in [

        "clasificacion",

        "regresion"

    ]:

        raise ValueError(

            "La tarea seleccionada "
            "no es compatible con ML."

        )

    # =====================================
    # 2. ENTRENAMIENTO ML REAL
    # =====================================

    resultado_entrenamiento = (

        self.ml_training_engine.entrenar(

            tipo_tarea=tipo_tarea,

            X_train=X_train,

            y_train=y_train,

            X_test=X_test,

            y_test=y_test,

            modelo=modelo

        )

    )

    # =====================================
    # 3. OBTENER PREDICCIONES
    # =====================================

    y_pred = (

        resultado_entrenamiento.predicciones

    )

    # =====================================
    # 4. EVALUAR MODELO
    # =====================================

    if tipo_tarea == "clasificacion":

        resultado_evaluacion = (

            self.evaluation_engine.evaluar_clasificacion(

                y_test,

                y_pred

            )

        )

    elif tipo_tarea == "regresion":

        resultado_evaluacion = (

            self.evaluation_engine
            .evaluar_regresion(

                y_test,

                y_pred

            )

        )

    else:

        raise ValueError(

            "Tipo de tarea no soportado."

        )

    # =====================================
    # 5. CREAR POLÍTICA POR DEFECTO
    # =====================================

    if politica is None:

        if tipo_tarea == "clasificacion":

            politica = EvaluationPolicy(

                nombre=(

                    "Politica ML "
                    "Clasificacion"

                ),

                metricas_minimas={

                    "accuracy": 0.80,

                    "precision": 0.80,

                    "recall": 0.80,

                    "f1": 0.80

                },

                metricas_criticas=[

                    "f1"

                ]

            )

        elif tipo_tarea == "regresion":

            politica = EvaluationPolicy(

                nombre=(

                    "Politica ML "
                    "Regresion"

                ),

                metricas_minimas={

                    "r2": 0.80

                },

                metricas_criticas=[

                    "r2"

                ]

            )

    # =====================================
    # 6. APLICAR POLÍTICA
    # =====================================

    resultado_policy = (

        self.policy_engine.evaluar(

            resultado_evaluacion,

            politica

        )

    )

    # =====================================
    # 7. REGISTRAR MODELO SI SE APRUEBA
    # =====================================

    modelo_registrado = None

    if (

        resultado_policy.estado

        ==

        "aprobado"

    ):

        modelo_registrado = (

            self.model_registry.registrar(

                nombre=nombre_modelo,

                framework="Scikit-learn",

                arquitectura=(

                    type(

                        resultado_entrenamiento.modelo

                    ).__name__

                ),

                dataset=dataset_nombre,

                version="1.0.0",

                metricas=(

                    resultado_evaluacion
                    .metricas

                )

            )

        )
    def ejecutar_dl():
            def actualizar_job(
    
        epoch,
    
        epochs_total,
    
        metricas
    
    ):
    
        self.job_manager.actualizar_progreso(
    
            job.id,
    
            epoch,
    
            metricas
    
        )
    def entrenar(
    
        self,
    
        modo,
    
        **kwargs
    
    ):
    
        modo_info = (
    
            self.mode_selector.obtener(
    
                modo
    
            )
    
        )
    
        if modo_info.modo == TrainingMode.ML:
    
            return self.ejecutar_ml(
    
                **kwargs
    
            )
    
        elif modo_info.modo == TrainingMode.DL:
    
            return self.ejecutar_dl(
    
                **kwargs
    
            )
    
        elif modo_info.modo == TrainingMode.HYBRID:
    
            raise NotImplementedError(
    
                "El modo híbrido aún no está implementado."
    
            )
    
        raise ValueError(
    
            "Modo de entrenamiento inválido."
    
        )
    # =====================================
    # 8. DEVOLVER RESULTADO
    # =====================================

    return {

        "estado": (

            resultado_policy.estado

        ),

        "modelo": (

            resultado_entrenamiento.modelo

        ),

        "predicciones": y_pred,

        "metricas": (

            resultado_evaluacion.metricas

        ),

        "politica": (

            resultado_policy

        ),

        "modelo_registrado": (

            modelo_registrado

        )

    }
    