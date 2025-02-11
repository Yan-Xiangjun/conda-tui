if not exist "%~dp0condat_venv\" (
    python -m venv "%~dp0condat_venv"
    %~dp0condat_venv\Scripts\pip.exe install textual==1.0.0
)
%~dp0condat_venv\Scripts\python.exe %~dp0main.py