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
from ulauncher.api.shared.action.ShowNotificationAction import ShowNotificationAction


class TerminalCommandExtension(Extension):
    """Extensão para executar comandos do terminal via ULauncher"""

    # Comandos considerados perigosos que requerem confirmação
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
        
        require_confirm = extension.preferences.get('require_confirm', 'true') == 'true'
        show_output = extension.preferences.get('show_output', 'false') == 'true'

        items = []

        if not query:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Digite um comando para executar',
                description='Exemplo: sudo reboot, ls -la, echo "Hello"',
                on_enter=HideWindowAction()
            ))
        else:
            # Verifica se o comando é perigoso
            is_dangerous = any(query.startswith(cmd) or query.split()[0] == cmd 
                              for cmd in TerminalCommandExtension.DANGEROUS_COMMANDS)
            
            # Detecta se precisa de terminal interativo (sudo, comandos que pedem input)
            # Comandos que geralmente precisam de interação do usuário
            interactive_commands = ['sudo', 'ssh', 'mysql', 'psql', 'nano', 'vim', 'vi', 'less', 'more']
            needs_terminal = any(query.strip().startswith(cmd + ' ') or query.strip() == cmd 
                                for cmd in interactive_commands)
            
            if is_dangerous and require_confirm:
                # Mostra confirmação para comandos perigosos
                if needs_terminal:
                    # Para comandos que precisam de interação, abre em terminal
                    terminal_cmd = f'gnome-terminal -- bash -c "{shlex.quote(query)}; read -p \\"Pressione Enter para fechar...\\"" || xterm -e bash -c "{shlex.quote(query)}; read -p \\"Pressione Enter para fechar...\\"" || x-terminal-emulator -e bash -c "{shlex.quote(query)}; read -p \\"Pressione Enter para fechar...\\""'
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar: {query}',
                        description='⚠️ Comando perigoso - Abrirá em terminal para interação',
                        on_enter=RunScriptAction(terminal_cmd, run_in_background=True)
                    ))
                else:
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar: {query}',
                        description='⚠️ Comando perigoso - Pressione Enter para confirmar',
                        on_enter=RunScriptAction(
                            f'bash -c "{shlex.quote(query)}"',
                            run_in_background=False
                        )
                    ))
            else:
                # Comando normal - executa diretamente
                if needs_terminal:
                    # Para comandos que precisam de interação, abre em terminal
                    terminal_cmd = f'gnome-terminal -- bash -c "{shlex.quote(query)}; read -p \\"Pressione Enter para fechar...\\"" || xterm -e bash -c "{shlex.quote(query)}; read -p \\"Pressione Enter para fechar...\\"" || x-terminal-emulator -e bash -c "{shlex.quote(query)}; read -p \\"Pressione Enter para fechar...\\""'
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar: {query}',
                        description='Abrirá em terminal para interação',
                        on_enter=RunScriptAction(terminal_cmd, run_in_background=True)
                    ))
                else:
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar: {query}',
                        description='Pressione Enter para executar',
                        on_enter=RunScriptAction(
                            f'bash -c "{shlex.quote(query)}"',
                            run_in_background=False
                        )
                    ))
                
                # Se show_output estiver ativado, adiciona opção para mostrar saída
                if show_output:
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Executar e mostrar saída: {query}',
                        description='Executa o comando e mostra a saída em uma notificação',
                        on_enter=RunScriptAction(
                            f'bash -c "output=$({shlex.quote(query)} 2>&1); notify-send -t 5000 \"Comando executado\" \"$output\""',
                            run_in_background=False
                        )
                    ))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    """Ouvinte para eventos de entrada de item"""

    def on_event(self, event, extension):
        # A ação já foi definida no KeywordQueryEventListener
        return HideWindowAction()


if __name__ == '__main__':
    TerminalCommandExtension().run()

