import configparser
import os
import shutil
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# custom modules
from webdriver_update_tool import update_chromedriver4mac as ucd4mac


class TestUpdateChromedriver4mac(unittest.TestCase):
    def setUp(self):
        self._driver_version_number = "73.0.3683.68"
        self._conf = configparser.ConfigParser()
        here = os.path.abspath(os.path.dirname(__file__))
        module_path = os.path.join(here, os.pardir)
        config_path = os.path.join(module_path, "config.ini")
        self._conf.read(config_path)
        self._local_chrome_path = self._conf.get("localinfo", "mac_local_chrome_path")
        self._path_to_extract_driver_zip = os.path.join(
            here, self._conf.get("localinfo", "driver_folder_name"))
        self._chrome_driver_path = os.path.join(
            self._path_to_extract_driver_zip, "chromedriver")
        self._chrome_driver_base_url = self._conf.get("chromedriver", "base_url")
        self._chrome_driver_mac_zip_name = self._conf.get("chromedriver", "mac_zip_name")
        pass

    def tearDown(self):
        shutil.rmtree(self._path_to_extract_driver_zip, ignore_errors=True)
        pass

    def test_get_driver_download_url(self):
        driver_version_number = self._driver_version_number
        driver_download_url = ucd4mac.get_driver_download_url(driver_version_number)
        expected_driver_download_url = "{}/{}/{}".format(
            self._chrome_driver_base_url, driver_version_number,
            self._chrome_driver_mac_zip_name)

        self.assertEqual(driver_download_url, expected_driver_download_url)

    def test_update_driver(self):
        driver_version_number = self._driver_version_number
        driver_download_url = ucd4mac.get_driver_download_url(driver_version_number)
        ucd4mac.download_driver(driver_download_url, self._path_to_extract_driver_zip)
        ucd4mac.update_driver(self._local_chrome_path, self._path_to_extract_driver_zip)
        raised = False
        try:
            options = Options()
            options.add_argument("headless")
            webdriver.Chrome(self._chrome_driver_path, options=options)
        except Exception:
            raised = True

        self.assertEqual(raised, False)


if __name__ == "__main__":
    unittest.main()
