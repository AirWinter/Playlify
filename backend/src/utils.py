# https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
def chunks(lst: list, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def stringify(string: str):
    """Method to make a string more beautiful"""
    res = string.replace('-', ' ')
    return res.title()


def to_uri(track_id: str):
    """Method to turn a track id into a spotify uri"""
    return f"spotify:track:{track_id}"
