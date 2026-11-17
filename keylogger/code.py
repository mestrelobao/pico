import sys
import board
import usb_host
import supervisor

# Configuração dos Pinos GPIO do USB Host Fêmea (Altere se necessário)
PINO_DP = board.GP16  # Dados + (D+)
PINO_DM = board.GP17  # Dados - (D-)

def inicializar_usb_host():
    """Inicializa a porta física de USB Host via PIO."""
    try:
        # A porta permanece ativa em segundo plano no CircuitPython
        porta = usb_host.Port(PINO_DP, PINO_DM)
        print("-" * 40)
        print("SISTEMA: Porta USB Host inicializada com sucesso!")
        print("SISTEMA: Conecte o teclado USB na porta secundária.")
        print("-" * 40)
        return porta
    except Exception as erro:
        print(f"ERRO CRÍTICO: Falha ao abrir porta USB Host: {erro}")
        return None

def processar_teclado():
    """Monitora o buffer e processa os caracteres digitados no teclado."""
    # Verifica quantos bytes estão esperando no buffer do stdin
    bytes_no_buffer = supervisor.runtime.serial_bytes_available

    if bytes_no_buffer > 0:
        # Lê os caracteres disponíveis
        dados_brutos = sys.stdin.read(bytes_no_buffer)

        for caractere in dados_brutos:
            # Tratamento estético para a quebra de linha (Enter)
            if caractere in ("\r", "\n"):
                print()  # Pula a linha no console do computador

            # Tratamento para a tecla Backspace apagar o caractere anterior no console
            elif caractere == "\x08":
                print("\b \b", end="")

            # Exibe caracteres normais na tela do computador
            else:
                print(caractere, end="")

# --- Execução Principal ---
# Garante a inicialização da porta ao iniciar a Pico
porta_ativa = inicializar_usb_host()

while True:
    if porta_ativa is not None:
        processar_teclado()
    else:
        # Pisca um aviso ou aguarda caso a inicialização falhe
        pass
