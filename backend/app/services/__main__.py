import asyncio
import logging
import signal

from app.config import settings
from app.services.collector import DataCollector


def main() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-8s %(name)s  %(message)s",
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    collector = DataCollector()
    loop.run_until_complete(collector.start())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, loop.stop)

    logging.getLogger(__name__).info("Collector running, press Ctrl+C to stop")

    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    main()
