# indialights-fetch
This is a python code to get bulk village level lights data using India Lights API - http://api.nightlights.io/

## Usage
`VillagesForState.py` is the python file with the bulk fetch logic. Run this python file to start fetching.
Paramaters at the top can be changed accordingly to fetch required bulk data.
Comments are added for explanation.


`village_dumps_by_state` folder has the respective village code dumps for each state.
Village code dumps are information about all the villages in a state according to India's 2001 census.
The village codes required by India Lights API are 16 digit codes for villages from India's 2001 census data,
as can be seen in the first 4 columns in [West Bengal's list of villages from the census](http://censusindia.gov.in/Census_Data_2001/PLCN/DIR-19r.pdf).
Data for other states can be found [here](http://censusindia.gov.in/Census_Data_2001/PLCN/plcn.html).

Village dumps for 6 states - Assam, Andhra Pradesh, Bihar, Uttar Pradesh, Orissa and West Bengal have been added.
These are mandatory and required for traversing line by line to hit the India Lights API with the village code.
For any other states, follow these steps to get the dump file. It should take 5 minutes and
be formatted like `village_dumps_by_state/wb_villages_dump.csv` at the end of it.

Steps to create village dump file:
1. Download census 2001 data for respective state from [here](http://censusindia.gov.in/Census_Data_2001/PLCN/plcn.html).
2. Open in preferred PDF reader and copy all contents (this may take some time) to a text editor which supports regex, like [Sublime Text](https://www.sublimetext.com/).
3. Enter Find mode (Ctrl+F on Windows or Cmd+F on Mac).
4. Enter `^[0-9]{2} [0-9]{2} [0-9]{4} [0-9]{8} .*`. This searches for all relevant entries.
5. Click Find All.
6. Copy the content. Paste it in a new file and save it inside `village_dumps_by_state` folder.
7. Update the `village_dump_file_path` parameter in the python file.

## Sample data
![sample screenshot](./screenshots/sample_data_image.png)
