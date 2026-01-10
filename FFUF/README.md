# FFUF Skill for Gemini CLI

## Credits & Acknowledgements

This project is based on and inspired by the work of **[`rez0`](https://x.com/rez0__)**

- Original FFUF skill & helper logic:  
 https://github.com/jthack/ffuf_claude_skill/tree/main/ffuf-skill

  - GitHub : https://github.com/jthack  
  - X (Twitter) : https://x.com/rez0__

#### Installing Gemini CLI
  https://google-gemini.github.io/gemini-cli/

#### Requirements
  - macOS, Linux or Windows
  - Node.js version 20 or higher  
  
#### Install globally with npm
  ```shell
  npm install -g @google/gemini-cli
  ```
  ```shell
  brew install gemini-cli
  ```
#### Preview Release
- Note: `skills` are currently **only available** in the `preview`

```shell
npm install -g @google/gemini-cli@preview
```

#### Run Gemini CLI, then choose Login with Google and follow browser authentication flow when prompted
```shell
gemini
```
#### Download this repo and place its content in `~/.gemini/skills/`
File structure should look like this
```shell
.gemini/
└─ skills/
   └─ ffuf/
      ├─ SKILL.md
      └─ ffuf_helper.py

```
- `ffuf` must be a directory
- `SKILL.md` and `ffuf_helper.py` must live inside the `ffuf/` folder
<img width="1411" height="537" alt="image" src="https://github.com/user-attachments/assets/f446c712-2a1b-4581-bd04-4aa4fb92d26d" />

#### Verify
```shell
ls ~/.gemini/skills/ffuf
```
#### Expected output
```shell
SKILL.md
ffuf_helper.py
```

#### Run Gemini CLI
```shell
gemini
```
<img width="1688" height="775" alt="image" src="https://github.com/user-attachments/assets/0b0d173b-dc6d-4d70-8c16-e57e99e5f434" />
