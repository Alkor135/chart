import time
import configparser
from binance import ThreadedWebsocketManager

# Loading keys from config file
config = configparser.ConfigParser()
config.read_file(open('secret.cfg'))
api_key = config.get('BINANCE', 'ACTUAL_API_KEY')
api_secret = config.get('BINANCE', 'ACTUAL_SECRET_KEY')


def main():
    symbol = 'BTCUSDT'

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"\nmessage type: {msg['e']}")
        print(f"Best bid price: {float(msg['b'][0][0]):.2f}.")
        print(f"Best ask price: {float(msg['a'][0][0]):.2f}.")
        # print(msg)

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # multiple sockets can be started
    twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    # streams = ['btcusdt@miniTicker', 'btcusdt@bookTicker']
    streams = ['btcusdt@bookTicker']
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

    twm.join()


if __name__ == "__main__":
   main()
