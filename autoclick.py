"""
╔══════════════════════════════════════════════════╗
║          ⛏️  MINECRAFT AUTOCLICKER  ⛏️           ║
║                                                  ║
║  F6  → Activar / Desactivar                     ║
║  F7  → Cambiar entre click izq / der            ║
║  F8  → Subir CPS (+1)                           ║
║  F9  → Bajar CPS (-1)                           ║
║  ESC → Salir del programa                        ║
╚══════════════════════════════════════════════════╝
"""

import threading
import time
import sys
import os

try:
    from pynput.mouse import Button, Controller as MouseController
    from pynput.keyboard import Key, Listener as KeyboardListener
except ImportError:
    print("\n❌ Necesitas instalar 'pynput'. Ejecuta:")
    print("   pip install pynput\n")
    sys.exit(1)


# ─── Configuración ───────────────────────────────────────────
class AutoClicker:
    def __init__(self):
        self.mouse = MouseController()
        self.clicking = False
        self.running = True
        self.cps = 10              # Clicks por segundo (default)
        self.min_cps = 1
        self.max_cps = 50
        self.button = Button.left  # Botón del mouse
        self.button_name = "IZQ"
        self.click_count = 0
        self.lock = threading.Lock()

    def toggle(self):
        """Activa o desactiva el autoclicker."""
        with self.lock:
            self.clicking = not self.clicking
            if self.clicking:
                self.click_count = 0
        self.print_status()

    def change_button(self):
        """Cambia entre click izquierdo y derecho."""
        with self.lock:
            if self.button == Button.left:
                self.button = Button.right
                self.button_name = "DER"
            else:
                self.button = Button.left
                self.button_name = "IZQ"
        self.print_status()

    def increase_cps(self):
        """Sube el CPS en 1."""
        with self.lock:
            if self.cps < self.max_cps:
                self.cps += 1
        self.print_status()

    def decrease_cps(self):
        """Baja el CPS en 1."""
        with self.lock:
            if self.cps > self.min_cps:
                self.cps -= 1
        self.print_status()

    def click_loop(self):
        """Hilo principal que ejecuta los clicks."""
        while self.running:
            if self.clicking:
                with self.lock:
                    self.mouse.click(self.button)
                    self.click_count += 1
                    interval = 1.0 / self.cps
                time.sleep(interval)
            else:
                time.sleep(0.05)  # Espera ligera cuando está inactivo

    def on_key_press(self, key):
        """Maneja las teclas presionadas."""
        try:
            if key == Key.f6:
                self.toggle()
            elif key == Key.f7:
                self.change_button()
            elif key == Key.f8:
                self.increase_cps()
            elif key == Key.f9:
                self.decrease_cps()
            elif key == Key.esc:
                self.stop()
                return False  # Detiene el listener
        except Exception:
            pass

    def stop(self):
        """Detiene todo el programa."""
        self.clicking = False
        self.running = False
        self.clear_screen()
        print("\n  👋 ¡Autoclicker cerrado! Buena partida.\n")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_status(self):
        """Muestra el estado actual en consola."""
        self.clear_screen()
        state = "🟢 ACTIVO" if self.clicking else "🔴 INACTIVO"
        bar_len = min(self.cps, 50)
        bar = "█" * bar_len + "░" * (50 - bar_len)

        print(f"""
╔══════════════════════════════════════════════════════╗
║            ⛏️  MINECRAFT AUTOCLICKER  ⛏️              ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   Estado:    {state:<39s} ║
║   CPS:       {self.cps:<39d} ║
║   Botón:     {self.button_name:<39s} ║
║   Clicks:    {self.click_count:<39d} ║
║                                                      ║
║   Velocidad: [{bar}] ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║   F6  → Activar / Desactivar                        ║
║   F7  → Cambiar botón (izq/der)                     ║
║   F8  → Subir CPS (+1)                              ║
║   F9  → Bajar CPS (-1)                              ║
║   ESC → Salir                                        ║
╚══════════════════════════════════════════════════════╝
""")

    def start(self):
        """Inicia el autoclicker."""
        self.print_status()

        # Hilo de clicks
        click_thread = threading.Thread(target=self.click_loop, daemon=True)
        click_thread.start()

        # Listener de teclado (bloquea hasta ESC)
        with KeyboardListener(on_press=self.on_key_press) as listener:
            listener.join()


# ─── Main ────────────────────────────────────────────────────
if __name__ == "__main__":
    auto = AutoClicker()
    auto.start()
