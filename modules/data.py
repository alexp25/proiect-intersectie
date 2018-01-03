from modules import globals
import csv
import copy
import json

class aux:
    INDEX_ROAD = 0
    INDEX_SECTION = 1
    INDEX_FROM = 2
    INDEX_TO = 3
    INDEX_TIMESTAMP = 4
    INDEX_FLOW = 5

    section_model = {
            "number": 0,
            "direction": 1,
            "to": "",
            "from": "",
            "data": []
    }

    road_model = {
            "road": "",
            "section": []
    }

    data_model = {
            "timestamp": "",
            "flow": 0
    }

    @staticmethod
    def add_section(d):
        new_section = copy.copy(aux.section_model)
        section_number = int(d[aux.INDEX_SECTION].split(".")[0])
        section_direction = int(d[aux.INDEX_SECTION].split(".")[1])

        new_section["number"] = section_number
        new_section["direction"] = section_direction
        new_section["from"] = d[aux.INDEX_FROM]
        new_section["to"] = d[aux.INDEX_TO]
        return new_section

    @staticmethod
    def add_data(d):
        new_data = copy.copy(aux.data_model)
        new_data["timestamp"] = d[aux.INDEX_TIMESTAMP]
        new_data["flow"] = int(d[aux.INDEX_FLOW])
        return new_data

    @staticmethod
    def add_section_data(section, data):
        section["data"].append(data)

class Data:
    def __init__(self):
        self.data = None


    def load_data(self, filename="data/date_trafic_2.csv", format_file=False, p=False):
        """
        load data
        filename: date_trafic.csv - bad format, needs format file flag
                  date_trafic_1.csv - aux file, null bytes removed
                  date_trafic_2.csv - formatted file, can be used at next run
        :param filename:
        :param format_file:
        """
        filename_only = filename.split(".")[0]
        ext = filename.split(".")[1]
        data_array = []
        csv_file = filename
        try:
            if format_file:
                csv_file = filename_only + "_1." + ext
                with open(filename, 'rt') as csvfile:
                    data = csvfile.read()
                with open(csv_file, 'wt', newline="\n", encoding='utf-8-sig') as csvfile:
                    csvfile.write(data.replace('\x00', ''))

            with open(csv_file, 'rt') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                for row in reader:
                    if len(row) > 0:
                        data_array.append(row)

            if format_file:
                with open(filename_only + "_2." + ext, 'w', newline="\n", encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile, delimiter="\t")
                    for d in data_array:
                        writer.writerow(d)

            if p:
                nmax = len(data_array)
                for (i, d) in enumerate(data_array):
                    if i < nmax:
                        print(d)
                    else:
                        break

            self.data = data_array
        except:
            globals.print_exception("")

    def write_data_json(self, data, filename="data/date_trafic.json"):
        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(data, indent=2))
        except:
            globals.print_exception("write data json")

    def process_data(self, write=True):
        roads = []

        roads_names = []
        for d in self.data:
            roads_names.append(d[aux.INDEX_ROAD])

        roads_names_u = list(set(roads_names))

        for r in roads_names_u:
            new_road = copy.copy(aux.road_model)
            new_road["road"] = r
            roads.append(new_road)

        for (i, r) in enumerate(roads):
            if i < 5:
                for (i, d) in enumerate(self.data):
                    if d[aux.INDEX_ROAD] == r["road"] and i > 0:
                        print(d[aux.INDEX_ROAD])
                        section_number = int(d[aux.INDEX_SECTION].split(".")[0])
                        section_direction = int(d[aux.INDEX_SECTION].split(".")[1])
                        if len(r["section"]) == 0:
                            new_section = aux.add_section(d)
                            new_data = aux.add_data(d)
                            new_section["data"].append(new_data)
                            r["section"].append(new_section)
                        else:
                            existing_section = False
                            # add data to section
                            # or add new section with data if it does not exist
                            for s in r["section"]:
                                if section_number == s["number"] and section_direction == s["direction"]:
                                    new_data = aux.add_data(d)
                                    #s["data"].append(new_data)
                                    existing_section = True
                                    break
                            if not existing_section:
                                new_section = aux.add_section(d)
                                new_data = aux.add_data(d)
                                #new_section["data"].append(new_data)
                                r["section"].append(new_section)
                        break

        print(roads_names_u)
        print(len(roads_names_u))
        print(len(roads))

        # print(json.dumps(roads[0], indent=2))
        self.write_data_json(roads)




