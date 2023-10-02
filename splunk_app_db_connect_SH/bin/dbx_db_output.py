from dbx_bootstrap_env import setup_python_path

import sys
import time
import requests
import re

from dbx2.dbx_logger import logger
from dbx2.rest.settings import Settings
from splunklib import modularinput as smi
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class DbxDbOutputRunner:
    SCHEME = """<scheme>
        <title>Scheduled DBX DB Output Job Runner</title>
        <use_external_validation>false</use_external_validation>
        <streaming_mode>xml</streaming_mode>
        <use_single_instance>false</use_single_instance>
    </scheme>
    """

    def __init__(self):
        taskserverPort = Settings.read_taskserver_port()
        self.server_db_output_url = "http://127.0.0.1:" + str(taskserverPort) + "/api/outputs/{}/run"
        self.modinput_name_regex = re.compile('dbx_db_output://([\w.-]+)$')

    def do_scheme(self):
        print(self.SCHEME)

    def init_stream(self):
        sys.stdout.write("<stream>")

    def fini_stream(self):
        sys.stdout.write("</stream>")

    def get_config(self):
        try:
            return smi.InputDefinition.parse(sys.stdin)
        except Exception as e:
            raise Exception(f"Error getting Splunk configuration via STDIN: {str(e)}")

    def stream_events(self):
        start_time = time.time()
        logger.info("action=send_run_output_request")

        try:
            input_definition = self.get_config()
            modinput_name = next(iter(input_definition.inputs.keys()))
            db_output_name = self.modinput_name_regex.search(modinput_name).group(1)
            logger.info(f"Run DB Output name={db_output_name}")

            headers = {
                'content-type': 'application/json',
                'X-DBX-SESSION_KEY': input_definition.metadata['session_key'],
            }

            s = requests.Session()
            retries = Retry(total=5, backoff_factor=1)
            s.mount('http://', HTTPAdapter(max_retries=retries))

            response = s.post(url=self.server_db_output_url.format(db_output_name), headers=headers,
                                     verify=False)

            if response.status_code != 200:
                if response.status_code == 303:
                    logger.info(f"Output was run on other node status={response.status_code} content={response.content}")
                else:
                    logger.warn(f"Run Db Output name={db_output_name} failed, status={response.status_code} content={response.content}")
            else:
                logger.info(f"Run DB Output name={db_output_name} completed, content={response.content}")
        except Exception as e:
            logger.error(f"action=Failed running DB Output name={db_output_name}, exception={e}")
        finally:
            logger.info(f"Run DB Output name={db_output_name} took {time.time() - start_time} s")

    def run(self):
        if len(sys.argv) > 1:
            if sys.argv[1] == "--scheme":
                self.do_scheme()
            else:
                return 1
        else:
            self.stream_events()

        return 0


if __name__ == "__main__":
    exit_code = DbxDbOutputRunner().run()
    sys.exit(exit_code)
