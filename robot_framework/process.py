"""This module contains the main process of the robot."""

import string
import random
import os

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")

    credential_names = orchestrator_connection.process_arguments.split(",")
    credential_names = [c.strip() for c in credential_names]

    for name in credential_names:
        orchestrator_connection.log_info(f"Changing password for {name}.")

        cred = orchestrator_connection.get_credential(name)

        new_password = create_password()

        change_password(username=cred.username, old_password=cred.password, new_password=new_password)

        orchestrator_connection.update_credential(name, new_username=cred.username, new_password=new_password)

    orchestrator_connection.log_info(f"Changed {len(credential_names)} passwords.")


def create_password() -> str:
    """Create a password containing 6 lowercase letters
    and 2 numbers.

    Returns:
        The new password.
    """
    letters = random.choices(string.ascii_lowercase, k=6)
    digits = random.choices(string.digits, k=2)
    password = letters + digits
    random.shuffle(password)
    return "".join(password)


def change_password(username: str, old_password: str, new_password: str):
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()

    browser.get("https://cap-awswlbs-wm3q2021.kmd.dk/KMDNovaESDH/forside")

    wait = WebDriverWait(browser, 20)
    wait.until(EC.element_to_be_clickable((By.ID, "inputUsername")))

    browser.find_element(By.ID, "inputUsername").send_keys(username)
    browser.find_element(By.ID, "inputPassword").send_keys(old_password)
    browser.find_element(By.ID, "cbChangePassword").click()
    browser.find_element(By.ID, "inputNewPassword").send_keys(new_password)
    browser.find_element(By.ID, "inputNewPasswordConfirm").send_keys(new_password)
    browser.find_element(By.ID, "logonBtn").click()
    return browser


if __name__ == '__main__':
    username = ""
    old_password = ""
    new_password = create_password()
    change_password(username, old_password, new_password)
    print(new_password)

    conn_string = os.getenv("OpenOrchestratorConnString")
    crypto_key = os.getenv("OpenOrchestratorKey")
    oc = OrchestratorConnection("Eflyt Test", conn_string, crypto_key, "KMD Ejendomsbeskatning")
    process(oc)
