set -x
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$DIR/condat_venv" ]; then
    python3 -m venv "$DIR/condat_venv"
    "$DIR/condat_venv/bin/pip" install textual==1.0.0
fi
"$DIR/condat_venv/bin/python" "$DIR/main.py"