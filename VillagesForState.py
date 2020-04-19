import requests
import os
import re
from datetime import datetime
from pathlib import Path
from utils.get_meta_data_for_state import get_meta_data_for_state
from utils.State import State

folder = os.getcwd() + "/data/"

# Parameters to be changed
state = State.UTTAR_PRADESH    # Change this to corresponding state for which data is to be fetched eg. State.ORISSA for fetching data for villages in Orissa.


# Specifying range of download
download_all_villages   = False                     # If set to True, all villages' data are fetched.
                                                    # starting_village_number and ending_village_number parameters are used only if this is set to False.
starting_village_number = "00000000"                # Check the sample village dumps inside village_dumps_by_state. The 4th column denotes this.
                                                    # Enter the village number from which you need to start fetching.
                                                    # Not used when download_all_villages is set to False.
ending_village_number   = "00000200"                # Bulk fetch will stop at this village number, including this.
                                                    # Not used when download_all_villages is set to False.

# Misc parameters
append_to_file       = False                        # This will append data to append_to_file_name file if set to True, and a new file will be not be created.
append_to_file_name  = "andhra_village_data-13.04.2020-05.11.55"
                                                    # Change this to the file name to which data is to be appended when append_to_file is set to True.
                                                    # Not used when append_to_file is False.
keep_empty_data_rows = True                         # If set to True, villages with empty data are kept in the data file.

# Starting and ending months for each village fetch
start_year              = "2008"
start_month             = "1"
end_year                = "2013"
end_month               = "12"


###


# Methods
def write_line_in_file(
        il_village_id,
        state_name,
        state,
        district_name,
        district,
        sub_district_name,
        sub_district,
        constituency,
        village_name,
        village,
        year,
        month,
        count,
        min,
        max,
        mean,
        median
):
    output_file.write(
        il_village_id + "," +
        state_name + "," +
        state + "," +
        district_name + "," +
        district + "," +
        sub_district_name + "," +
        sub_district + "," +
        constituency + "," +
        village_name + "," +
        village + "," +
        str(year) + "," +
        str(month) + "," +
        str(count) + "," +
        str(min )+ "," +
        str(max) + "," +
        str(mean) + "," +
        str(median) + "\n"
    )


def parse_response(response, village_object):
    global current_state_name, current_district_name, current_sub_district_name
    if response.status_code and response.status_code == 200:
        json = response.json()
        if len(json) == 0:
            if keep_empty_data_rows:
                write_line_in_file(
                    village_object.india_lights_village_code,
                    current_state_name,
                    village_object.state_code,
                    current_district_name,
                    village_object.district_code,
                    current_sub_district_name,
                    village_object.sub_district_code,
                    village_object.constituency,
                    village_object.village_name,
                    village_object.village_code,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                )
            no_data_text = "### No data for village " + village_object.village_code + "\n"
            print(no_data_text)
            error_file.write(no_data_text)
        else:
            for month_data in json:
                write_line_in_file(
                    village_object.india_lights_village_code,
                    current_state_name,
                    village_object.state_code,
                    current_district_name,
                    village_object.district_code,
                    current_sub_district_name,
                    village_object.sub_district_code,
                    village_object.constituency,
                    village_object.village_name,
                    village_object.village_code,
                    month_data['year'],
                    month_data['month'],
                    month_data['count'],
                    month_data['vis_min'],
                    month_data['vis_max'],
                    month_data['vis_mean'],
                    month_data['vis_median']
                )
            print("Download complete")
    else:
        error_text = "###### Error for village: " + village_object.village_code + "\n" + response.json()['message'] + "\n\n\n\n\n"
        print(error_text)
        error_file.write(error_text)


def get_progress(village_number):
    current = int(village_number[:-2])
    if download_all_villages:
        perc_complete = current/last_village_int * 100
    else:
        progress = current - start_village_int
        perc_complete = progress / village_diff * 100

    return round(perc_complete, 2)


def download_data_for_village(india_lights_village_code, village_number):
    print("Downloading village code: " + india_lights_village_code + "\tVillage number: " + village_number + "\tProgress: " + str(get_progress(village_number)) + "%")
    url = "http://api.nightlights.io/months/" + start_year + "." + start_month + "-" + end_year + "." + end_month + "/villages/" + india_lights_village_code

    try:
        return requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)


class VillageDataObject:
    state_code = ""
    district_code = ""
    sub_district_code = ""
    constituency = ""
    village_name = ""
    village_code = ""
    india_lights_village_code = ""

    def __init__(self, dump_line):
        global current_state_name, current_district_name, current_sub_district_name
        values = re.split(r"[,\s]\s*", dump_line) # Separating the fields based on ' ' or ','
        stateCode = values[0]
        districtCode = values[1]
        subDistrictCode = values[2]
        villageCode = values[3]
        fieldName = ""
        for i in range(4, len(values)):
            fieldName += values[i] + " "
        fieldName = fieldName.strip()

        if districtCode == "00" and subDistrictCode == "0000" and villageCode == "00000000":
            current_state_name = fieldName
        elif subDistrictCode == "0000" and villageCode == "00000000":
            current_district_name = fieldName
        elif villageCode == "00000000":
            current_sub_district_name = fieldName
        else:
            self.village_name = fieldName

        self.state_code = stateCode
        self.district_code = districtCode
        self.sub_district_code = subDistrictCode
        self.village_code = villageCode
        self.india_lights_village_code = self.state_code + self.district_code + self.sub_district_code + self.village_code


# Processing - Don't touch this
state_meta              = get_meta_data_for_state(state)
state_folder            = state_meta.output_folder_name
state_code              = state_meta.state_code
directory               = folder + state_folder + "/"
output_file_path_name   = state_meta.output_file_path_name # If append_to_file is set to True, append_to_file_name is used.
village_dump_file_path  = state_meta.village_dump_file_path
last_village            = state_meta.last_village

last_village_int = int(last_village[:-2])
start_village_int = int(starting_village_number[:-2])
end_village_int = int(ending_village_number[:-2])
village_diff = end_village_int - start_village_int

temp_download_flag = False

now = datetime.now()
dt_string = now.strftime("-%d.%m.%Y-%H.%M.%S")
output_file_path = directory + (append_to_file_name if append_to_file else output_file_path_name) + (dt_string if not append_to_file else "")
error_file_path = output_file_path + "-error.csv"
output_file_path += ".csv"


###

# MAIN CODE STARTS HERE
# Downloading begins here
Path(directory).mkdir(parents=True, exist_ok=True)
output_file = open(output_file_path, 'a' if append_to_file else 'w')
error_file = open(error_file_path, 'a' if append_to_file else 'w')

current_state_name = ""
current_district_name = ""
current_sub_district_name = ""
with open(village_dump_file_path) as infile:
    if not append_to_file:
        write_line_in_file('ILVillageId','StateName','StateCode','DistrictName','DistrictCode','SubDistrictName','SubDistrictCode','Constituency','VillageName','VillageCode','Year','Month','Count','Min','Max','Mean','Median')

    for line in infile:
        line = line.strip('\n')
        village_data = VillageDataObject(line)

        if not download_all_villages and village_data.village_code == starting_village_number:
            temp_download_flag = True

        if (download_all_villages or temp_download_flag) and village_data.village_name != "":
            village_response = download_data_for_village(village_data.india_lights_village_code, village_data.village_code)
            parse_response(village_response, village_data)

        if not download_all_villages and village_data.village_code == ending_village_number:
            temp_download_flag = False
            break


output_file.close()
error_file.close()


print("\n\n############### DOWNLOAD COMPLETE ##############\n\nData stored in: " + output_file_path + "\n\n")
