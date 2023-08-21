from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import time

from myidapp.database import crud, database, models, schemas
from myidapp.utils import logger


class UpworkCategoryParser:
    def __init__(self, headless: bool = False) -> None:
        logger.info("UpworkCategoryParser init")
        self.set_driver(headless=headless)

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

    def run(self, db: Optional[Session] = None) -> List[models.UpworkCategory]:
        """Main function of UpworkCategoryParser

        Returns:
            List[models.UpworkCategory]: _description_
        """
        self.flush_all_categories_from_database(db=db)
        if not hasattr(self, "driver"):
            logger.warning("UpworkCategoryParser parse_categories: driver not set")
            self.set_driver()

        logger.info("UpworkCategoryParser parse_categories")
        search_options = self.parse_search_options()
        logger.info(
            f"UpworkCategoryParser parse_categories: "
            f"search_options parsed len:{len(search_options)}"
        )

        categories = []
        for option in search_options:
            category = self.parse_li_option(option)
            time.sleep(1)
            categories.append(category)
            self.insert_category_into_database(category, db=db)

        return categories

    def parse_search_options(self) -> List[WebElement]:
        """Find end return list of available category options on upwork search page

        Returns:
            List[WebElement]: _description_
        """
        self.driver.get("https://www.upwork.com/nx/jobs/search/?sort=recency")

        self.click_search_options()

        logger.info("UpworkCategoryParser parse_search_options: search input clicked")
        options = self.driver.find_elements(By.CSS_SELECTOR, 'li[role="option"]')
        return options

    def parse_li_option(self, option: WebElement) -> Dict[str, str]:
        """Parse li option to get category name and link
        Args:
            option (WebElement): li option
        Returns:
            Tuple[str, str]: category name and link
        """
        # self.click_remove_filters_button()
        self.click_search_options()
        result = {}
        name = option.text.strip()
        result["name"] = name

        try:
            option.click()
        except Exception as e:
            logger.warning(
                f"UpworkCategoryParser parse_li_option: CANNOT CLICK OPTION: {e}"
            )
        option_url = self.get_page_url()

        result["url"] = option_url
        return result

    def get_page_url(self) -> str:
        return self.driver.current_url

    def click_search_options(self) -> None:
        """Click on search input to show available options"""
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, "input[type='search'][class='up-input']"
            ).click()
        except NoSuchElementException:
            logger.warning("UpworkCategoryParser parse_search_options: NO SEARCH INPUT")
            self.driver.quit()
        except Exception as e:
            logger.error(
                f"UpworkCategoryParser parse_search_options: {e}",
            )
            self.driver.quit()

    def click_remove_filters_button(self) -> None:
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, "button.up-btn.up-btn-link.m-0.px-0"
            ).click()
        except Exception as e:
            logger.error(
                f"UpworkCategoryParser click_remove_filters_button: {e}",
            )
            self.driver.quit()

    def insert_category_into_database(
        self, category: Dict[str, str], db: Optional[Session] = None
    ) -> None:
        category_create = schemas.UpworkCategoryCreate(
            name=category.get("name") or "", link=category.get("url") or ""
        )
        crud.insert_upwork_category(
            db=db or database.SessionLocal(), category=category_create
        )
        logger.debug(f"UpworkCategoryParser insert_category_into_database: {category}")

    def flush_all_categories_from_database(self, db: Optional[Session] = None) -> None:
        crud.flush_all_upwork_categories(db=db or database.SessionLocal())


if __name__ == "__main__":
    ucp = UpworkCategoryParser()
    print(ucp.run())
