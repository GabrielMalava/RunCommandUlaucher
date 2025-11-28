#!/usr/bin/env python3
"""
ULauncher Extension - Terminal Command Executor
Executa comandos do terminal diretamente do ULauncher
"""

import subprocess
import shlex
import os
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
            
            # Verifica se o comando existe no PATH do bash
            cmd_name = query.split()[0]
            cmd_exists_in_bash = False
            try:
                result = subprocess.run(['bash', '-c', f'command -v {shlex.quote(cmd_name)}'], 
                                       capture_output=True, timeout=1)
                cmd_exists_in_bash = result.returncode == 0
            except:
                pass
            
            use_fish = not cmd_exists_in_bash
            
            if needs_terminal:
                if use_fish:
                    # Escapa aspas duplas
                    escaped_query = query.replace('"', '\\"')
                    cmd_str = f'gnome-terminal -- fish --login -c "{escaped_query}; exec fish"'
                else:
                    expanded_path = os.environ.get('PATH', '') + ':' + os.path.expanduser('~/.local/bin') + ':' + os.path.expanduser('~/bin')
                    escaped_query = query.replace('"', '\\"')
                    cmd_str = f'gnome-terminal -- bash -c "export PATH={expanded_path}; {escaped_query}; read -p \\"Pressione Enter para fechar...\\""'
                
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=f'Executar: {query}',
                    description='Abrirá em terminal para interação' + (' - Comando perigoso!' if is_dangerous else ''),
                    on_enter=RunScriptAction(cmd_str)
                ))
            else:
                expanded_path = '$HOME/.local/bin:$HOME/bin:$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
                if use_fish:
                    cmd_str = f'fish --login -c {shlex.quote(query)} &'
                else:
                    cmd_str = f'bash -c "export PATH={expanded_path}; {shlex.quote(query)} &"'
                
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=f'Executar: {query}',
                    description='Pressione Enter para executar' + (' - Comando perigoso!' if is_dangerous else ''),
                    on_enter=RunScriptAction(cmd_str)
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
    """Ouvinte para eventos de entrada de item - executa comandos diretamente"""

    def on_event(self, event, extension):
        action = event.get_action()
        
        # Executa diretamente via subprocess quando RunScriptAction é acionado
        if isinstance(action, RunScriptAction):
            try:
                cmd = action.script
                # Executa o comando diretamente em background
                subprocess.Popen(cmd, shell=True, start_new_session=True, 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                              stdin=subprocess.DEVNULL)
            except Exception as e:
                pass
        
        # Retorna HideWindowAction imediatamente para não travar
        return HideWindowAction()


if __name__ == '__main__':
    TerminalCommandExtension().run()
