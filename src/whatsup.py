from datetime import date, datetime
import time
import pyautogui as pg
import webbrowser as web
import yaml

import pandas as pd
from pynput.keyboard import Controller

from src.constants import BIBLE_BASE_URL, VERSE


class Whatsup:
    def __init__(self, config_file_path: str):
        with open(config_file_path, "r") as file:
            self.configuration = yaml.load(file, Loader=yaml.Loader)
        self.book_in_url_format = self.configuration["book_in_url_format"]
        self.book = self.configuration["book"]
        self.phone_numbers = self.configuration["phone_numbers"]
        self.start_date = datetime.strptime(
            self.configuration["start_date"], "%Y-%m-%d"
        ).date()
        self.end_date = datetime.strptime(
            self.configuration["end_date"], "%Y-%m-%d"
        ).date()
        self.chapters = range(1, self.configuration["chapters"] + 1)

    def send_messages(self):
        chapter = self._get_today_chapter()
        link = f"{BIBLE_BASE_URL}/{self.book_in_url_format}/{chapter}/{VERSE}"
        message = f"{self.book} {chapter}: {link}"

        # Open the tab and wait for it to load
        web.open(f"https://web.whatsapp.com/")
        time.sleep(10)

        keyboard = Controller()
        mouse_x = self.configuration["mouse_x"]
        mouse_y = self.configuration["mouse_y"]
        for phone_number in self.phone_numbers:
            # Click on Chrome address bar then wait 2 seconds and click again to edit
            pg.click(mouse_x, mouse_y)
            time.sleep(2)
            pg.click(mouse_x, mouse_y)

            # Type in the message, press enter, then wait page to load (8 sec) and click
            # enter again to send the message
            # These times will depend on internet and computer
            keyboard.type(f"/send?phone={phone_number}&text={message}")
            pg.press("enter")
            time.sleep(8)
            pg.press("enter")

            # This last pause is necessary because we are in a loop.
            time.sleep(3)

    def _get_today_chapter(self):
        date_range = self._get_date_range()
        date_index = date_range.index(date.today())
        chapter = self.chapters[date_index]
        return chapter

    def _get_date_range(self):
        date_range = pd.date_range(start=self.start_date, end=self.end_date)
        date_range = [dt.to_pydatetime().date() for dt in date_range.to_list()]
        return date_range
