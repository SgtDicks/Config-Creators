
# vRising Config Editor

## Version 0.5.0 - RCON Integration and Enhancements

### Overview
The vRising Config Editor is a graphical user interface (GUI) tool designed to help you easily configure your vRising server settings. This tool allows you to load, modify, and save `ServerGameSettings.json` and `ServerHostSettings.json` files through an intuitive interface.

### Features
- **User-Friendly GUI**: Built using Tkinter, the editor provides a simple and clean interface for configuring server settings.
- **Load and Save Configuration**: Easily load existing configuration files, make changes, and save them back to the JSON format.
- **Extensive Game Settings**: Supports a wide range of server game settings including game modes, damage modes, inventory stacks modifier, drop table modifier, material yield modifier, and many more.
- **Tooltips for Guidance**: Integrated tooltips provide helpful information for each configuration option.
- **RCON Integration**: Added support for RCON connections to the server, allowing remote command execution.

### How to Use
1. **Launch the Application**: Run the `vRisingConfigEditor.py` script to launch the GUI.
2. **Load Configuration**: Use the File menu to load your `ServerGameSettings.json` or `ServerHostSettings.json` files.
3. **Edit Settings**: Modify the settings as needed using the provided input fields.
4. **Save Configuration**: Save your changes back to the JSON file using the File menu.
5. **RCON Commands**: Use the RCON tab to connect to your server and send remote commands.

### Menu Options
- **File**:
  - **Load Game Settings**: Load an existing `ServerGameSettings.json` file.
  - **Save Game Settings**: Save the current game settings to `ServerGameSettings.json`.
  - **Load Host Settings**: Load an existing `ServerHostSettings.json` file.
  - **Save Host Settings**: Save the current host settings to `ServerHostSettings.json`.

### Requirements
- Python 3.x
- Tkinter library
- `tooltip` library
- `mcrcon` library

### Installation
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/SgtDicks/Config-Creator/vRisingConfigEditor.git
   ```
2. **Install Required Libraries**:
   ```sh
   pip install tkinter tooltip mcrcon
   ```

### Executable
- You can also download the executable version of the vRising Config Editor from the [releases](https://github.com/yourusername/vRisingConfigEditor/releases) page.

### Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

### Contact
For any questions or support, please contact `Sgt.Dicks@gmail.com`.

---

Enjoy configuring your vRising server with ease!
