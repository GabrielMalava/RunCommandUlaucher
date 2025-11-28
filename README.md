# Terminal Command Executor - Extensão ULauncher

Extensão para o ULauncher que permite executar comandos do terminal diretamente pela barra de pesquisa, sem precisar abrir uma janela de terminal.

## 🚀 Funcionalidades

- Execute qualquer comando do terminal diretamente do ULauncher
- Confirmação automática para comandos perigosos (sudo, rm, reboot, etc)
- Opção para mostrar a saída do comando em notificações
- Configurável via preferências do ULauncher

## 📦 Instalação

### Método 1: Instalação Manual

1. Clone ou copie este diretório para a pasta de extensões do ULauncher:
```bash
cp -r UlaucherProjectTerminal ~/.config/ulauncher/extensions/com.github.malava-dev.terminal-command
```

2. Instale as dependências:
```bash
cd ~/.config/ulauncher/extensions/com.github.malava-dev.terminal-command
pip3 install -r requirements.txt
```

3. Reinicie o ULauncher:
```bash
ulauncher --restart
```

### Método 2: Usando o Script de Instalação

Execute o script de instalação:
```bash
chmod +x install.sh
./install.sh
```

## ⚙️ Configuração

Após a instalação, você pode configurar a extensão nas Preferências do ULauncher:

1. Abra o ULauncher (Alt+Space ou o atalho configurado)
2. Clique no ícone de engrenagem (⚙️) para abrir as Preferências
3. Vá até a aba "Extensões"
4. Encontre "Terminal Command Executor" e clique em "Configurar"

### Opções Disponíveis:

- **Palavra-chave**: Define a palavra-chave para ativar a extensão (padrão: `!`)
- **Exigir confirmação**: Quando ativado, comandos perigosos requerem confirmação
- **Mostrar saída**: Quando ativado, mostra a saída do comando em uma notificação

## 💡 Como Usar

1. Abra o ULauncher (Alt+Space por padrão)
2. Digite a palavra-chave configurada (padrão: `!`)
3. Digite o comando que deseja executar
4. Pressione Enter para executar

### Exemplos:

- `!sudo reboot` - Reinicia o sistema
- `!ls -la` - Lista arquivos
- `!echo "Hello World"` - Exibe uma mensagem
- `!git status` - Verifica status do git
- `!systemctl status docker` - Verifica status de um serviço

## ⚠️ Segurança

A extensão detecta automaticamente comandos perigosos e solicita confirmação antes de executá-los. Os comandos considerados perigosos incluem:

- `sudo` - Execução com privilégios elevados
- `rm` - Remoção de arquivos
- `dd`, `mkfs`, `fdisk` - Operações de disco
- `shutdown`, `reboot`, `poweroff` - Controle do sistema
- `killall`, `pkill`, `kill` - Encerramento de processos

Você pode desativar a confirmação nas configurações, mas isso não é recomendado por questões de segurança.

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
```

### Requisitos

- Python 3.6+
- ULauncher 2.0+
- Dependências listadas em `requirements.txt`

## 📝 Licença

Este projeto é de código aberto e está disponível para uso pessoal.

## 🤝 Contribuindo

Sinta-se à vontade para fazer fork, melhorar e contribuir com este projeto!

