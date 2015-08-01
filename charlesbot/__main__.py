import logging
import sys
from charlesbot.robot import Robot


def main(args=None):
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s: %(levelname)s [%(name)s:%(lineno)d] %(message)s'
    )
    log = logging.getLogger(__name__)
    log.info("Starting CharlesBOT now!")

    slackbot = Robot()
    slackbot.start()

if __name__ == "__main__":
    main()
