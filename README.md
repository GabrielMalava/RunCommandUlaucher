# Terminal Command Executor - Extensão ULauncher

Extensão para o ULauncher que permite executar comandos do terminal diretamente pela barra de pesquisa, sem precisar abrir uma janela de terminal.

## 🚀 Funcionalidades

- Execute qualquer comando do terminal diretamente do ULauncher
- Confirmação automática para comandos perigosos (sudo, rm, reboot, etc)
- Opção para mostrar a saída do comando em notificações
- Configurável via preferências do ULauncher

## 📦 Instalação

### Método 1: Instalação Direta do GitHub (Recomendado)

Se você já clonou o repositório localmente, execute:

```bash
cd /home/malava-dev/Documents/git/UlaucherProjectTerminal
./install.sh
```

Ou se quiser instalar diretamente do GitHub sem clonar primeiro:

```bash
# Clone o repositório
git clone https://github.com/GabrielMalava/RunCommandUlaucher.git
cd RunCommandUlaucher

# Execute o script de instalação
chmod +x install.sh
./install.sh
```

### Método 2: Instalação Manual

1. Clone ou copie este diretório para a pasta de extensões do ULauncher:
```bash
git clone https://github.com/GabrielMalava/RunCommandUlaucher.git
cp -r RunCommandUlaucher ~/.local/share/ulauncher/extensions/com.github.malava-dev.terminal-command
```

2. Instale as dependências:
```bash
cd ~/.local/share/ulauncher/extensions/com.github.malava-dev.terminal-command
pip3 install -r requirements.txt --user
```

3. Reinicie o ULauncher:
```bash
ulauncher --restart
```

### Método 3: Via Interface do ULauncher (Pode não funcionar)

Alguns usuários relatam problemas ao instalar diretamente via URL do GitHub na interface do ULauncher. Se quiser tentar:

1. Abra o ULauncher (Alt+Space)
2. Pressione `Ctrl+P` para abrir Preferências
3. Vá até a aba "Extensões"
4. Clique em "Adicionar extensão"
5. Cole a URL: `https://github.com/GabrielMalava/RunCommandUlaucher.git`
6. Se não funcionar, use um dos métodos acima

**Nota:** O método mais confiável é usar o script `install.sh` após clonar o repositório.

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

