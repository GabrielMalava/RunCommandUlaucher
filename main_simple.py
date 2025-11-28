#!/usr/bin/env python3
"""
ULauncher Extension - Terminal Command Executor (Versão Simplificada)
"""

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


class TerminalCommandExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        query = query.strip()
        
        items = []
        
        if not query:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Digite um comando para executar',
                description='Exemplo: ls, echo "teste", sudo reboot',
                on_enter=HideWindowAction()
            ))
        else:
            # Versão simples - executa o comando diretamente
            # RunScriptAction aceita apenas o comando como string
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=f'Executar: {query}',
                description='Pressione Enter para executar este comando',
                on_enter=RunScriptAction(query)
            ))
        
        return RenderResultListAction(items)


if __name__ == '__main__':
    TerminalCommandExtension().run()

