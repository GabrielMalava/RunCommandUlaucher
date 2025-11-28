
echo "Diagnóstico da Extensão ULauncher"
echo "======================================"
echo ""

EXT_DIR="$HOME/.config/ulauncher/extensions/com.github.malava-dev.terminal-command"

echo "1. Verificando se a extensão está instalada..."
if [ -d "$EXT_DIR" ]; then
    echo "Extensão encontrada em: $EXT_DIR"
else
    echo "Extensão NÃO encontrada!"
    exit 1
fi

echo ""
echo "2. Verificando arquivos necessários..."
for file in manifest.json main.py images/icon.png; do
    if [ -f "$EXT_DIR/$file" ]; then
        echo "$file existe"
    else
        echo "$file NÃO existe!"
    fi
done

echo ""
echo "3. Verificando sintaxe do Python..."
if python3 -m py_compile "$EXT_DIR/main.py" 2>/dev/null; then
    echo "Sintaxe Python OK"
else
    echo "Erro de sintaxe Python!"
    python3 -m py_compile "$EXT_DIR/main.py"
fi

echo ""
echo "4. Verificando manifest.json..."
if python3 -m json.tool "$EXT_DIR/manifest.json" > /dev/null 2>&1; then
    echo "manifest.json válido"
    echo "   Palavra-chave configurada:"
    python3 -c "import json; m=json.load(open('$EXT_DIR/manifest.json')); print('   -', [p['default_value'] for p in m.get('preferences', []) if p.get('id')=='keyword'][0] or '!')"
else
    echo "manifest.json inválido!"
fi

echo ""
echo "5. Verificando se o ULauncher está rodando..."
if pgrep -x ulauncher > /dev/null; then
    echo "ULauncher está rodando (PID: $(pgrep -x ulauncher))"
else
    echo "ULauncher NÃO está rodando"
    echo "   Execute: ulauncher &"
fi

echo ""
echo "6. Instruções para testar:"
echo "   a) Abra o ULauncher (Alt+Space)"
echo "   b) Digite '!' (ou a palavra-chave configurada)"
echo "   c) Digite um comando simples como: ls"
echo "   d) Pressione Enter"
echo ""
echo "7. Se não aparecer nada quando digitar '!':"
echo "   - Abra Preferências do ULauncher (Ctrl+P)"
echo "   - Vá em 'Extensões'"
echo "   - Verifique se 'Terminal Command Executor' está listada e ATIVADA"
echo "   - Se não estiver, ative-a"
echo ""
echo "8. Para ver logs em tempo real:"
echo "   journalctl --user -f -u ulauncher"


