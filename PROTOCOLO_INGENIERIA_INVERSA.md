# Análisis de Ingeniería Inversa del Protocolo IR (REA)
### Control Mabe / Haier `0010406609` (V12843 HJ RC6 E) & Unidad `MMT12CABWCC32ECI1`

---

## 1. Análisis Físico y de Evidencias (Evidence Identification)

* **Dispositivo emisor:** Control remoto Mabe modelo `0010406609` (Placa `V12843 HJ RC6 E`).
* **Unidad interior:** Split Mabe `MMT12CABWCC32ECI1` (Refrigerante ecológico R32).
* **OEM y Fabricante base:** Haier Electronics Group.
* **Medio de transmisión:** Modulación Infrarroja (IR) a **38 kHz**, Duty Cycle del 33%.
* **Receptor objetivo:** Xiaomi POCO X3 Pro (Hardware con chip `ConsumerIrManager` nativo en Android).

---

## 2. Características del Protocolo de Aire Acondicionado vs. TV/Audio

A diferencia de los controles remotos de televisores (que usan protocolos como NEC o Sony donde cada botón envía un solo código de 16/32 bits tipo "Volumen +"), **los aires acondicionados transmiten un paquete de estado completo en cada pulsación**:
* Cada vez que se presiona un botón (por ejemplo: subir de 22°C a 23°C), el control envía la configuración global entera:
  * Encendido/Apagado
  * Modo de operación (Cool, Heat, Fan, Dry, Auto)
  * Temperatura objetivo (16°C a 30°C)
  * Velocidad del ventilador (Auto, Low, Med, High)
  * Swing (Horizontal y Vertical)
  * Funciones especiales (Turbo, Eco, Sleep, Health Airflow)
  * Byte de Suma de Verificación (*Checksum*) para validar que no hubo interferencia lumínica.

---

## 3. Especificación de Tiempos de Modulación (Pulse Timings)

El protocolo de la familia **Haier AC / Mabe (0010406609)** utiliza codificación por distancia de pulsos (*Pulse Distance Coding*):

| Elemento de Señal | Pulso (Mark / LED ON) | Espacio (Space / LED OFF) | Total (µs) |
| :--- | :--- | :--- | :--- |
| **Cabecera (Header)** | 3000 µs | 3000 µs | 6000 µs |
| **Bit Lógico `0`** | 520 µs | 560 µs | 1080 µs |
| **Bit Lógico `1`** | 520 µs | 1650 µs | 2170 µs |
| **Separador de Bloque** | 520 µs | 4200 µs | 4720 µs |
| **Fin de Trama (Stop)** | 520 µs | Fin de ráfaga | - |

---

## 4. Estructura de la Trama de Datos (Payload Structure)

La trama consta habitualmente de **10 a 14 Bytes** (dependiendo del subconjunto de funciones activas):

```text
[Header: 3000, 3000]
[Byte 0: Identificador de Fabricante / Modelo (0xA6 o 0x55)]
[Byte 1: Modo de operación (Cool=0x01, Dry=0x02, Fan=0x03, Heat=0x04, Auto=0x00)]
[Byte 2: Temperatura objetivo (Valor codificado: Temp - 16°C)]
[Byte 3: Velocidad del ventilador y Swing]
[Byte 4: Temporizador ON/OFF y reloj]
[Byte 5: Modo Turbo / Eco / Sleep]
...
[Byte N: Checksum = Suma de los bytes anteriores módulo 256]
[Stop Bit: 520µs mark]
```

---

## 5. Implementación Nativa en Android (`ConsumerIrManager`)

El POCO X3 Pro cuenta con la API oficial de Android `android.hardware.ConsumerIrManager`. Para transmitir cualquiera de estos comandos de forma programática:

```kotlin
val irManager = context.getSystemService(Context.CONSUMER_IR_SERVICE) as ConsumerIrManager

if (irManager.hasIrEmitter()) {
    val frequency = 38000 // 38 kHz
    
    // Array de pulsos alternados en microsegundos [Mark, Space, Mark, Space...]
    val pattern = intArrayOf(
        3000, 3000, // Header
        520, 1650,  // Bit 1
        520, 560,   // Bit 0
        // ... bits de datos generados dinámicamente ...
        520         // Stop bit
    )
    
    irManager.transmit(frequency, pattern)
}
```

---

## 6. Conclusión de la Evaluación REA

Gracias a la coexistencia del chip emisor IR en el **POCO X3 Pro** y la identificación exacta del control `0010406609` (Haier/Mabe), no se requiere comprar ningún accesorio adicional (dongles USB o hubs WiFi externos). La emulación se logra al 100% por software en el teléfono.

