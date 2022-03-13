import pandas as pd


def init_lists(self):
    self.unit_types = ['Crew', 'Pack', 'Post', 'Ship', 'Troop', 'Other']
    self.squad_types = ['Den', 'Patrol', 'Team', 'Crew', 'Post', 'Ship', 'Other']
    self.itinerary_columns = ['Itinerary', 'Start\nStation']
    self.schedules_columns = ['Start', 'End', 'Note']
    self.youths_columns = ['First Name', 'Last Name', 'Email', 'Primary Phone', 'Unit']
    self.adults_columns = ['First Name', 'Last Name', 'Email', 'Primary Phone', 'Unit']
    self.squads_columns = ['SquadType', 'SquadName', 'Unit', 'SquadLeader', 'Itinerary']
    self.units_columns = ['UnitType', 'UnitNumber', 'Leader1', 'Leader2', 'Leader3',
                          'ParticipateFlag', 'HostFlag', 'Station']
    self.coursepoint_columns = ['StopType', 'StopID', 'NextStopType', 'NextStopID']
    self.courses_columns = ['Name', 'Description', 'FirstStop']
    self.waypoints_columns = ['Name', 'Description', 'Longitude', 'Latitude']
    self.stations_columns = ['Name', 'Description', 'Unit', 'PrimaryAdult', 'SecondaryAdult',
                             'Longitude', 'Latitude']
    self.settings_columns = ['file_onopen', 'file_directory']
    self.event_options = ['map_open', 'north', 'south', 'east', 'west']


def init_settings(self):
    self.df_settings = pd.DataFrame(columns=self.settings_columns, index=[0])
    self.df_settings.fillna(' ', inplace=True)
    return self.df_settings

def init_eventoptions(self):
    self.df_eveentoptions = pd.DataFrame(columns=self.event_options, index=[0])
    self.df_eveentoptions.fillna(' ',inplace=True)
    return self.df_eveentoptions

def init_squads(self):
    self.df_squads = pd.DataFrame(columns=self.squads_columns, index=[0, 1, 2, 3, 4, 5])
    self.df_squads.fillna(' ', inplace=True)
    for idx, row in self.df_squads.iterrows():
        row['SquadType'] = ' '
    return self.df_squads


def init_units(self):
    self.df_units = pd.DataFrame(columns=self.units_columns, index=[0, 1, 2, 3, 4, 5])
    self.df_units.fillna(' ', inplace=True)

    for idx, row in self.df_units.iterrows():
        row['UnitType'] = ' '
        row['UnitNumber'] = ' '

    return self.df_units


def init_stations(self):
    self.df_stations = pd.DataFrame(columns=self.stations_columns, index=[0, 1, 2, 3, 4, 5])
    x: float = 0.00

    for idx, row in self.df_stations.iterrows():
        row['Name'] = ' '
        row['Description'] = ' '
        row['Troop'] = ' '
        row['PrimaryAdult'] = ' '
        row['SecondaryAdult'] = ' '
        row['Longitude'] = x
        row['Latitude'] = x
    return self.df_stations


def init_waypoints(self):
    df_waypoints = pd.DataFrame(columns=self.waypoints_columns, index=[0, 1, 2, 3, 4, 5])
    df_waypoints.fillna('Empty', inplace=True)

    x: float = 0.00

    for idx, row in df_waypoints.iterrows():
        row['Name'] = ' '
        row['Description'] = ' '
        row['Longitude'] = x
        row['Latitude'] = x
    return df_waypoints


def init_courses(self):
    df_courses = pd.DataFrame(columns=self.courses_columns, index=[0, 1, 2, 3, 4, 5])
    df_courses.fillna(' ', inplace=True)
    return df_courses


def init_coursepoints(self):
    df_coursepoints = pd.DataFrame(columns=self.coursepoint_columns, index=[0, 1, 2, 3, 4, 5])
    df_coursepoints.fillna(' ', inplace=True)
    return df_coursepoints


def init_adults(self):
    df_adults = pd.DataFrame(columns=self.adults_columns, index=[0, 1, 2, 3, 4, 5])
    df_adults.fillna(' ', inplace=True)
    return df_adults


def init_youths(self):
    df_youths = pd.DataFrame(columns=self.youths_columns, index=[0, 1, 2, 3, 4, 5])
    df_youths.fillna(' ', inplace=True)
    return df_youths


def init_schedules(self):
    df_schedules = pd.DataFrame(columns=self.schedules_columns, index=[0, 1, 2, 3, 4, 5])
    df_schedules.fillna('  ', inplace=True)
    return df_schedules


def init_itineraries(self):
    df_itineraries = pd.DataFrame(columns=self.itinerary_columns, index=[0, 1, 2, 3, 4, 5])
    df_itineraries.fillna(' ', inplace=True)
    return df_itineraries
