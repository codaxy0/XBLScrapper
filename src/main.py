import os
import time
from typing import Any, Dict, List, Set, Union

import requests

from config import Settings
from logger import Logging

RateLimited = "rate_limited"


class XBLScrapper:
    def __init__(self) -> None:
        self.logger = Logging()
        self.xbl_api_key = Settings.OPENXBL_API_KEY
        self.api_base_url = "https://xbl.io/api/v2"

    @staticmethod
    def __save_gamertags_to_file(gamertags: List[str]) -> None:
        if not os.path.exists("output/"):
            os.makedirs("output/")

        with open("output/gamertags.txt", "a") as f:
            f.write("\n".join(gamertags) + "\n")

    def __get_friends_gamertag(self, data: Dict[str, Any]) -> List[str]:
        return [friend.get("gamertag") for friend in data.get("people", [])]

    def convert_gamertag_to_xuid(self, gamertag: str) -> Union[str, None]:
        url = self.api_base_url + f"/search/{gamertag}"
        headers = {
            "X-Authorization": self.xbl_api_key,
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return str(data["people"][0]["xuid"])
        except requests.exceptions.RequestException as e:
            if e.response is not None:
                if (
                    e.response.status_code == 400
                ):  # this goofy ahh api returns 400 for rate limit
                    return RateLimited

                if e.response.status_code == 403:
                    return None

            self.logger.error(f"Error retrieving XUID for {gamertag}: {e}")
            return None

    def get_user_friends(self, gamertag: str) -> Union[List[str], str, None]:
        xuid = self.convert_gamertag_to_xuid(gamertag)

        if xuid == RateLimited:
            return RateLimited
        if not xuid:
            return None

        url = self.api_base_url + f"/friends/{xuid}"
        headers = {
            "X-Authorization": self.xbl_api_key,
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return self.__get_friends_gamertag(data)
        except requests.exceptions.RequestException as e:
            if e.response is not None:
                if e.response.status_code == 429:
                    return RateLimited
                if e.response.status_code == 403:
                    return None

            self.logger.error(f"Error retrieving friends for {gamertag}: {e}")
            return None

    def start(self) -> None:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        self.logger.print_banner()
        initial_gamertag = input("Enter initial gamertag: ")
        queue = [initial_gamertag]
        processed_gamertags: Set[str] = set()

        while queue:
            current_gamertag = queue.pop(0)

            if current_gamertag in processed_gamertags:
                continue

            friends = self.get_user_friends(current_gamertag)

            if friends == RateLimited:
                self.logger.error("Rate limit exceeded! Try again in 1 hour.")
                break

            if friends is None:
                self.logger.warning(
                    f"Failed to retrieve friends for {current_gamertag}. Retrying..."
                )
                continue

            processed_gamertags.add(current_gamertag)
            self.logger.info(
                f"{current_gamertag} -> {len(friends)} friends found"
            )

            XBLScrapper.__save_gamertags_to_file(friends)  # type: ignore
            queue.extend(friends)
            time.sleep(10)


if __name__ == "__main__":
    XBLScrapper().start()
