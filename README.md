## This repository is deprecated. Please visit [KuriOS](https://github.com/PersoSirEduard/KuriOS) instead 

# KuriOS Developer Guide

## Directory
KuriOS operates and stores data mostly inside volatile memory. However, to first initialize the system, on boot, it requires three files including `directory.json`, `help.json`, and `permissions.json`.

### directory.json
* This file stores the basic storage structure of files and folders. Every file object has this format:
	
   ```json
   "<file name>": {
	"type": "file",
		"invulnerable": true,
		"cache": "<file in ./cache to access the data>"
   }
   ```
*Note: Instead of `cache`, the `data` property can be used to load a string without looking for a cache file on the storage.*
*  Every folder object has this format:

   ```json
   "<folder name>": {
	"type": "folder",
		"invulnerable": true,
		"files": {
			...
		}
   }
   ```
   For both folder and files, optional arguments include:
   * `locked: Boolean`: If true, it will turn the object into an encrypted vault during OS initialization.
   * `password: String`: Password used to encrypt the vault (if `locked` is true) and defaults to "default".
   * `availability: [Datetime, DateTime]`: Interval of time when the file is available/visible.
   * `permission: String`: Required user permission to access the file. Permissions and roles can be setup in `permissions.json`.


## Commands
* **help**: Provide a list of commands available from the `help.json` file.
* **echo [msg]**: Output some string on the terminal.
* **pwd**: Output the current working directory.
* **ls [-t] [-f]**: List the contents of the current working directory.
* **cd [path]**:  Change the current working directory.
* **cat [file]**: Preview the contents of a file.
* **grab [file]**: Download a file.
* **lock [file or path] [password]**: Lock the contents of a folder or file inside a secure vault.
* **unlock [file or path] [password]**: Unlock a secure vault.
* **su [role] [password]**: Gain superuser privileges.
* **neofetch**: (...)
* **get**: (...)
* **set**: (...)
* **del**: (...)
