# Derby Runner
<img
  src="https://github.com/Harleydog1020/derby_runner/blob/NextPhase/resources/Screenshot1.png"
  title="Derby Runner Example Screenshot"
  width="500">
This is an open source python project that attempts to provide a GUI interface to tables and reports to facilitate managing and scoring Scouting events like Klondike Derby.  The intention is that it be simple and straight forward so that non-technical types can have some hope at downloading, installing and running it with little or no help from a highly skilled programmer.  How close to that goal it can get will remain to be seen.  Some time has been invested.  Here some of the accomplishments to date:
* A Table style editor at a basic level and tables of data for:
*   Units: like Troops, Crews, Packs, Ships, etc.
*   Squads: like Patrols, Dens, Teams
*   Places: Stations with activities; Waypoints, landmarks but no activities; courses, which are an ordered collection of places
*   People: adults, youths, and their assignements
*   A map function has been added as well as a calendar
*   the beginnings of custom, field level editors for dropdowns and dates in the table editor

All of these are stored in a single file for each "Event", using h5 file format so that they can all be kept together
