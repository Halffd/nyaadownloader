import NyaaPy


def find_torrent(uploader: str, anime_name: str, episode: int, quality: int, untrusted_option: bool) -> dict:
    """Find if the torrent is already in the database. If not, download it.
    Args:
        uploader (str): The name of the uploader.
        anime_name (str): The name of the anime.
        episode (int): The episode number.
        quality (str): The quality of the torrent.

    Returns:
        dict: Returns torrent if found, else None.
    """

    # Because anime title usually have their episode number like '0X' when X < 10, we need to add a 0 to the episode number.
    if episode >= 100:
        episode = str(episode)
    elif episode >= 10:
        episode = "0" + str(episode)
    else:
        episode = "00" + str(episode)
    b = '_'
    normal = f"[{uploader}] {anime_name}{b}{episode} [{quality}p]"
    new = f"[{uploader}]_{anime_name}_{episode}_({quality}p)"
    print(new,'\n')
    found_torrents = NyaaPy.Nyaa.search(
        keyword=new,
        category=1,
        subcategory=2,
        filters=0 if untrusted_option else 2,
    ) + NyaaPy.Nyaa.search(
        keyword=new,
        category=1,
        subcategory=2,
        filters=0 if untrusted_option else 2,
    )
    print('\n',found_torrents,'\n')
    try:
        # We take the very closest title to what we are looking for.
        torrent = None
        for t in found_torrents:  # (break if found, so we get the most recent one)
            if (
                t["name"].lower().find(f"{anime_name}{b}{episode}".lower()) != -1
                and t["name"].lower().find("~") == -1
            ):  # we want to avoid ~ because Erai-Raws use it for already packed episodes
                torrent = t
                break

        # Else, we take try to get a close title to the one we are looking for.
        if torrent is None:
            for t in found_torrents:
                if (
                    t["name"].lower().find(f"{anime_name}".lower()) != -1
                    and t["name"].lower().find(f" {episode} ") != -1
                    and t["name"].lower().find("~") == -1
                ):  # we want to avoid ~ because Erai-Raws use it for already packed episodes
                    torrent = t
                    break

    # The only exception possible is that no torrent have been found when NyaaPy.Nyaa.search()
    # (we are doing dict operations on a None object => raise an exception)
    except:
        return {}
    print('\n',torrent)
    return torrent

t = find_torrent(uploader="Some-Stuffs",
                anime_name="Pocket_Monsters_(2019)",
                episode=8,
                quality=1080,
                untrusted_option=1)
print('\n\n',t)