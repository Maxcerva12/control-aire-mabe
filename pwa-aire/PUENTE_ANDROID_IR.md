# Cómo Conectar la PWA al Emisor Infrarrojo de tu POCO X3 Pro

La aplicación web / PWA que acabamos de crear calcula en tiempo real los pulsos de **38 kHz** y los paquetes de estado para el protocolo de tu aire Mabe / Haier (`0010406609`).

---

## 🔒 La Realidad Técnica de los Navegadores Móviles

Por motivos de seguridad y privacidad del consorcio W3C, **Google Chrome y los navegadores móviles estándar no permiten que una página web común acceda directamente al hardware del LED Infrarrojo del teléfono** (no existe una API web `navigator.infrared`).

Sin embargo, hay **3 formas excelentes y probadas** para que esta PWA active el infrarrojo físico de tu POCO X3 Pro:

---

## 🚀 Método A: Contenedor Android Nativo con WebView (Recomendado)

Convertir la PWA en una aplicación instalada en tu POCO X3 Pro que use el componente nativo `ConsumerIrManager` de Android.

El archivo `index.html` ya tiene listo el puente JavaScript:
```javascript
if (window.AndroidIR && window.AndroidIR.transmit) {
    window.AndroidIR.transmit(38000, JSON.stringify(pulses));
}
```

En el proyecto Android (en Kotlin o Java), solo se añade este puente al WebView:

```kotlin
// MainActivity.kt
class MainActivity : AppCompatActivity() {
    private lateinit var irManager: ConsumerIrManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val webView = WebView(this)
        setContentView(webView)

        irManager = getSystemService(Context.CONSUMER_IR_SERVICE) as ConsumerIrManager

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true

        // Inyectar el puente JavaScript
        webView.addJavascriptInterface(object {
            @JavascriptInterface
            fun transmit(carrierFreq: Int, patternJson: String) {
                val jsonArray = JSONArray(patternJson)
                val pattern = IntArray(jsonArray.length()) { i -> jsonArray.getInt(i) }
                
                // Emite la señal física por el hardware del POCO X3 Pro
                irManager.transmit(carrierFreq, pattern)
            }
        }, "AndroidIR")

        // Cargar la PWA (localmente desde assets o desde tu servidor)
        webView.loadUrl("file:///android_asset/index.html")
    }
}
```

---

## 📲 Método B: Usando Termux + Termux:API en tu POCO X3 Pro

Si no quieres compilar una app con Android Studio:
1. Instala **Termux** y **Termux:API** en tu POCO X3 Pro desde F-Droid.
2. Termux incluye el comando nativo `termux-infrared-transmit`:
   ```bash
   pkg install python termux-api
   ```
3. Copias la carpeta `pwa-aire` a tu teléfono y ejecutas:
   ```bash
   python server.py
   ```
4. Al abrir `http://localhost:8080` en Chrome en tu teléfono, el servidor Python llama internamente a `termux-infrared-transmit` y ¡tu aire responderá directamente desde la web!

---

## 🌐 Método C: Emisor WiFi IoT (ESP8266 / ESP32)

Si deseas poder controlar el aire **desde cualquier lugar de tu casa (o fuera de ella)** sin necesidad de apuntar el teléfono directamente a la unidad:
* Un módulo **ESP32 o D1 Mini** (cuesta menos de $3 USD) con un pequeño LED infrarrojo apuntando al aire.
* Se conecta a tu red WiFi local.
* Cuando tocas cualquier botón en la PWA (desde tu PC, iPhone, Android o tablet), la PWA envía la petición HTTP al ESP32 y este dispara la ráfaga infrarroja al aire.

