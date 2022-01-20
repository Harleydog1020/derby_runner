import pandas
import feather

class initData():
    def initEvent(self):
        event_columns = ['EventID', 'eName', 'eDescription', 'eStartDateTime', 'eEndDateTime']
        df_event = pandas.DataFrame(columns=event_columns)

    def initStations(self):
        stations_columns = ['StationID', 'sName', 'sDescription', 'TroopID', 'Primary_AdultID', 'Secondary_AdultID', 'Longitude', 'Latitude', 'EventID']
        df_stations =pandas.DataFrame(columns=stations_columns)