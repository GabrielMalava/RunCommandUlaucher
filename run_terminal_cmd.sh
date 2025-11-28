#!/bin/bash
# Script wrapper para executar comandos no terminal via ULauncher
# Executa em background e retorna imediatamente

COMMAND="$1"
SHELL_TYPE="${2:-fish}"

# Desacopla completamente do processo pai usando nohup e setsid
if [ "$SHELL_TYPE" = "fish" ]; then
    # Usa --login para carregar funções do fish
    if command -v gnome-terminal >/dev/null 2>&1; then
        nohup gnome-terminal -- fish --login -c "$COMMAND; exec fish" >/dev/null 2>&1 &
    elif command -v xterm >/dev/null 2>&1; then
        nohup xterm -e fish --login -c "$COMMAND; exec fish" >/dev/null 2>&1 &
    else
        nohup x-terminal-emulator -e fish --login -c "$COMMAND; exec fish" >/dev/null 2>&1 &
    fi
else
    EXPANDED_PATH="$HOME/.local/bin:$HOME/bin:$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    if command -v gnome-terminal >/dev/null 2>&1; then
        nohup gnome-terminal -- bash -c "export PATH=$EXPANDED_PATH; $COMMAND; read -p \"Pressione Enter para fechar...\"" >/dev/null 2>&1 &
    elif command -v xterm >/dev/null 2>&1; then
        nohup xterm -e bash -c "export PATH=$EXPANDED_PATH; $COMMAND; read -p \"Pressione Enter para fechar...\"" >/dev/null 2>&1 &
    else
        nohup x-terminal-emulator -e bash -c "export PATH=$EXPANDED_PATH; $COMMAND; read -p \"Pressione Enter para fechar...\"" >/dev/null 2>&1 &
    fi
fi

# Retorna imediatamente
exit 0

