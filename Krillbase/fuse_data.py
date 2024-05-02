
def fuse_data(cmems_path, kbase_path, data_id, y1, y2):
    from get_krillbase_data import FilesKB, DataKB
    from get_cmems_data import FilesCM, DataCM
    from pre_process import Fuse

    # CMEMS files
    files_cm = FilesCM(cmems_path, data_id, y1, y2)

    # Krill_base files
    files_kb = FilesKB(kbase_path)

    # Furnish datasets
    data_cm = DataCM(files_cm)
    data_kb = DataKB(files_kb, year_start=int(y1), year_end=int(y2))

    # Fuse datasets
    data = Fuse(data_cm, data_kb)
    return data
