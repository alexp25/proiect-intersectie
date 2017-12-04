from modules.network import Network

if __name__ == "__main__":
    network = Network()
    # network.load_data()
    # network.disp()
    network.load_data_json()
    network.disp()