import pandas
import feather

class initData():
    def initEvents(self):
        event_columns = ['EventID', 'eName', 'eDescription', 'eStartDateTime', 'eEndDateTime']
        df_event = pandas.DataFrame(columns=event_columns, index=[1, 2, 3, 4, 5])

    def initStations(self):
        stations_columns = ['StationID', 'sName', 'sDescription', 'TroopID', 'Primary\nAdultID', 'Secondary\nAdultID',
                            'Longitude', 'Latitude', 'EventID']
        df_stations = pandas.DataFrame(columns=stations_columns, index=[1, 2, 3, 4, 5])
        df_stations.to_feather(stationsFile)
