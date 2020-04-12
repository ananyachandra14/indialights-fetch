# indialights-fetch
This is a python code to get bulk village level lights data using India Lights API - http://api.nightlights.io/

## Usage
`VillagesForState.py` is the python file with the bulk fetch logic. Run this python file to start fetching.
Paramaters at the top can be changed accordingly to fetch required bulk data.
Comments are added for explanation.


`village_dumps_by_state` folder has the respective village code dumps for each state.
The village codes required by India Lights API are 16 digit codes for villages from India's 2001 census data,
as can be seen in the first 4 columns in [West Bengal's list of villages from the census](http://censusindia.gov.in/Census_Data_2001/PLCN/DIR-19r.pdf).
Data for other states can be found [here](http://censusindia.gov.in/Census_Data_2001/PLCN/plcn.html).

Make sure to format the content like `village_dumps_by_state/wb_villages_dump.csv` if being applied for other states.
