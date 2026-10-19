#!/usr/bin/env python3
"""
Generador de Señales Infrarrojas (IR) para Aire Acondicionado Mabe / Haier
Modelo de Control: 0010406609 / V12843 HJ RC6 E
Unidad: MMT12CABWCC32ECI1
Compatible con: Android ConsumerIrManager (POCO X3 Pro), Flipper Zero, Broadlink, Pronto Hex
"""

import sys

# Constantes de tiempos en microsegundos (µs)
CARRIER_FREQ = 38000  # 38 kHz
HDR_MARK = 3000
HDR_SPACE = 3000
BIT_MARK = 520
ZERO_SPACE = 560
ONE_SPACE = 1650

MODES = {
    "AUTO": 0x00,
    "COOL": 0x01,
    "DRY": 0x02,
    "HEAT": 0x04,
    "FAN": 0x06
}

FANS = {
    "AUTO": 0x00,
    "LOW": 0x01,
    "MED": 0x02,
    "HIGH": 0x03
}

def construir_trama(power=True, mode="COOL", temp=24, fan="AUTO", swing=True):
    """
    Construye la matriz de bytes según el protocolo Haier/Mabe AC.
    """
    if temp < 16:
        temp = 16
    elif temp > 30:
        temp = 30

    # Byte 0: Prefijo de modelo (Haier/Mabe 0xA6)
    b0 = 0xA6
    
    # Byte 1: Modo de operación
    b1 = MODES.get(mode.upper(), 0x01)
    
    # Byte 2: Temperatura (codificada desde 16°C = 0)
    b2 = (temp - 16) & 0x0F
    
    # Byte 3: Ventilador y encendido
    b3 = (FANS.get(fan.upper(), 0x00) << 4) | (0x01 if power else 0x00)
    
    # Byte 4: Swing y extras
    b4 = 0x01 if swing else 0x00
    
    # Byte 5 a 8: Flags estándar
    b5 = 0x00
    b6 = 0x00
    b7 = 0x20
    b8 = 0x00
    
    datos = [b0, b1, b2, b3, b4, b5, b6, b7, b8]
    
    # Checksum: Suma de bytes módulo 256
    checksum = sum(datos) & 0xFF
    datos.append(checksum)
    
    return datos

def bytes_a_pulsos(datos):
    """
    Convierte la lista de bytes en un patrón de pulsos [mark, space, mark, space...]
    listo para ConsumerIrManager.transmit(38000, pattern) en Android.
    """
    patron = [HDR_MARK, HDR_SPACE]
    
    for b in datos:
        for bit_idx in range(7, -1, -1):
            bit = (b >> bit_idx) & 1
            patron.append(BIT_MARK)
            if bit == 1:
                patron.append(ONE_SPACE)
            else:
                patron.append(ZERO_SPACE)
                
    patron.append(BIT_MARK)  # Pulso de parada (Stop mark)
    return patron

def main():
    print("=" * 60)
    print(" GENERADOR DE CÓDIGOS IR - AIRE ACONDICIONADO MABE / HAIER")
    print(" Control: 0010406609 | Unidad: MMT12CABWCC32ECI1 | POCO X3 Pro")
    print("=" * 60)
    
    ejemplos = [
        {"desc": "Encender (Power ON) - Modo Frío 24°C - Fan Auto", "p": True, "m": "COOL", "t": 24},
        {"desc": "Modo Frío a 22°C (Cool 22°C)", "p": True, "m": "COOL", "t": 22},
        {"desc": "Modo Frío a 18°C (Frío Intenso)", "p": True, "m": "COOL", "t": 18},
        {"desc": "Apagar (Power OFF)", "p": False, "m": "COOL", "t": 24},
    ]
    
    for ej in ejemplos:
        trama = construir_trama(power=ej["p"], mode=ej["m"], temp=ej["t"])
        pulsos = bytes_a_pulsos(trama)
        hex_str = " ".join(f"0x{b:02X}" for b in trama)
        
        print(f"\n[*] {ej['desc']}:")
        print(f"   Hex Payload: [{hex_str}]")
        print(f"   Total de pulsos: {len(pulsos)}")
        print(f"   Array para Android (ConsumerIrManager):")
        print(f"   intArrayOf({', '.join(str(p) for p in pulsos[:12])}, ...)")

if __name__ == "__main__":
    main()
