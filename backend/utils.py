def filter_by_genre(genre, songs):
    res = []
    for song in songs:
        if genre in song['genres'] and song['id'] not in res:
            res.append(song['id'])
    return res

def filter_by_language(language, songs):
    res = []
    for song in songs:
        for genre in song['genres']:
            if language in genre and song['id'] not in res:
                res.append(song['id'])
    return res

# import datetime
def filter_by_date(start_date, end_date, songs):
    res = []
    if start_date >= end_date:
        raise ValueError("Start date has to be before end date")

    for song in songs:
        if song['date-created'] >= start_date and song['date-created'] <= end_date:
            res.append(song['id'])
    return res

# https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def stringify(str):
    """Method to make a string more beautiful"""
    res = str.replace('-', ' ')
    return res.title()