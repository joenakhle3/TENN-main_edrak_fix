import os
import sys
import argparse

from tenn_ai.fabric_ai.input_ai.tenn_monitor import TENN_Monitor

#################################################################################################################

def main():
    # Initialize command-line argument parser
    parser = argparse.ArgumentParser(description='InputAI Monitor a folder and ingest relevant URLs.')
    parser.add_argument('folder', type=str, help='The folder to monitor')

    # Parse command-line arguments
    args = parser.parse_args()

    # Check if the folder exists
    if not os.path.exists(args.folder) or not os.path.isdir(args.folder):
        print("EdrakFS TENN_Monitor - Error: The specified folder does not exist or is not a folder." + args.folder)
        exit(1)

    # Start monitoring the specified folder
    monitor = TENN_Monitor(passed_folder=args.folder, passed_verbose=True)
    monitor.start_monitoring()

if __name__ == "__main__":
    main()