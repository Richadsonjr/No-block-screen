import pyautogui
import time
import ctypes
import datetime
import sys


ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("dwTime", ctypes.c_uint),
    ]

def prevent_sleep():

    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )

def get_idle_duration():

    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))

    millis = ctypes.windll.kernel32.GetTickCount64() - lastInputInfo.dwTime
    return millis / 1000.0

def registrar_log(mensagem):
    hora_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_atividade_mouse.txt", "a", encoding="utf-8") as f:
        f.write(f"[{hora_atual}] {mensagem}\n")

def iniciar_preventivo():

    pyautogui.FAILSAFE = False
    
    print("========================================")
    print("   ANTI-BLOQUEIO DE TELA V2.0 (MODO HARD)")
    print("========================================")
    print("Objetivo: Impedir bloqueio após 60s ocioso.")
    print("Ações: Movimento de mouse + Tecla Shift + Signal OS.")
    print("Pressione CTRL + C para encerrar.\n")
    
    registrar_log("Iniciando monitoramento V2.0.")

    try:
        while True:
            segundos_ocioso = get_idle_duration()
            

            sys.stdout.write(f"\rOcioso há: {int(segundos_ocioso)}s | Limite: 60s   ")
            sys.stdout.flush()

            if segundos_ocioso >= 60:
                print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Atuando...")
                

                prevent_sleep()
                

                pyautogui.moveRel(10, 10)
                pyautogui.moveRel(-10, -10)
                

                pyautogui.press('shift')
                
                registrar_log(f"Atividade simulada após {int(segundos_ocioso)}s de ócio.")
                

                time.sleep(5)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        registrar_log("Script encerrado pelo usuário.")
        print("\n\n[!] Script encerrado.")
        sys.exit()

if __name__ == "__main__":
    iniciar_preventivo()
