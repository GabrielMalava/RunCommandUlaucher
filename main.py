#!/usr/bin/env python3
"""
ULauncher Extension - Terminal Command Executor
Executa comandos do terminal diretamente do ULauncher
"""

import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


INTERACTIVE_COMMANDS = [
    'sudo', 'ssh', 'mysql', 'psql', 'nano', 'vim', 'vi', 'less', 'more',
    'top', 'htop', 'man', 'watch', 'tail -f', 'journalctl'
]

DANGEROUS_COMMANDS = [
    'sudo', 'rm', 'dd', 'mkfs', 'fdisk', 'shutdown', 'reboot',
    'poweroff', 'halt', 'killall', 'pkill', 'kill'
]


def needs_interactive_terminal(cmd):
    """Verifica se o comando precisa de um terminal interativo"""
    cmd_lower = cmd.lower().strip()
    for interactive in INTERACTIVE_COMMANDS:
        if cmd_lower.startswith(interactive + ' ') or cmd_lower == interactive:
            return True
    return False


def is_dangerous_command(cmd):
    """Verifica se é um comando perigoso"""
    if not cmd:
        return False
    first_word = cmd.split()[0].lower()
    return first_word in DANGEROUS_COMMANDS


def escape_for_shell(cmd):
    """Escapa o comando para uso em shell de forma segura"""
    return cmd.replace("'", "'\\''")


class TerminalCommandExtension(Extension):
    """Extensão para executar comandos do terminal via ULauncher"""

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    """Ouvinte para eventos de consulta por palavra-chave"""

    def on_event(self, event, extension):
        query = (event.get_argument() or "").strip()
        items = []

        if not query:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Digite um comando para executar',
                description='Exemplo: ls -la, echo "Hello", git status',
                on_enter=HideWindowAction()
            ))
            return RenderResultListAction(items)

        dangerous = is_dangerous_command(query)
        warning = ' ⚠️ Comando perigoso!' if dangerous else ''
        escaped_cmd = escape_for_shell(query)

        background_script = f"nohup bash -c '{escaped_cmd}' > /dev/null 2>&1 &"
        
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f'▶ Executar: {query}',
            description=f'Executa em background (sem janela){warning}',
            on_enter=RunScriptAction(background_script)
        ))

        home_dir = os.path.expanduser("~")
        terminal_script = f"gnome-terminal --working-directory=\"{home_dir}\" -- bash --login -c '{escaped_cmd}; echo; echo Pressione ENTER para fechar...; read'"
        
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f'🖥️ Abrir em terminal: {query}',
            description=f'Abre terminal para ver a saída{warning}',
            on_enter=RunScriptAction(terminal_script)
        ))

        notify_script = f"bash -c 'output=$({escaped_cmd} 2>&1); notify-send -t 10000 \"Resultado\" \"$output\"'"
        
        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f'🔔 Executar e notificar: {query}',
            description=f'Mostra resultado em notificação{warning}',
            on_enter=RunScriptAction(notify_script)
        ))

        return RenderResultListAction(items)


if __name__ == '__main__':
    TerminalCommandExtension().run()
