# Instagram Automation: Follow & Unfollow

[![License](https://img.shields.io/static/v1?label=License&message=MIT&color=blue&style=plastic&logo=appveyor)](https://opensource.org/licenses/MIT)

## Table Of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [GitHub](#github)
- [Contact](#contact)

![GitHub repo size](https://img.shields.io/github/repo-size/brij0/Instagram_unfollowing?style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/brij0/Instagram_unfollowing?style=plastic)

## Description
This project automates Instagram activities such as following, unfollowing, and identifying potential users to connect with based on activity data. It uses `SeleniumBase` for browser automation, processes data with `BeautifulSoup`, and handles JSON and CSV files for efficient data storage and retrieval.

### Features
- **Unfollow Users**: Identifies and unfollows users who don’t follow back.
- **Follow Users**: Sends follow requests to selected Instagram users.
- **CSV Data Storage**: Logs potential connections and interactions for future analysis.
- **Cookie Management**: Reuses session cookies for a seamless user experience.

### Challenges Faced
- Handling diverse JSON structures in Instagram data exports.
- Maintaining realistic delays to avoid triggering anti-bot measures.
- Managing browser automation across varying Instagram post layouts.

## Installation

To set up and run the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/brij0/Instagram_unfollow.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd Instagram_unfollow
    ```

3. **Set up a virtual environment** (optional but recommended):
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows: env\Scripts\activate
    ```

4. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Add Instagram cookies**:
   Save your session cookies in a `cookies.json` file in the project directory.

## Usage

1. **To Unfollow Users**:
   ```bash
   python Instagram_Unfollow.py

## Contributing

Contributions to this project are welcome! Follow these steps:

1. Fork the repository.
2. Create a new feature branch: `git checkout -b feature-branch`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Submit a pull request.

Please ensure that your code follows best practices and is well documented.

## GitHub

You can find the repository and more projects at my GitHub profile:

- brij0's [GitHub Profile](https://github.com/brij0/)

## Contact

Feel free to reach out for any questions, feedback, or collaborations:

- Email: bthakrar@uoguelph.ca

