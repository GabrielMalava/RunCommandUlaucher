#!/bin/bash
# Script wrapper para executar comandos no terminal via ULauncher

COMMAND="$1"
SHELL_TYPE="${2:-fish}"

if [ "$SHELL_TYPE" = "fish" ]; then
    if command -v gnome-terminal >/dev/null 2>&1; then
        gnome-terminal -- fish -c "$COMMAND; exec fish"
    elif command -v xterm >/dev/null 2>&1; then
        xterm -e fish -c "$COMMAND; exec fish"
    else
        x-terminal-emulator -e fish -c "$COMMAND; exec fish"
    fi
else
    EXPANDED_PATH="$HOME/.local/bin:$HOME/bin:$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    if command -v gnome-terminal >/dev/null 2>&1; then
        gnome-terminal -- bash -c "export PATH=$EXPANDED_PATH; $COMMAND; read -p \"Pressione Enter para fechar...\""
    elif command -v xterm >/dev/null 2>&1; then
        xterm -e bash -c "export PATH=$EXPANDED_PATH; $COMMAND; read -p \"Pressione Enter para fechar...\""
    else
        x-terminal-emulator -e bash -c "export PATH=$EXPANDED_PATH; $COMMAND; read -p \"Pressione Enter para fechar...\""
    fi
fi

