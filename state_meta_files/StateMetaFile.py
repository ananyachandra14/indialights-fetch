class StateMetaFile:
    output_folder_name = ""                 # This is just to create the folder inside the directory where all village data will be stored
    state_code = ""                         # Unused. State codes according to 2001 census.
    output_file_path_name = ""              # New file is created with this name. Timestamp gets suffixed to this to avoid rewriting mistakenly.
                                            # If append_to_file is set to True, append_to_file_name parameter in VillagesForState.py is used.
    village_dump_file_path = ""
    last_village = ""                       # For tracking progress when download_all_villages is True.
                                            # When adding a new state_meta, set this to the last village number present in the dump file.

    def __init__(self, output_folder_name, state_code, output_file_path_name, village_dump_file_path, last_village):
        self.output_folder_name = output_folder_name
        self.state_code = state_code
        self.output_file_path_name = output_file_path_name
        self.village_dump_file_path = village_dump_file_path
        self.last_village = last_village
