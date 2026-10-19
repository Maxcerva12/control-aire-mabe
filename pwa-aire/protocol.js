/**
 * Protocolo Infrarrojo para Aire Acondicionado Mabe / Haier
 * Control Remoto: 0010406609 / V12843 HJ RC6 E
 * Unidad: MMT12CABWCC32ECI1
 */

class MabeAcProtocol {
  constructor() {
    this.CARRIER_FREQ = 38000; // 38 kHz
    this.HDR_MARK = 3000;
    this.HDR_SPACE = 3000;
    this.BIT_MARK = 520;
    this.ZERO_SPACE = 560;
    this.ONE_SPACE = 1650;

    this.MODES = {
      AUTO: 0x00,
      COOL: 0x01,
      DRY: 0x02,
      HEAT: 0x04,
      FAN: 0x06
    };

    this.FANS = {
      AUTO: 0x00,
      LOW: 0x01,
      MED: 0x02,
      HIGH: 0x03
    };
  }

  buildStatePacket(state) {
    let temp = Math.max(16, Math.min(30, state.temp || 24));
    
    // Byte 0: Prefijo de modelo Haier/Mabe (0xA6)
    const b0 = 0xA6;
    
    // Byte 1: Modo de operación
    const b1 = this.MODES[state.mode] !== undefined ? this.MODES[state.mode] : 0x01;
    
    // Byte 2: Temperatura (offset desde 16°C)
    const b2 = (temp - 16) & 0x0F;
    
    // Byte 3: Ventilador y Encendido
    const fanCode = this.FANS[state.fan] !== undefined ? this.FANS[state.fan] : 0x00;
    const b3 = (fanCode << 4) | (state.power ? 0x01 : 0x00);
    
    // Byte 4: Swing
    const b4 = state.swing ? 0x01 : 0x00;
    
    // Byte 5-8: Bytes estándar
    const b5 = state.turbo ? 0x40 : 0x00;
    const b6 = state.eco ? 0x10 : 0x00;
    const b7 = 0x20;
    const b8 = 0x00;
    
    const payload = [b0, b1, b2, b3, b4, b5, b6, b7, b8];
    
    // Checksum: Suma de bytes módulo 256
    const checksum = payload.reduce((acc, val) => acc + val, 0) & 0xFF;
    payload.push(checksum);
    
    return payload;
  }

  packetToPulses(payload) {
    const pulses = [this.HDR_MARK, this.HDR_SPACE];
    
    for (const byte of payload) {
      for (let bitIdx = 7; bitIdx >= 0; bitIdx--) {
        const bit = (byte >> bitIdx) & 1;
        pulses.push(this.BIT_MARK);
        if (bit === 1) {
          pulses.push(this.ONE_SPACE);
        } else {
          pulses.push(this.ZERO_SPACE);
        }
      }
    }
    
    // Bit de parada (Stop mark)
    pulses.push(this.BIT_MARK);
    return pulses;
  }

  generateProntoHex(pulses) {
    // Frecuencia portadora 38kHz en notación Pronto: 1000000 / (38000 * 0.241246) ≈ 0x006D
    const freqCode = "006d";
    const burstCount = Math.floor(pulses.length / 2);
    const burstHex = burstCount.toString(16).padStart(4, "0");
    
    let hex = `0000 ${freqCode} ${burstHex} 0000`;
    for (const p of pulses) {
      const units = Math.round(p / 26.3); // ciclos de 38kHz
      hex += ` ${units.toString(16).padStart(4, "0")}`;
    }
    return hex;
  }
}

if (typeof window !== 'undefined') {
  window.MabeAcProtocol = MabeAcProtocol;
}

