import argparse
from src.network.peer import P2PAITrainingPeer
from src.utils.config import load_config
from src.utils.logging import setup_logging

def main():
    parser = argparse.ArgumentParser(description="P2P AI Training Network Node")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to the configuration file")
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Setup logging
    logger = setup_logging(config.get("log_level", "INFO"))

    # Initialize and start the P2P node
    peer = P2PAITrainingPeer(config["host"], config["port"])
    try:
        peer.start()
        logger.info(f"P2P AI Training Node started on {config['host']}:{config['port']}")
        peer.join()  # Keep the main thread alive
    except KeyboardInterrupt:
        logger.info("Shutting down P2P AI Training Node...")
        peer.stop()

if __name__ == "__main__":
    main()