#!/usr/bin/env python3
"""
ULauncher Extension - Terminal Command Executor
Executa comandos do terminal diretamente do ULauncher
"""

import subprocess
import shlex
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


class TerminalCommandExtension(Extension):
    """Extensão para executar comandos do terminal via ULauncher"""

    DANGEROUS_COMMANDS = ['sudo', 'rm', 'dd', 'mkfs', 'fdisk', 'shutdown', 'reboot', 
                          'poweroff', 'halt', 'killall', 'pkill', 'kill']

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    """Ouvinte para eventos de consulta por palavra-chave"""

    def on_event(self, event, extension):
        query = event.get_argument() or ""
        query = query.strip()
        
        require_confirm = True  
        show_output = False  
        items = []

        if not query:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Digite um comando para executar',
                description='Exemplo: sudo reboot, ls -la, echo "Hello"',
                on_enter=HideWindowAction()
            ))
        else:
            is_dangerous = any(query.startswith(cmd) or query.split()[0] == cmd 
                              for cmd in TerminalCommandExtension.DANGEROUS_COMMANDS)
            
            interactive_commands = ['sudo', 'ssh', 'mysql', 'psql', 'nano', 'vim', 'vi', 'less', 'more']
            needs_terminal = any(query.strip().startswith(cmd + ' ') or query.strip() == cmd 
                                for cmd in interactive_commands)
            
            if is_dangerous and require_confirm:
                if needs_terminal:
                    escaped_query = query.replace('"', '\\"')
                    terminal_cmd = f'gnome-terminal -- bash -c "export PATH=\\$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; {escaped_query}; read -p \\"Pressione Enter para fechar...\\"" || xterm -e bash -c "export PATH=\\$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; {escaped_query}; read -p \\"Pressione Enter para fechar...\\"" || x-terminal-emulator -e bash -c "export PATH=\\$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; {escaped_query}; read -p \\"Pressione Enter para fechar...\\""'
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar: {query}',
                        description='Comando perigoso - Abrirá em terminal para interação',
                        on_enter=RunScriptAction(terminal_cmd)
                    ))
                else:
                    bash_cmd = f'bash -c "export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; {shlex.quote(query)}"'
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar: {query}',
                        description='Comando perigoso - Pressione Enter para confirmar',
                        on_enter=RunScriptAction(bash_cmd)
                    ))
            else:
                if needs_terminal:
                    escaped_query = query.replace('"', '\\"')
                    terminal_cmd = f'gnome-terminal -- bash -c "export PATH=\\$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; {escaped_query}; read -p \\"Pressione Enter para fechar...\\"" || xterm -e bash -c "export PATH=\\$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; {escaped_query}; read -p \\"Pressione Enter para fechar...\\"" || x-terminal-emulator -e bash -c "export PATH=\\$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; {escaped_query}; read -p \\"Pressione Enter para fechar...\\""'
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar: {query}',
                        description='Abrirá em terminal para interação',
                        on_enter=RunScriptAction(terminal_cmd)
                    ))
                else:
                    bash_cmd = f'bash -c "export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; {shlex.quote(query)}"'
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar: {query}',
                        description='Pressione Enter para executar',
                        on_enter=RunScriptAction(bash_cmd)
                    ))
                
                if show_output:
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar e mostrar saída: {query}',
                        description='Executa o comando e mostra a saída em uma notificação',
                        on_enter=RunScriptAction(
                            f'bash -c "output=$({shlex.quote(query)} 2>&1); notify-send -t 5000 \"Comando executado\" \"$output\""'
                        )
                    ))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    """Ouvinte para eventos de entrada de item"""

    def on_event(self, event, extension):
        return HideWindowAction()


if __name__ == '__main__':
    TerminalCommandExtension().run()

