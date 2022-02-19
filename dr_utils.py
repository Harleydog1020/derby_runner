import pandas as pd

def init_squads(self):
    self.df_squads = pd.DataFrame(columns=self.squads_columns, index=[0, 1, 2, 3, 4, 5])
    self.df_squads.fillna('Empty', inplace=True)
    for idx, row in self.df_squads.iterrows():
        row['SquadID'] = 'Q' + str(idx).zfill(3)
        row['SquadType'] = ' '
    return self.df_units


def init_units(self):
    self.df_units = pd.DataFrame(columns=self.units_columns, index=[0, 1, 2, 3, 4, 5])
    self.df_units.fillna('Empty', inplace=True)
    for idx, row in self.df_units.iterrows():
        row['UnitID'] = 'U' + str(idx).zfill(3)
        row['UnitType'] = ' '
    return self.df_units

def init_stations(self):
    self.df_stations = pd.DataFrame(columns=self.stations_columns, index=[0, 1, 2, 3, 4, 5])
    x: float = 0.00

    for idx, row in self.df_stations.iterrows():
        row['StationID'] = 'S' + str(idx).zfill(3)
        row['Name'] = 'Enter Name'
        row['Description'] = 'Enter Description'
        row['TroopID'] = ' '
        row['PrimaryAdultID'] = ' '
        row['SecondaryAdultID'] = ' '
        row['Longitude'] = x
        row['Latitude'] = x
    return self.df_stations


def init_waypoints(self):
    df_waypoints = pd.DataFrame(columns=self.waypoints_columns, index=[0, 1, 2, 3, 4, 5])
    df_waypoints.fillna('Empty', inplace=True)

    x: float = 0.00

    for idx, row in df_waypoints.iterrows():
        row['WaypointID'] = 'W' + str(idx).zfill(3)
        row['Name'] = 'Enter Name'
        row['Description'] = 'Enter Description'
        row['Longitude'] = x
        row['Latitude'] = x
    return df_waypoints


def init_courses(self):
    df_courses = pd.DataFrame(columns=self.courses_columns, index=[0, 1, 2, 3, 4, 5])
    df_courses.fillna('Empty', inplace=True)

    for idx, row in df_courses.iterrows():
        row['CourseID'] = 'C' + str(idx).zfill(3)
    return df_courses


def init_coursepoints(self):
    df_coursepoints = pd.DataFrame(columns=self.coursepoint_columns, index=[0, 1, 2, 3, 4, 5])
    df_coursepoints.fillna('Empty', inplace=True)
    for idx, row in df_coursepoints.iterrows():
        row['CoursepointID'] = 'P' + str(idx).zfill(3)
    return df_coursepoints

def init_adults(self):
    df_adults = pd.DataFrame(columns=self.adults_columns, index=[0, 1, 2, 3, 4, 5])
    df_adults.fillna('Empty', inplace=True)
    for idx, row in df_adults.iterrows():
        row['AdultID'] = 'A' + str(idx).zfill(3)
    return df_adults

def init_youths(self):
    df_youths = pd.DataFrame(columns=self.youths_columns, index=[0, 1, 2, 3, 4, 5])
    df_youths.fillna('Empty', inplace=True)
    for idx, row in df_youths.iterrows():
        row['YouthID'] = 'Y' + str(idx).zfill(3)
    return df_youths

def init_schedules(self):
    df_schedules = pd.DataFrame(columns=self.schedules_columns, index=[0, 1, 2, 3, 4, 5])
    df_schedules.fillna('Empty', inplace=True)
    for idx, row in df_schedules.iterrows():
        row['ScheduleID'] = 'H' + str(idx).zfill(3)
    return df_schedules

def init_itineraries(self):
    df_itineraries = pd.DataFrame(columns=self.itinerary_columns, index=[0, 1, 2, 3, 4, 5])
    df_itineraries.fillna('Empty', inplace=True)
    for idx, row in df_itineraries.iterrows():
        row['ItineraryID'] = 'I' + str(idx).zfill(3)
    return df_itineraries

