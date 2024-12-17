# ------------------------------IMPORTS------------------------------


import NyaaPy
import requests
import webbrowser as wb
import time

# ------------------------------FUNCTIONS------------------------------


def is_in_database(anime_name: str) -> bool:
    """Check if anime exists in Nyaa database
    Args:
        anime_name (str): Name of the anime to check.

    Raises:
        Exception: If the anime is not found in the database, the only possible reason is that user has no Internet connection.

    Returns:
        bool: True if check was successful, False otherwise.
    """
    try:
        if (
            len(
                NyaaPy.Nyaa.search(
                    keyword=anime_name, category=1, subcategory=2, filters=0
                )
            )
            == 0
        ):
            return False
    except:
        raise Exception("No Internet connection available.")
    return True


def download(torrent: dict) -> bool:
    """Download a nyaa.si torrent from the web (also retrives its original name)

    Args:
        torrent (dict): The dictionary returned by the NyaaPy.search() method.

    Returns:
        bool: True if the transfer was successful, False otherwise.
    """
    try:
        with requests.get(torrent["download_url"]) as response, open(
            torrent["name"] + ".torrent", "wb"
        ) as out_file:
            out_file.write(response.content)

    except requests.Timeout:
        return False

    return True


def transfer(torrent: dict) -> bool:
    """Open the user's torrent client and transfers the file to it.
    Args:
        torrent (dict): The dictionary returned by the NyaaPy.search() method.

    Returns:
        bool: True if the transfer was successful, False otherwise.
    """
    try:
        wb.open(torrent["magnet"])

    except:
        return False

    return True


def find_torrent_pkmn(uploader: str, anime_name: str, episode: int, quality: int, untrusted_option: bool) -> dict:
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
def find_torrent_any(
    uploader: str,
    anime_name: str,
    episode: int,
    quality: int,
    untrusted_option: bool,
    search_format: str = "[{uploader}]_{anime_name}_{episode}_({quality}p)",
    delimiter: str = "_",
    episode_padding: int = 2,
) -> dict:
    """Find if the torrent is already in the database. If not, download it.

    Args:
        uploader (str): The name of the uploader.
        anime_name (str): The name of the anime.
        episode (int): The episode number.
        quality (int): The quality of the torrent.
        untrusted_option (bool): Whether to search for untrusted torrents.
        search_format (str, optional): The format of the search string. Defaults to "[{uploader}]_{anime_name}_{episode}_({quality}p)".
        delimiter (str, optional): The delimiter used in the search string. Defaults to "_".
        episode_padding (int, optional): The number of zeros to pad the episode number with. Defaults to 2.

    Returns:
        dict: Returns the torrent if found, else an empty dictionary.
    """

    # Pad the episode number with leading zeros
    episode_str = f"{episode:0{episode_padding}d}"

    # Format the search string
    search_string = search_format.format(
        uploader=uploader,
        anime_name=anime_name,
        episode=episode_str,
        quality=quality,
    )

    # Replace the delimiters with spaces for the search
    search_string = search_string.replace(delimiter, " ")

    # Search for the torrent
    found_torrents = NyaaPy.Nyaa.search(
        keyword=search_string,
        category=1,
        subcategory=2,
        filters=0 if untrusted_option else 2,
    )

    # Find the most relevant torrent
    torrent = None
    for t in found_torrents:
        if (
            t["name"].lower().find(f"{anime_name}{delimiter}{episode_str}".lower()) != -1
            and t["name"].lower().find("~") == -1
        ):  # we want to avoid ~ because Erai-Raws use it for already packed episodes
            torrent = t
            break

    if torrent is None:
        for t in found_torrents:
            if (
                t["name"].lower().find(f"{anime_name}".lower()) != -1
                and t["name"].lower().find(f" {episode_str} ") != -1
                and t["name"].lower().find("~") == -1
            ):  # we want to avoid ~ because Erai-Raws use it for already packed episodes
                torrent = t
                break

    return torrent or {}
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
    if episode >= 10:
        episode = str(episode)
    else:
        episode = "0" + str(episode)

    found_torrents = NyaaPy.Nyaa.search(
        keyword=f"[{uploader}] {anime_name} - {episode} [{quality}p]",
        category=1,
        subcategory=2,
        filters=0 if untrusted_option else 2,
    ) + NyaaPy.Nyaa.search(
        keyword=f"[{uploader}] {anime_name} - {episode} ({quality}p)",
        category=1,
        subcategory=2,
        filters=0 if untrusted_option else 2,
    )
    
    try:
        # We take the very closest title to what we are looking for.
        torrent = None
        for t in found_torrents:  # (break if found, so we get the most recent one)
            if (
                t["name"].lower().find(f"{anime_name} - {episode}".lower()) != -1
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

    return torrent
if __name__ == "__main__":
    # Get user input for quality, anime name, uploader, start episode, and end episode
    quality = int(input("Enter desired video quality (e.g., 1080): "))
    anime_name = input("Enter the anime name: ")
    uploader = input("Enter the uploader name: ")
    start_episode = int(input("Enter the start episode number: "))
    end_episode = int(input("Enter the end episode number: "))

    maximum = 20

    for i in range(start_episode, end_episode + 1):
        success = False
        tries = 0
        while not success and tries < maximum:
            try:
                t = find_torrent(uploader=uploader,
                                anime_name=anime_name,
                                episode=i,
                                quality=quality,
                                untrusted_option=1)
                if t:
                    download(t)
                success = True
            except Exception as e:
                tries += 1
                print(f"Error downloading episode {i}: {e}")
                time.sleep(5)
"""if __name__ == "__main__":
    for i in range(88, 300):
        success = False
        tries = 0
        maximum = 20
        while not success and tries < maximum:
            try:
                t = find_torrent(uploader="Some-Stuffs",
                            anime_name="Pocket_Monsters_(2019)",
                            episode=i,
                            quality=1080,
                            untrusted_option=1)
                if t:
                    download(t)
                success = True
            except Exception as e:
                tries += 1
                print(f"Error downloading episode {i}: {e}")
                time.sleep(5)"""