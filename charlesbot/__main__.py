import logging.config
from charlesbot.util.config import get_config_file_name
from charlesbot.util.config import read_config


def main(args=None):
    parser = read_config(get_config_file_name())
    logging.config.fileConfig(parser.get('main', 'logging_config'))
    log = logging.getLogger(__name__)
    log.info("Starting CharlesBOT now!")

if __name__ == "__main__":
    main()
