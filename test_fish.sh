#!/bin/bash
# Teste simples para verificar se fish --login funciona
gnome-terminal -- fish --login -c "vpnstart; echo ''; echo 'Pressione Enter para fechar...'; read" &
echo "Terminal aberto. Verifique se o comando foi executado."

