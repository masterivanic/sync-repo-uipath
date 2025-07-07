# UiPath manager versioning cli application

"""
 Allow user to push prod or dev version and publish it
 to stay up-to-date
"""

"""
  command to develop:
     robot deploy (this will commit and pus to orchestor)
     robot deploy dev : deploy and commit on dev branch
     robot deploy prod: deploy and commit on main branch
     robot analyze
     robot repair 🤖 (feature)
"""

import argparse
from command import RobotCommand

def main():
    robot = RobotCommand()
    cli = argparse.ArgumentParser(
        prog="robot", 
        description="Sync git and orchestrator to safe development and production 🤖",
        epilog="Robot command run all uipath",
        add_help=True,
        exit_on_error=True
    )
    subparsers = cli.add_subparsers(dest='command', required=True)
    subparsers.add_parser('init', help='Initialize a git repository')
    subparsers.add_parser('deploy', help='Commit and push to orchestor')

    # cli.add_argument("--dev", type=str, help="push on given develop branch")

    args = cli.parse_args()
    if args.command == "deploy":
        robot.deploy()
    if args.command == "init":
        robot.init_repository()


if __name__ == '__main__':
    main()
