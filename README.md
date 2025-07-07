# Robot CLI 🤖🤖

A Python command-line tool for managing UiPath automation projects and their Git repositories.  
Automate common tasks like repository initialization, deployment to different branches, and publishing to Orchestrator.

## Features

- **robot init**: Initialize a new Git repository for your project.
- **robot deploy**: Commit and push changes to the `orchestor` remote.
    - `--dev`: Deploy and commit to the `dev` branch.
    - `--prod`: Deploy and commit to the `main` branch.
- **robot analyze**: (Planned) Analyze your automation project.
- **robot repair 🤖**: (Planned) Repair your automation project.

## Requirements

- Python 3.7+
- [Git](https://git-scm.com/) installed and available in your PATH
- [UiPath CLI](https://docs.uipath.com/) installed and available in your PATH

## Installation

Clone this repository and install dependencies if any:

```bash
git clone https://github.com/masterivanic/sync-repo-uipath.git
cd robot-cli
```

## Usage

### Initialize a Git Repository

```bash
robot init
```
- Initializes a new Git repository in the current directory.
- Prompts for the remote origin URL.

### Deploy Changes

```bash
robot deploy
```
- Commits and pushes changes to the `dev` branch by default.
- Publishes the project to UiPath Orchestrator.

#### Deploy to Dev Branch

```bash
robot deploy --dev
```

#### Deploy to Main (Prod) Branch

```bash
robot deploy --prod
```

### Analyze Project

```bash
robot analyze
```
- (Coming soon) Analyze your automation project.

### Repair Project

```bash
robot repair
```
- (Coming soon) Repair your automation project.

## Error Handling

- If Git or UiPath CLI is not installed, the tool will raise a descriptive exception.
- If the project is not initialized as a Git repository, relevant commands will prompt you to initialize.

## Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

## Credits

- Inspired by UiPath automation best practices.
- Developed by @masterivanic.

## Notes

- This tool assumes you have a valid `project.json` in your project root.
- For more information on UiPath CLI publishing, see [UiPath Documentation](https://docs.uipath.com/fr/studio/standalone/2023.4/user-guide/about-publishing-automation-projects).

**Happy Automating! 🤖🚀**