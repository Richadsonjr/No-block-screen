Documentação: Anti-Bloqueio de Tela V2.0 (Modo Hard)
====================================================

Este script em Python tem como objetivo principal impedir que o sistema operacional entre em modo de suspensão, bloqueie a tela ou mude o status para "Ausente" (Away) em aplicativos de comunicação, simulando atividade humana e enviando sinais diretamente ao kernel do Windows.

🛠️ Tecnologias e Bibliotecas
-----------------------------

O script utiliza uma combinação de automação de interface e chamadas de sistema de baixo nível:

*   **pyautogui**: Utilizada para simular movimentos físicos do mouse e pressionamento de teclas.
    
*   **ctypes**: Permite chamar funções de bibliotecas dinâmicas (DLLs) do Windows (kernel32.dll e user32.dll).
    
*   **time & datetime**: Gerenciam os intervalos de execução e a formatação de horários para o log.
    
*   **sys**: Utilizado para manipulação da saída do console (refresh da linha de contagem).
    

🏗️ Estrutura do Código
-----------------------

### 1\. Prevenção de Suspensão via Kernel (prevent\_sleep)

Diferente de apenas mover o mouse, esta função utiliza a API do Windows SetThreadExecutionState.

*   **ES\_CONTINUOUS**: Mantém o estado definido até a próxima chamada.
    
*   **ES\_SYSTEM\_REQUIRED**: Impede que o computador entre em suspensão.
    
*   **ES\_DISPLAY\_REQUIRED**: Impede que o monitor/monitor apague.
    

### 2\. Monitoramento de Ociosidade (get\_idle\_duration)

O script é inteligente: ele não fica movendo o mouse o tempo todo. Ele utiliza a estrutura LASTINPUTINFO para perguntar ao Windows: _"Há quantos milissegundos houve a última interação física (teclado ou mouse)?"_. O movimento só ocorre se esse tempo exceder 60 segundos.

### 3\. Simulação de Atividade (O "Modo Hard")

Quando o limite de 60s é atingido, o script executa uma tríade de ações:

1.  **Sinal de Sistema**: Notifica o Windows para manter a tela ligada.
    
2.  **Movimento Relativo**: Move o mouse 10 pixels para baixo/direita e volta para a posição original rapidamente.
    
3.  **Tecla Neutra**: Pressiona a tecla Shift, que é uma tecla "segura" (geralmente não interfere em janelas abertas ou digitação acidental).
    

### 4\. Sistema de Logging

Todas as ativações são registradas no arquivo log\_atividade\_mouse.txt. Isso permite auditar em quais horários o script precisou atuar para manter a máquina ativa.

⚙️ Funcionamento do Loop Principal
----------------------------------

1.  **Início**: Configura o pyautogui.FAILSAFE = False para evitar que o script pare se o mouse bater no canto da tela.
    
2.  **Checagem**: A cada 1 segundo, verifica o tempo de ociosidade.
    
3.  **Feedback Visual**: Exibe no console um contador dinâmico: Ocioso há: Xs | Limite: 60s.
    
4.  **Ação**: Se ocioso >= 60s, executa a rotina de movimento, registra o log e aguarda 5 segundos para estabilizar.
    
5.  **Interrupção**: O script roda indefinidamente até que o usuário pressione CTRL + C.
    

⚠️ Requisitos e Avisos
----------------------

*   **Sistema Operacional**: Windows (devido ao uso de ctypes.windll).
    
*   Bashpip install pyautogui
    
*   **Uso Ético**: Este tipo de ferramenta é geralmente utilizado para manter sessões de processamento longas ativas ou apresentações. Verifique as políticas de conformidade da sua organização antes de utilizá-lo em ambientes corporativos.
    

### Exemplo de Log Gerado

> \[2023-10-27 10:15:30\] Iniciando monitoramento V2.0.
> 
> \[2023-10-27 10:20:45\] Atividade simulada após 60s de ócio.
