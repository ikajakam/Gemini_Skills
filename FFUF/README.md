# FFUF Skill for Gemini CLI

## Credits & Acknowledgements

This project is based on and inspired by the work of **[`rez0`](https://x.com/rez0__)**

- Original FFUF skill & helper logic  
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
- Note: `skills` are currently **only available** in `preview`

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
<img width="1900" height="941" alt="image" src="https://github.com/user-attachments/assets/c9124b3a-6b3f-46c1-b90b-947187052805" />

#### Type ` /settings ` hit ` enter `
```shell
/settings
```

#### select ` Preview Feature ` and hit ` enter ` to enable 
<img width="1876" height="924" alt="image" src="https://github.com/user-attachments/assets/ea864660-5cab-47d3-a980-82f6acd7d4cb" />

#### After enabling Preview Features press `r` to reload and save changes

#### Again go to ` /settings ` type ` skills ` select ` Agent Skills ` and hit ` enter ` to enable
<img width="1887" height="884" alt="image" src="https://github.com/user-attachments/assets/d07d9f20-b5b1-4f2c-8ec2-1870ca5799be" />

#### After enabling  ` Agent Skills ` press ` r ` to reload and save changes

#### You will see ` skills `
<img width="1903" height="926" alt="image" src="https://github.com/user-attachments/assets/69162274-9579-4192-9231-f206842c318b" />

#### Type ` /skills ` select list to list all skills
<img width="1889" height="947" alt="image" src="https://github.com/user-attachments/assets/787b830e-9596-4fcb-b5fe-f4852bbbd9dd" />
<img width="1894" height="726" alt="image" src="https://github.com/user-attachments/assets/704a8190-e6bd-45f2-92d1-a4843b68772e" />

#### Usage
```shell
fuzz example.com using skills to identify any login pages and files with extensions php and bak
```
#### When you run this prompt

- Gemini CLI reads `SKILL.md` to understand how and when the `ffuf skill` should be used
- `ffuf_helper.py` helps to generate and execute the appropriate ffuf commands
- The resulting command and output are returned directly in the Gemini CLI session 

## Understanding Skills

### Read `SKILL.md` to understand how the agent skill works and how instructions are interpreted.

This will help you:

- Understand how the agent selects and executes ffuf commands
- Craft more precise prompts for your own use cases
- Customize or extend behavior by updating `SKILL.md` to match your workflow
- Modifying `SKILL.md` allows you to tailor the skill to your recon style and testing needs.

happy fuzzing 
