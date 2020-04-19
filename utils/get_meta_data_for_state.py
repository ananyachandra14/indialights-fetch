from utils.State import State
from state_meta_files.andhra_pradesh_meta import andhra_pradesh_meta
from state_meta_files.assam_meta import assam_meta
from state_meta_files.bihar_meta import bihar_meta
from state_meta_files.orissa_meta import orissa_meta
from state_meta_files.uttar_pradesh_meta import uttar_pradesh_meta
from state_meta_files.west_bengal_meta import west_bengal_meta


def get_meta_data_for_state(state):
    meta_for_state = {
        State.ANDHRA_PRADESH: andhra_pradesh_meta,
        State.ASSAM: assam_meta,
        State.BIHAR: bihar_meta,
        State.ORISSA: orissa_meta,
        State.UTTAR_PRADESH: uttar_pradesh_meta,
        State.WEST_BENGAL: west_bengal_meta,
    }
    return meta_for_state.get(state)