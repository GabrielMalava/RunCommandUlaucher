#!/bin/bash

# Script de instalação para a extensão Terminal Command Executor do ULauncher

set -e

EXTENSION_NAME="com.github.malava-dev.terminal-command"
ULAUNCHER_EXT_DIR="$HOME/.config/ulauncher/extensions"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$ULAUNCHER_EXT_DIR/$EXTENSION_NAME"

echo "🚀 Instalando Terminal Command Executor para ULauncher..."
echo ""

# Verifica se o ULauncher está instalado
if ! command -v ulauncher &> /dev/null; then
    echo "❌ Erro: ULauncher não está instalado!"
    echo "   Instale o ULauncher primeiro:"
    echo "   sudo add-apt-repository ppa:agornostal/ulauncher"
    echo "   sudo apt update"
    echo "   sudo apt install ulauncher"
    exit 1
fi

# Cria o diretório de extensões se não existir
mkdir -p "$ULAUNCHER_EXT_DIR"

# Remove instalação anterior se existir
if [ -d "$TARGET_DIR" ]; then
    echo "📦 Removendo instalação anterior..."
    rm -rf "$TARGET_DIR"
fi

# Copia os arquivos da extensão
echo "📋 Copiando arquivos da extensão..."
cp -r "$PROJECT_DIR" "$TARGET_DIR"

# Remove arquivos desnecessários
cd "$TARGET_DIR"
rm -f install.sh README.md .git -rf 2>/dev/null || true

# Instala dependências Python
echo "📥 Instalando dependências Python..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt --user
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt --user
else
    echo "⚠️  Aviso: pip não encontrado. Instale as dependências manualmente:"
    echo "   pip3 install -r $TARGET_DIR/requirements.txt"
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

