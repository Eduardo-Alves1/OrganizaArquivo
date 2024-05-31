import PySimpleGUI as sg
import os
import shutil
import logging

from logging import handlers
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)


class SGHandeler(logging.Handler):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def emit(self, record):
        log_entry = self.format(record)
        self.window.write_event_value("-LOG-", log_entry)


sg.theme("Tan")

tela_Layout = [
    [sg.Text("Selecione a pasta que está bagunçada.", text_color="black")],
    [
        sg.Input(key="pasta_bagunçada"),
        sg.FolderBrowse("Selecionar", button_color="blue"),
    ],
    [
        sg.Text(
            "Selecione a pasta onde será organizada seus arquivos.", text_color="black"
        )
    ],
    [
        sg.Input(key="pasta_organizada"),
        sg.FolderBrowse("Selecionar", button_color="blue"),
    ],
    [
        sg.Button("Iniciar", key="Iniciar", button_color="green"),
        sg.Button("Cancelar", key="Cancelar", button_color="red"),
        sg.Button("Finalizar", key="Finalizar", button_color="black"),
    ],
    [sg.Text("PROGRESSO", text_color="black")],
    [sg.Output(size=(80, 20), key="Output")],
]

window = sg.Window("Organizador", tela_Layout, finalize=True)

sg_handle = SGHandeler(window)
sg_handle.setFormatter(log_formatter)
logger.addHandler(sg_handle)

sg.popup(
    "O programa abaixo tem como intuito organizar os arquivos de um local. O programa separará e organizará os arquivos mediante ao seu tipo. Você deve escolher o local onde será guardado os arquivos, crie uma pasta antes de iniciar.",
    text_color="black",
    title="INFO",
)
# Aqui estamos lendo os eventos da tela a too momento caso uuario feche ou cancele
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Cancelar" or event == "Finalizar":
        logger.warning("Operação Encerrada")
        break

    if event == "Iniciar":
        para_organizar = values["pasta_bagunçada"]
        # Aqui tratamos caso o usuario não selecione a pasta.
        if not para_organizar:
            logger.error(
                "Nenhuma pasta selecionada. Por favor selecione uma pasta para continuar."
            )
            sg.popup_error("Selecione uma pasta que deseja organizar.")
            continue

        logger.info(f"A Pasta: {para_organizar}, foi selecionada.")

        # Pasta onde será guardado os arquivos ja organizados.
        organizada = values["pasta_organizada"]
        if not organizada:
            logger.error(
                "Nenhuma pasta selecionada. Por favor selecione uma pasta para continuar."
            )
            sg.popup_error(
                "Selecione pasta onde será guardados os arquivos organizados."
            )
            continue
        logger.info(f"A Pasta selecionada para guardar seu arquivos foi: {organizada}")

        sleep(2)
        logger.info("Organização inciada.")

        for arquivos in os.listdir(para_organizar):
            arquivo_origem = os.path.join(para_organizar, arquivos)
            # Verifique se o caminho é um arquivo
            if os.path.isfile(arquivo_origem):
                extencao = arquivos.split(".")[-1].upper()

                pasta_extencao = os.path.join(organizada, extencao)
                if not os.path.exists(pasta_extencao):
                    os.makedirs(pasta_extencao)
                    logger.info(
                        f"Pasta para extenção {extencao} criada: {pasta_extencao}"
                    )

                shutil.move(arquivo_origem, os.path.join(pasta_extencao, arquivos))
                logger.info(f"Arquivo {arquivos} movido para a pasta {pasta_extencao}")
        logger.info("Organização concluida.")

    elif event == "-LOG-":
        log_entry = values[event]
        window["Output"].update(log_entry + "\n", append=True)

window.close()
