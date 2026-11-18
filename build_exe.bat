@echo off
REM Genera dist\JustClimb.exe con todos los assets incluidos.
REM Ejecutar desde la raiz del repositorio, en Windows.

python -m pip install -r requirements.txt -r requirements-build.txt || goto :error

python -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name JustClimb ^
    --add-data "assets;assets" ^
    src\main.py || goto :error

echo.
echo Listo: dist\JustClimb.exe
goto :eof

:error
echo.
echo Hubo un error al generar el ejecutable.
exit /b 1
