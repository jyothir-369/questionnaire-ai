# backend/auth.py

import yaml
from pathlib import Path
import streamlit_authenticator as stauth

def get_authenticator():
    # Path to config.yaml (two levels up from this file)
    CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

    # Load config
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # Basic validation
    if "credentials" not in config or "usernames" not in config["credentials"]:
        raise ValueError("Invalid config.yaml: Missing 'credentials.usernames' section")

    # Cookie settings (with defaults)
    cookie_config = config.get("cookie", {})
    cookie_name = cookie_config.get("name", "questionnaire_cookie")
    cookie_key = cookie_config.get("key", "supersecretkey")
    cookie_expiry = cookie_config.get("expiry_days", 30)

    # Create authenticator – passwords can be plain text
    authenticator = stauth.Authenticate(
        config["credentials"],
        cookie_name,
        cookie_key,
        cookie_expiry
    )
    return authenticator