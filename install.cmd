echo "Creating virtual environment ..."
if not exist "%~dp0condat_venv\" (
    python -m venv "%~dp0condat_venv"
    "%~dp0condat_venv\Scripts\pip.exe" install textual==1.0.0
)
echo "Adding the directory to PATH ..."
setx condat_path %~dp0
setx PATH "%%PATH%%;%%condat_path%%"
echo "Done. Please restart the terminal."
