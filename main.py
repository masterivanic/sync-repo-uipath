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
from pathlib import Path

def main():
    robot = RobotCommand()
    cli = argparse.ArgumentParser(
        prog="robot", 
        description="Sync git and orchestrator to safe development and production 🤖",
        epilog="""
            Examples:
                robot deploy --dev -m "Dev commit"
                robot deploy --prod -m "Prod deploy"
                robot deploy -m "Default to dev"
                robot deploy --path /path/to/your/project -m "Run in another folder"
                robot init
                robot analyze
                robot repair
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        exit_on_error=True
    )
    subparsers = cli.add_subparsers(dest='command', required=True)
    init_parser = subparsers.add_parser('init', help='Initialize a git repository')
    init_parser.add_argument('-p', '--path', type=str, help='Project directory (default: current)', default=None)
   
    deploy_parser = subparsers.add_parser('deploy', help='Commit and push to orchestrator')
    group = deploy_parser.add_mutually_exclusive_group()
    group.add_argument('--dev', action='store_true', help='Deploy and commit on dev environnment')
    group.add_argument('--prod', action='store_true', help='Deploy and commit on prod environnment')
    deploy_parser.add_argument('-m', '--message', type=str, help='Commit message', required=True)
    deploy_parser.add_argument('-p', '--path', type=str, help='Project directory (default: current)', default=None)

    args = cli.parse_args()
    current_directory = Path(args.path) if args.path else Path.cwd()
    if args.command == "deploy":
        target = "dev" if args.dev else "main" if args.prod else "dev"
        commit_message = args.message
        robot = RobotCommand(current_directory=current_directory)
        robot.deploy(target=target, commit_message=commit_message)
    elif args.command == "init":
        robot = RobotCommand(current_directory=current_directory)
        robot.init_repository()


if __name__ == '__main__':
    main()
