import configparser
import logging
import os
import re
import subprocess
import urllib.request
import zipfile
from tempfile import NamedTemporaryFile


def get_local_browser_version(local_chorme_path) -> str:
    version = subprocess.getoutput(local_chorme_path + ' --version')
    return re.search(r'[0-9\.]+', version).group()


def get_local_driver_version(chrome_driver_path) -> str:
    if os.path.isfile(chrome_driver_path):
        version = subprocess.getoutput(chrome_driver_path + ' -v')
    else:
        version = '0'

    return re.search(r'[0-9\.]+', version).group()


def get_driver_download_url(target_version_number) -> str:
    # get 86.0.4240
    target_version_number = re.search(r'([0-9]+\.[0-9]+\.[0-9]+)', target_version_number).group(1)

    latest_release_url = "{}/LATEST_RELEASE_{}".format(
        chrome_driver_base_url, target_version_number)

    with urllib.request.urlopen(latest_release_url) as response:
        latest_release_version = response.read().decode()
        download_url = "{}/{}/{}".format(
            chrome_driver_base_url, latest_release_version,
            chrome_driver_mac_zip_name)

    return download_url


def download_driver(url, path_to_extract_driver_zip):
    with urllib.request.urlopen(url) as response, NamedTemporaryFile() as tfile:
        tfile.write(response.read())
        with zipfile.ZipFile(tfile.name) as zf:
            zf.extractall(path_to_extract_driver_zip)
            chrome_driver_path = os.path.join(path_to_extract_driver_zip, "chromedriver")
            subprocess.run(['chmod', 'u+x', chrome_driver_path])
            logging.info("Download driver successfully")


def update_driver(local_chorme_path, path_to_extract_driver_zip):
    '''
    Update the webdriver.

    Parameters:
        local_chorme_path (str): The path of local Chrome application
        path_to_extract_driver_zip (str): The path to extract the downloaded zip
    '''
    version = get_local_browser_version(local_chorme_path)
    version_number = re.search(r'([0-9\.]+)\.[0-9]+', version).group(1)  # get 86.0.4240
    driver_download_url = get_driver_download_url(version_number)
    download_driver(driver_download_url, path_to_extract_driver_zip)


def check_driver(local_chorme_path, path_to_extract_driver_zip, chrome_driver_path):
    '''
    Check if the webdriver supports the current version Chrome. If not, update the webdriver.

    Compare the local chrome version with the local webdriver version.
    If the latter is less than the former, then update the local webdriver.

    Parameters:
        local_chorme_path (str): The path of local Chrome application
        path_to_extract_driver_zip (str): The path to extract the downloaded zip
        chrome_driver_path (str): The path of local chromedriver
    '''
    version_pattern = r'([0-9]+)'
    local_driver_version = re.search(
        version_pattern,
        get_local_driver_version(chrome_driver_path)).group()
    local_browser_version = re.search(
        version_pattern,
        get_local_browser_version(local_chorme_path)).group()
    logging.info('local driver version: %s', local_driver_version)
    logging.info('local browser version: %s', local_browser_version)
    if local_driver_version < local_browser_version:
        update_driver(local_chorme_path, path_to_extract_driver_zip)


# set up chrome_driver_base_url and chrome_driver_mac_zip_name
conf = configparser.ConfigParser()
here = os.path.abspath(os.path.dirname(__file__))
module_path = os.path.join(here, os.pardir)
config_path = os.path.join(module_path, "config.ini")
conf.read(config_path)
chrome_driver_base_url = conf.get("chromedriver", "base_url")
chrome_driver_mac_zip_name = conf.get("chromedriver", "mac_zip_name")

if __name__ == '__main__':
    path_to_extract_driver_zip = os.path.join(
        module_path, conf.get("localinfo", "driver_folder_name"))
    chrome_driver_path = os.path.join(
        path_to_extract_driver_zip, conf.get("localinfo", "chrome_driver_name"))
    check_driver(conf.get("localinfo", "mac_local_chrome_path"),
                 path_to_extract_driver_zip, chrome_driver_path)
