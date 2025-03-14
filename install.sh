set -x
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Creating virtual environment ..."
if [ ! -d "$DIR/condat_venv" ]; then
    python3 -m venv "$DIR/condat_venv"
    "$DIR/condat_venv/bin/pip" install textual==1.0.0
fi
chmod +x "$DIR/condat"
echo "Adding the directory to PATH ..."
echo "export PATH=\$PATH:$DIR" >> ~/.$(basename "$SHELL")rc
echo "Done. Please restart the terminal."
