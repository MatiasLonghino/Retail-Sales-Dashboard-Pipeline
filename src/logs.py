import logging
import os

LOG_PATH = "logs/pipeline.log"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def log_info(message, df=None):
    """
    Log informativo.
    Puede recibir texto y opcionalmente un dataframe.
    """

    if df is not None:
        logging.info(
            f"{message} | rows={df.shape[0]} | cols={df.shape[1]} | columns={list(df.columns)}"
        )
    else:
        logging.info(message)


def log_warning(message, df=None):
    """
    Log de advertencia.
    """

    if df is not None:
        logging.warning(
            f"{message} | rows={df.shape[0]} | cols={df.shape[1]} | columns={list(df.columns)}"
        )
    else:
        logging.warning(message)


def log_error(message, df=None):
    """
    Log de error.
    """

    if df is not None:
        logging.error(
            f"{message} | rows={df.shape[0]} | cols={df.shape[1]} | columns={list(df.columns)}"
        )
    else:
        logging.error(message)
        
def log_step(step_name):
    logging.info(f"----- {step_name} -----")