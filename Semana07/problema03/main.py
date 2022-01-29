from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
import requests

gui = Builder.load_file("screen.kv")

class CurrenceScraper(App):
    def build(self):
        return gui

    def on_start(self):
        self.root.ids["currence1"].text = f"Dolar R${self.get_quotation('USD')}"
        self.root.ids["currence2"].text = f"Euro R${self.get_quotation('EUR')}"
        self.root.ids["currence3"].text = f"Bitcoin R${self.get_quotation('BTC')}"
        self.root.ids["currence4"].text = f"Ethereum R${self.get_quotation('ETH')}"

    def get_quotation(self, currence):
        link = f"https://economia.awesomeapi.com.br/last/{currence}-BRL"
        request = requests.get(link)
        request_dict = request.json()
        quotation = request_dict[f"{currence}BRL"]["bid"]
        return quotation

if __name__ == "__main__":
    Config.set('graphics', 'width', '1100')
    Config.set('graphics', 'height', '300')
    Config.write()
    CurrenceScraper().run()
    