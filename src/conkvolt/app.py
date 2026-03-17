import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from datetime import datetime

class ConkVolt(toga.App):
    def startup(self):
        # iOS için daha geniş padding (boşluk) ekledik
        main_box = toga.Box(style=Pack(padding=(40, 20, 20, 20), background_color='white'))
        main_box.direction = COLUMN 

        title = toga.Label('CONKVOLT iOS PRO', style=Pack(padding=(10, 0, 15, 0), font_size=22, font_weight='bold', text_align=CENTER))
        
        # Giriş Alanları
        self.guc_input = toga.TextInput(placeholder='Toplam Güç (Watt)', style=Pack(padding=5))
        self.volt_input = toga.TextInput(placeholder='Gerilim (220, 380, 400)', style=Pack(padding=5))

        # Buton - iOS'ta daha büyük ve belirgin butonlar tercih edilir
        self.btn = toga.Button('HESAPLAMAYI BAŞLAT', on_press=self.hesapla, style=Pack(padding=20, font_weight='bold'))

        # Sonuçlar
        self.faz_label = toga.Label('Sistem: -', style=Pack(padding=5, font_weight='bold'))
        self.akim_label = toga.Label('Akım: -', style=Pack(padding=2, font_size=14, font_weight='bold', color='#007AFF')) # iOS Mavisi
        self.sigorta_label = toga.Label('Sigorta: -', style=Pack(padding=2, font_size=14, font_weight='bold', color='#FF3B30')) # iOS Kırmızısı
        self.kesit_label = toga.Label('Kablo: -', style=Pack(padding=2, font_size=14, font_weight='bold', color='#34C759')) # iOS Yeşili

        # Alt Bilgi
        footer_box = toga.Box(style=Pack(padding=20, background_color='#1C1C1E')) # iOS Dark Mode Arka Planı
        footer_box.direction = COLUMN
        tarih_str = datetime.now().strftime("%d / %m / 2026")
        footer_box.add(toga.Label('DESIGN: RAMAZAN CÖNK', style=Pack(color='white', font_weight='bold', text_align=CENTER)))
        footer_box.add(toga.Label(f'RELEASE: {tarih_str}', style=Pack(color='#32D74B', font_size=10, text_align=CENTER)))

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
                self.faz_label.text = "Sistem: TRIFAZE"
            else:
                i = p / v
                self.faz_label.text = "Sistem: MONOFAZE"

            # 200A'e kadar Sigorta, 120mm'e kadar Kablo (Önceki kararlı mantık)
            st_sigortalar = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200]
            sigorta = next((x for x in st_sigortalar if x >= i * 1.25), "Özel")
            
            # Kablo Mantığı (Özel 10A sınırı dahil)
            if i <= 10 and not is_trifaze: kesit = "1.5 mm²"
            elif i <= 18: kesit = "2.5 mm²"
            elif i <= 25: kesit = "4 mm²"
            elif i <= 34: kesit = "6 mm²"
            elif i <= 46: kesit = "10 mm²"
            elif i <= 62: kesit = "16 mm²"
            elif i <= 82: kesit = "25 mm²"
            elif i <= 102: kesit = "35 mm²"
            elif i <= 124: kesit = "50 mm²"
            elif i <= 155: kesit = "70 mm²"
            elif i <= 188: kesit = "95 mm²"
            elif i <= 220: kesit = "120 mm²"
            else: kesit = "Özel Bara"

            self.akim_label.text = f"Akım: {i:.2f} A"
            self.sigorta_label.text = f"Sigorta: {sigorta} A"
            self.kesit_label.text = f"Kablo: {kesit}"
        except ValueError:
            self.faz_label.text = "Hata: Sayısal değer girin!"

def main():
    return ConkVolt('ConkVolt', 'com.conkvolt.conkvolt')
