@echo off
title Entrenador - Instalador y Lanzador

echo ============================================
echo       AI_TRAINER / Entrenador
echo       Instalador de recursos Python
echo ============================================
echo.

REM --------------------------------------------
REM 1. Ir a la carpeta donde esta este .bat
REM --------------------------------------------
cd /d "%~dp0"

echo [1/6] Carpeta del proyecto:
echo %cd%
echo.

REM --------------------------------------------
REM 2. Comprobar que Python este instalado
REM --------------------------------------------
echo [2/6] Comprobando Python...

python --version >nul 2>&1

if errorlevel 1 (
echo.
echo ERROR: Python no esta instalado o no esta agregado al PATH.
echo Instala Python y vuelve a ejecutar este archivo.
echo.
pause
exit /b 1
)

python --version
echo.

REM --------------------------------------------
REM 3. Crear entorno virtual si no existe
REM --------------------------------------------
echo [3/6] Comprobando entorno virtual...

if not exist "gisam\Scripts\python.exe" (
echo.
echo No se encontro el entorno virtual.
echo Creando .venv...
echo.

```
python -m venv gisam

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo crear el entorno virtual.
    pause
    exit /b 1
)

echo Entorno virtual creado correctamente.
```

) else (
echo El entorno virtual ya existe.
)

echo.

REM --------------------------------------------
REM 4. Activar entorno virtual
REM --------------------------------------------
echo [4/6] Activando entorno virtual...

call ".venv\Scripts\activate.bat"

if errorlevel 1 (
echo.
echo ERROR: No se pudo activar el entorno virtual.
pause
exit /b 1
)

echo Entorno virtual activado.
echo.

REM --------------------------------------------
REM 5. Actualizar pip
REM --------------------------------------------
echo [5/6] Actualizando pip...

python -m pip install --upgrade pip

echo.

REM --------------------------------------------
REM 6. Instalar dependencias
REM --------------------------------------------
echo [6/6] Instalando dependencias...

if exist "requirements.txt" (
echo.
echo Se encontro requirements.txt
echo Instalando dependencias...
echo.

```
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ADVERTENCIA: Ocurrio un error instalando algunas dependencias.
    echo Revisa los mensajes anteriores.
    echo.
)
```

) else (
echo.
echo No se encontro requirements.txt
echo Instalando dependencias basicas conocidas...
echo.

```
python -m pip install flask
python -m pip install opencv-python
python -m pip install numpy
python -m pip install mysql-connector-python
python -m pip install pyserial
python -m pip install requests
python -m pip install google-api-python-client
python -m pip install google-auth-httplib2
python -m pip install google-auth-oauthlib

echo.
echo Dependencias basicas instaladas.
```

)

echo.
echo ============================================
echo       INSTALACION FINALIZADA
echo ============================================
echo.

REM --------------------------------------------
REM Ejecutar la aplicacion
REM --------------------------------------------
if exist "app.py" (
echo Iniciando app.py...
echo.

```
python app.py
```

) else if exist "app_corregido.py" (
echo Iniciando app_corregido.py...
echo.

```
python app_corregido.py
```

) else if exist "Server.py" (
echo Iniciando Server.py...
echo.

```
python Server.py
```

) else (
echo.
echo No se encontro app.py, app_corregido.py ni Server.py.
echo.
echo El entorno virtual esta listo.
)

echo.
echo ============================================
echo       PROGRAMA FINALIZADO
echo ============================================
pause
