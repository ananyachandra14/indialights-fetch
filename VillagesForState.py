import requests
from datetime import datetime
from pathlib import Path

folder = "/Users/ananya.chandra/Documents/"


# Util methods
def get_district_code(d_code):
    return str(d_code).zfill(2)


def get_sub_district_code(sd_code):
    return str(sd_code).zfill(4)


def get_village_code(v_code):
    return str(v_code).zfill(6) + "00"


def write_line_in_file(
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
    if response.status_code == 200:
        json = response.json()
        if len(json) == 0:
            write_line_in_file(
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
            print("### No data for village " + village_object.village_code)
        else:
            for month_data in json:
                write_line_in_file(
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
        print("###### Error: " + response.json()['message'] + "\n\n\n\n\n")


def get_progress(village_number):
    current = int(village_number[:-2])
    if download_all_villages:
        return current/last_village_int * 100
    else:
        progress = current - start_village_int
        return progress / village_diff * 100


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
        values = dump_line.split()
        stateCode = values[0]
        districtCode = values[1]
        subDistrictCode = values[2]
        villageCode = values[3]
        fieldName = ""
        for i in range(4, len(values)):
            fieldName += values[i] + " "
        fieldName.strip()

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





# MAIN CODE STARTS HERE

# Parameters to be changed
state                   = "west-bengal" # This is just to create the folder inside the directory where all village data will be stored
state_code              = "19" # uttar-pradesh - 9, bihar - 10, assam - 18, west-bengal - 19, orissa - 21, andhra-pradesh - 28
directory               = folder + state + "/"
output_file_path_name   = "wb_village_data"
village_dump_file_path  = "village_dumps_by_state/wb_villages_dump.csv"
last_village            = "04078200" # For tracking progress. Change this when changing village_dump_file_path.

# Starting and ending months for each village
start_year              = "2008"
end_year                = "2013"
start_month             = "1"
end_month               = "12"

download_all_villages   = False # If set to True, starting_village_number and ending_village_number properties aren't used
starting_village_number = "00000000"
ending_village_number   = "00010000" # Including this
append_to_file = False

### Processing - Don't touch this
last_village_int = int(last_village[:-2])
start_village_int = int(starting_village_number[:-2])
end_village_int = int(ending_village_number[:-2])
village_diff = end_village_int - start_village_int

temp_download_flag = False

now = datetime.now()
dt_string = now.strftime("-%d:%m:%Y-%H.%M.%S")
output_file_path = directory + output_file_path_name + (dt_string + ".csv" if not append_to_file else ".csv")

###

# Downloading begins here
Path(directory).mkdir(parents=True, exist_ok=True)
output_file = open(output_file_path, 'a' if append_to_file else 'w')

current_state_name = ""
current_district_name = ""
current_sub_district_name = ""
with open(village_dump_file_path) as infile:
    if not append_to_file:
        write_line_in_file('StateName','StateCode','DistrictName','DistrictCode','SubDistrictName','SubDistrictCode','Constituency','VillageName','VillageCode','Year','Month','Count','Min','Max','Mean','Median')

    for line in infile:
        line.strip('\n')
        village_data = VillageDataObject(line)

        if not download_all_villages and village_data.village_code == starting_village_number:
            temp_download_flag = True

        if download_all_villages or temp_download_flag:
            village_response = download_data_for_village(village_data.india_lights_village_code, village_data.village_code)
            parse_response(village_response, village_data)

        if not download_all_villages and village_data.village_code == ending_village_number:
            temp_download_flag = False
            break


output_file.close()


print("\n\n############### DOWNLOAD COMPLETE ##############\n\n")



# Unused because no way to tell how to change sub district

# starting_district = 1
# ending_district = 1
# starting_sub_district = 1
# ending_sub_district = 1
# starting_village = 1
# ending_village = 10
#
# starting_village_code = state_code + get_district_code(starting_district) + get_sub_district_code(starting_sub_district) + get_village_code(starting_village)
# ending_villagege_code = state_code + get_district_code(starting_district) + get_sub_district_code(starting_sub_district) + get_village_code(starting_village)

# for district_number in range(starting_district, ending_district + 1):
#     district_code = get_district_code(starting_district)
#     for sub_district_number in range(starting_sub_district, ending_sub_district + 1):
#         sub_district_code = get_sub_district_code(starting_sub_district)
#         for village_number in range(starting_village, ending_village + 1):
#             village_code = get_village_code(village_number)
#             india_lights_village = state_code + district_code + sub_district_code + village_code
#
#             print("Downloading village: " + india_lights_village + "\t Progress: " + str(village_number/ending_village * 100) + "%")
#             file_name = directory + str(india_lights_village)
#             url = "http://api.nightlights.io/months/" + start_year + "." + start_month + "-" + end_year + "." + end_month + "/villages/" + str(india_lights_village)
#             # if village_number == 4:
#             #     url = "http://api.nightlights.io/months/2008.1-2013.121/villages/1801000100000200"
#
#             try:
#                 response = requests.get(url)
#                 status_code = write_to_file(response)
#                 if status_code == 200:
#                     print("Download completed in: " + file_name)
#                 else:
#                     print("###### Error: " + response.json()['message'] + "\n\n\n\n\n")
#             except requests.exceptions.RequestException as e:
#                 print(e)
#                 break