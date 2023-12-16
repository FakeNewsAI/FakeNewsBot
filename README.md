<div align="center">

  # FakeNewsBot
  
  **A Python Telegram bot that helps you with fake news with power of Google Gemini Pro LLM and Google search.**

</div>

## How to use

1. Install Python 3.10 or higher
2. Create a virtual environment with `python -m venv venv` (recommended)
   - Activate the virtual environment with `venv\Scripts\activate.bat` (Windows) or `source venv/bin/activate` (Linux)
3. Install the requirements with `pip install -r requirements.txt`
4. Set the environment variables specified below. We have provided a `.env.example` file for you to fill in. Rename it to `.env` after filling in the values.
5. Run the bot with `python3 main.py`
6. Start using the telegram bot.

### Docker (recommended)

1. Install Docker
2. Set the environment variables specified below. We have provided a `.env.example` file for you to fill in. Rename it to `.env` after filling in the values.
3. Run the image with 
   ```shell
   docker run --env-file .env ghcr.io/fakenewsai/fakenewsbot:latest
   ```
4. Start using the telegram bot.
5. Update the FakeNewsBot image with
   ```shell
   docker pull ghcr.io/fakenewsai/fakenewsbot:latest
   ```

## Environment variables

`.env.example` contains the environment variables that need to be set. Rename it to `.env` after filling in the values.

- `GEMINI_KEY`: The API key for Google Gemini Pro LLM.
- `GOOGLE_SEARCH_KEY`: The API key for Google Search.
- `GOOGLE_CSE_ID`: The CSE ID for Google Search.
- `TELEGRAM_BOT_TOKEN`: The token for the Telegram bot.


## Filter Google search results

In the portal obtaining `GOOGLE_CSE_ID`, you can filter the search by whitelist or blacklist websites. You can also set region.

## How to contribute

1. Fork this repository.
2. Create a new branch with `git checkout -b <branch-name>`
3. Make your changes.
4. Commit your changes with `git commit -m "<commit-message>"`
5. Push your changes with `git push origin <branch-name>`
6. Create a pull request.
7. Wait for the pull request to be reviewed and merged.


## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.

## Tools/Services that made this project possible

- Langchain.
- Google Gemini Pro LLM.
- Google Search.
- Telegram.

## FAQ

### What is this?

This is a Telegram bot that helps you with fake news with power of Google Gemini Pro LLM and Google search.

### How does this work?

This bot uses Google Gemini Pro LLM and Google search to find the truth about a news article.

## Contributors

- [Mohammed Rabil](https://github.com/rabilrbl)
- [Vineeth Shenoy](https://github.com/Vineeth-03-Shenoy)

## Contact

- [Telegram](https://t.me/rabilrbl)

## Support

- [GitHub Sponsors](https://github.com/sponsors/rabilrbl)
