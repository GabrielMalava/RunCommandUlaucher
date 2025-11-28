

set -e

GITHUB_URL="https://github.com/GabrielMalava/RunCommandUlaucher.git"
EXTENSION_NAME="com.github.malava-dev.terminal-command"
ULAUNCHER_EXT_DIR="$HOME/.local/share/ulauncher/extensions"
TARGET_DIR="$ULAUNCHER_EXT_DIR/$EXTENSION_NAME"
TEMP_DIR=$(mktemp -d)

echo "Instalando Terminal Command Executor do GitHub para ULauncher..."
echo ""

if ! command -v ulauncher &> /dev/null; then
    echo "Erro: ULauncher não está instalado!"
    echo "   Instale o ULauncher primeiro:"
    echo "   sudo add-apt-repository ppa:agornostal/ulauncher"
    echo "   sudo apt update"
    echo "   sudo apt install ulauncher"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "   Erro: Git não está instalado!"
    echo "   Instale o Git primeiro:"
    echo "   sudo apt install git"
    exit 1
fi

mkdir -p "$ULAUNCHER_EXT_DIR"

if [ -d "$TARGET_DIR" ]; then
    echo "Removendo instalação anterior..."
    rm -rf "$TARGET_DIR"
fi

echo "Clonando repositório do GitHub..."
cd "$TEMP_DIR"
git clone "$GITHUB_URL" extension-temp

echo "Copiando arquivos da extensão..."
mkdir -p "$TARGET_DIR"
cp -r extension-temp/* "$TARGET_DIR"/

cd "$TARGET_DIR"
rm -rf .git install-from-github.sh 2>/dev/null || true

echo "Instalando dependências Python..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt --user
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt --user
else
    echo "Aviso: pip não encontrado. Instale as dependências manualmente:"
    echo "   pip3 install -r $TARGET_DIR/requirements.txt"
fi

if [ ! -f "images/icon.png" ] && [ -f "images/icon.svg" ]; then
    echo "Convertendo ícone SVG para PNG..."
    if command -v convert &> /dev/null; then
        convert images/icon.svg images/icon.png 2>/dev/null || true
    elif command -v inkscape &> /dev/null; then
        inkscape images/icon.svg --export-filename=images/icon.png --export-width=64 --export-height=64 2>/dev/null || true
    fi
fi

rm -rf "$TEMP_DIR"

echo ""
echo "Instalação concluída!"
echo ""
echo "Reiniciando ULauncher..."
ulauncher --restart 2>/dev/null || echo "Execute manualmente: ulauncher --restart"
echo ""
echo "Como usar:"
echo "   1. Abra o ULauncher (Alt+Space)"
echo "   2. Digite '!' seguido do comando (ex: !sudo reboot)"
echo "   3. Pressione Enter para executar"
echo ""
echo "Configure a extensão em: ULauncher > Preferências > Extensões"



