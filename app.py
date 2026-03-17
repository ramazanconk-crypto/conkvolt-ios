import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from datetime import datetime

class ConkVolt(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(padding=15, background_color='white'))
        main_box.direction = COLUMN 

        title = toga.Label('Sigorta ve Kablo Hesaplama', style=Pack(padding=(0, 0, 5, 0), font_size=20, font_weight='bold', text_align=CENTER))
        
        self.guc_input = toga.TextInput(placeholder='Güç (Watt) - Örn: 50000', style=Pack(padding=5))
        self.volt_input = toga.TextInput(placeholder='Gerilim (Volt) - Örn: 220 veya 380', style=Pack(padding=5))

        self.btn = toga.Button('GENİŞ KAPSAMLI HESAPLA', on_press=self.hesapla, style=Pack(padding=15, font_weight='bold'))

        self.faz_label = toga.Label('Sistem: -', style=Pack(padding=5, font_weight='bold'))
        self.akim_label = toga.Label('Akım: -', style=Pack(padding=2, font_size=13, font_weight='bold', color='#0056b3'))
        self.sigorta_label = toga.Label('Sigorta: -', style=Pack(padding=2, font_size=13, font_weight='bold', color='#d9534f'))
        self.kesit_label = toga.Label('Kablo Kesiti: -', style=Pack(padding=2, font_size=14, font_weight='bold', color='#28a745'))

        footer_box = toga.Box(style=Pack(padding=15, background_color='#222222'))
        footer_box.direction = COLUMN
        tarih_str = datetime.now().strftime("%d / %m / 2026")
        footer_box.add(toga.Label('TASARIM: RAMAZAN CÖNK', style=Pack(color='white', font_weight='bold', text_align=CENTER)))
        footer_box.add(toga.Label(f'FULL CAPACITY: {tarih_str}', style=Pack(color='#00FF00', font_size=10, text_align=CENTER)))

        main_box.add(title)
        main_box.add(self.guc_input)
        main_box.add(self.volt_input)
        main_box.add(self.btn)
        main_box.add(self.faz_label)
        main_box.add(self.akim_label)
        main_box.add(self.sigorta_label)
        main_box.add(self.kesit_label)
        main_box.add(footer_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def hesapla(self, widget):
        try:
            p = float(self.guc_input.value)
            v = float(self.volt_input.value)
            
            is_trifaze = v >= 300
            if is_trifaze:
                i = p / (v * 1.732)
                self.faz_label.text = "Sistem: TRIFAZE (3 Fazlı)"
            else:
                i = p / v
                self.faz_label.text = "Sistem: MONOFAZE (1 Fazlı)"

            # --- SİGORTA TABLOSU (200A'e kadar) ---
            st_sigortalar = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250]
            sigorta_akimi = i * 1.25
            sigorta = next((x for x in st_sigortalar if x >= sigorta_akimi), "Özel Kompakt Şalter")
            
            # --- GENİŞLETİLMİŞ KABLO KESİT TABLOSU (120mm²'ye kadar) ---
            if i <= 10 and not is_trifaze:
                kesit = "1.5 mm²"
            elif i <= 18:
                kesit = "2.5 mm²"
            elif i <= 25:
                kesit = "4 mm²"
            elif i <= 34:
                kesit = "6 mm²"
            elif i <= 46:
                kesit = "10 mm²"
            elif i <= 62:
                kesit = "16 mm²"
            elif i <= 82:
                kesit = "25 mm²"
            elif i <= 102:
                kesit = "35 mm²"
            elif i <= 124:
                kesit = "50 mm²"
            elif i <= 155:
                kesit = "70 mm²"
            elif i <= 188:
                kesit = "95 mm²"
            elif i <= 220:
                kesit = "120 mm²"
            else:
                kesit = "150 mm² veya Bara Sistemi"

            self.akim_label.text = f"Hesaplanan Akım: {i:.2f} A"
            self.sigorta_label.text = f"Emniyetli Sigorta: {sigorta} A"
            self.kesit_label.text = f"Önerilen Kablo: {kesit}"
            
        except ValueError:
            self.faz_label.text = "Hata: Geçersiz değer!"

def main():
    return ConkVolt('ConkVolt', 'com.conkvolt.conkvolt')