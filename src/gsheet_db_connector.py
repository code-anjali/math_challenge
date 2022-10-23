import json
import logging
import tempfile
from typing import Dict, List

import streamlit as st
from shillelagh.backends.apsw.db import connect




def fill_secrets_from_streamlit(credentials_empty_fp):
    logging.info(f"Filling secrets from streamlit...")
    credentials_filled_temp_fp = tempfile.NamedTemporaryFile(delete=False, suffix='.json').name
    with open(credentials_filled_temp_fp, 'w') as credentials_filled_temp:
        with open(credentials_empty_fp, 'r') as credentials_empty:
            credentials_empty_entries = json.load(credentials_empty)
            logging.debug(f"before credentials were: {credentials_empty_entries}")
            for key_to_copy in ["private_key", "private_key_id", "client_id"]:
                credentials_empty_entries[key_to_copy] = st.secrets["gcp_service_account"][key_to_copy]
                if not st.secrets["gcp_service_account"][key_to_copy]:
                    return ""
                assert len(credentials_empty_entries[key_to_copy]) > 0, f"toml from streamlit could not be read for: {key_to_copy} --> {st.secrets['gcp_service_account'][key_to_copy]}"
            json.dump(credentials_empty_entries, credentials_filled_temp)
            logging.debug(f"after credentials are  : {credentials_empty_entries}")
            logging.debug(f"saved credentials to   : {credentials_filled_temp}")
    return credentials_filled_temp_fp


def establish_connection(in_localhost=False,
                         credentials_empty_fp="credentials_empty.json",
                         local_secret_fp=".streamlit/googlesheetdb-credentials.json"
                         ):
    if "conn" not in st.session_state or st.session_state.conn.closed:
        service_account_file = local_secret_fp if in_localhost else fill_secrets_from_streamlit(credentials_empty_fp)
        if not service_account_file:
            return
        else:
            with open(service_account_file, 'r') as checkcheck:
                checks = json.load(checkcheck)
                if not in_localhost:
                    assert checks["private_key_id"] == st.secrets["gcp_service_account"]["private_key_id"], f"checks['private_key_id']={checks['private_key_id']} \nand\n st.secrets['gcp_service_account']['private_key_id'] = {st.secrets['gcp_service_account']['private_key_id']}"
                else:
                    assert len(checks["private_key_id"]) > 1

        db_conn= connect(":memory:", adapter_kwargs={
            "gsheetsapi": {"service_account_file": service_account_file}})
        if "conn" in st.session_state:
            st.session_state.conn = db_conn

        logging.info(f"Connection established? {'yes' if not db_conn.closed else 'no'}")
        return db_conn



