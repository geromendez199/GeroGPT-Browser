# GeroGPT-Browser

A simple assistant that performs web searches and summarizes webpages using the ChatGPT API.
It provides both a command-line interface and a lightweight graphical browser for chatting with GPT.
HTTP requests are cached for an hour to speed up repeated searches.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_key_here
```

3. Run a search (add `--num` to control results and `--lang` to select the language for summaries):

```bash
python cli.py search "search term" --summarize --lang Spanish --num 10 --bullets
```

This prints search results from DuckDuckGo and optionally summarizes the first
result. Add `--open` to launch the first link in your browser. Use `--bullets`
to format the summary as bullet points and `--sentences` to control its
length. The summary will use the requested language (default is English).

4. Summarize a specific URL (use `--bullets` for bullet points and `--sentences` to limit length):

```bash
python cli.py summarize https://example.com/article --lang French --bullets --sentences 3
```

5. Chat directly with ChatGPT:

```bash
python cli.py chat "Tell me a joke" --lang German
```

### Graphical browser

Launch a minimal GUI with an integrated ChatGPT panel:

```bash
python cli.py gui --dark
```

Use `--incognito` to start the browser in a private profile. A very small
ad blocker is built in to remove common tracking scripts.

### Building a Windows executable

Install PyInstaller and run one of the provided build scripts:

```bash
pip install pyinstaller
# On Windows
./build_exe.bat

# On Linux or macOS
./build_exe.sh
```

The standalone executable will be placed in the `dist` folder as
`GeroGPTBrowser.exe`.

### Building a Windows installer

To provide a simple "next, next, finish" style installation you can create a
Windows installer using [Inno Setup](https://jrsoftware.org/isinfo.php). Install
Inno Setup and then run the included batch script:

```bash
./build_installer.bat
```

This compiles `installer.iss` and produces `GeroGPTBrowserSetup.exe` which will
guide you through installation with a standard wizard.

### Downloading pre-built releases

Pre-packaged installers are automatically generated for each push to the
`main` branch using GitHub Actions. You can download the latest executable and
installer from the **Releases** page without installing any build tools:

1. Visit <https://github.com/your-user/GeroGPT-Browser/releases>
2. Download `GeroGPTBrowserSetup.exe`
3. Run the installer and follow the prompts

This provides a quick way to try the browser without manually running the build
scripts or installing Python dependencies.

