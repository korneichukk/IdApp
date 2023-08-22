from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sqlalchemy.orm import Session

from typing import List, Optional

from myidapp.utils import logger
from myidapp.database import models


class UpworkJobParser:
    def __init__(self) -> None:
        logger.info("UpworkJobParser init")
        self.set_driver()
        self.jobs: List[models.UpworkJob] = []

    def set_driver(self, headless: bool = False) -> None:
        """Set driver as new instance attribute
        Args:
            headless (bool, optional): Should driver run in headless
            (without windows) mode. Defaults to False.
        """
        logger.info("UpworkCategoryParser set_driver")
        if hasattr(self, "driver"):
            self.driver.quit()

        options = Options()
        service = Service()

        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(service=service, options=options)

    def read_jobs_from_database(self, db: Optional[Session] = None) -> None:
        ...
