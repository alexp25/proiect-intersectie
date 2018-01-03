from modules.network import Network
from modules.data import Data

if __name__ == "__main__":
    network = Network()
    data = Data()
    # network.load_data()
    # network.disp()


    network.load_data_json()
    # network.disp()

    data.load_data()
    # data.process_data()