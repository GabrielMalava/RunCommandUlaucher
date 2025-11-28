

EXTENSION_NAME="com.github.malava-dev.terminal-command"
# O ULauncher instala extensões em ~/.local/share/ulauncher/extensions/
ULAUNCHER_EXT_DIR="$HOME/.local/share/ulauncher/extensions"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$ULAUNCHER_EXT_DIR/$EXTENSION_NAME"

echo "Instalando Terminal Command Executor para ULauncher..."
echo ""

if ! command -v ulauncher &> /dev/null; then
    echo "Erro: ULauncher não está instalado!"
    echo "   Instale o ULauncher primeiro:"
    echo "   sudo add-apt-repository ppa:agornostal/ulauncher"
    echo "   sudo apt update"
    echo "   sudo apt install ulauncher"
    exit 1
fi

mkdir -p "$ULAUNCHER_EXT_DIR"

if [ -d "$TARGET_DIR" ]; then
    echo "Removendo instalação anterior..."
    rm -rf "$TARGET_DIR"
fi

echo "Copiando arquivos da extensão..."
cp -r "$PROJECT_DIR" "$TARGET_DIR"

cd "$TARGET_DIR"
rm -f install.sh README.md .git -rf 2>/dev/null || true

echo " Verificando dependências Python..."
if python3 -c "import ulauncher" 2>/dev/null; then
    echo "Módulo ulauncher já está disponível (instalado com o ULauncher)"
else
    echo "Módulo ulauncher não encontrado. Tentando instalar..."
    if command -v pip3 &> /dev/null; then
        if pip3 install -r requirements.txt --user 2>/dev/null; then
            echo "Dependências instaladas com sucesso (--user)"
        else
            echo "Tentando com --break-system-packages (pode ser necessário no Python 3.12+)..."
            if pip3 install -r requirements.txt --user --break-system-packages 2>/dev/null; then
                echo "Dependências instaladas com sucesso"
            else
                echo "Não foi possível instalar via pip3."
                echo "Tente instalar manualmente:"
                echo "   pip3 install --user --break-system-packages ulauncher"
                echo "   ou"
                echo "   sudo apt install python3-ulauncher"
                echo ""
                echo "Continuando mesmo assim - a extensão pode funcionar se o ULauncher já tiver as dependências"
            fi
        fi
    else
        echo "pip3 não encontrado. O ULauncher geralmente já inclui as dependências necessárias."
    fi
fi

# Verifica se o ícone existe, se não, cria um placeholder
if [ ! -f "images/icon.png" ]; then
    echo "🎨 Criando ícone placeholder..."
    mkdir -p images
    # Cria um ícone SVG simples e converte para PNG se possível
    cat > images/icon.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="#2ecc71" rx="8"/>
  <text x="32" y="42" font-family="monospace" font-size="32" fill="white" text-anchor="middle">$</text>
</svg>
EOF
    # Tenta converter SVG para PNG se o ImageMagick estiver disponível
    if command -v convert &> /dev/null; then
        convert images/icon.svg images/icon.png 2>/dev/null || true
    fi
fi

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "🔄 Reiniciando ULauncher..."
ulauncher --restart 2>/dev/null || echo "⚠️  Execute manualmente: ulauncher --restart"
echo ""
echo "📖 Como usar:"
echo "   1. Abra o ULauncher (Alt+Space)"
echo "   2. Digite '!' seguido do comando (ex: !sudo reboot)"
echo "   3. Pressione Enter para executar"
echo ""
echo "⚙️  Configure a extensão em: ULauncher > Preferências > Extensões"

