# Proyecto: Control de Aire Acondicionado Mabe con Xiaomi POCO X3 Pro

Este proyecto contiene la solución completa, análisis de ingeniería inversa y archivos necesarios para controlar tu aire acondicionado **Mabe** desde tu teléfono **Xiaomi POCO X3 Pro** utilizando su emisor infrarrojo (IR Blaster) integrado.

---

## 📂 Contenido de esta Carpeta

1. **[GUIA_CONFIGURACION_POCO_X3_PRO.md](GUIA_CONFIGURACION_POCO_X3_PRO.md)**
   * **¡Léelo primero!** Guía paso a paso para configurar tu POCO X3 Pro en 2 minutos usando la aplicación oficial **Mi Remoto** de Xiaomi o **ZaZa Remote**.
   * Incluye el secreto de compatibilidad de marcas (Mabe / Haier OEM).

2. **[PROTOCOLO_INGENIERIA_INVERSA.md](PROTOCOLO_INGENIERIA_INVERSA.md)**
   * Documento técnico de ingeniería inversa elaborado bajo la metodología **REA (Reverse Engineering Analysis)**.
   * Modulación 38 kHz, temporización de microsegundos (Mark/Space), codificación de tramas de estado completo y checksum.
   * Implementación de la API de Android `ConsumerIrManager`.

3. **[generador_ir_mabe_haier.py](generador_ir_mabe_haier.py)**
   * Script en Python que calcula los paquetes hexadecimales y los arrays de pulsos en microsegundos para cualquier combinación de temperatura (16°C a 30°C), modo (Cool, Dry, Heat, Fan), ventilador y encendido/apagado.

---

## 🎯 Resumen de Identificación de Equipos

* **Teléfono:** Xiaomi POCO X3 Pro (Hardware: Emisor de Infrarrojos 38 kHz).
* **Unidad de Aire:** Split Mabe Inverter 12,000 BTU (`MMT12CABWCC32ECI1`, Serie `ST25123021FEAO3000`).
* **Control Remoto Físico:** Mabe OEM Haier (`0010406609` / `V12843 HJ RC6 E`).

