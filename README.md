Installation
------------
```
git clone https://github.com/dennisleexyz/piazzetty
cd piazzetty
pip install -r requirements.txt
```
Usage
-----
```
./piazzetty
```
Bugs
----
- Only one account supported.
- Login can only be changed by manually editing the `config.ini` or deleting it
  and rerunning the program to input new credentials.
- Email and password are saved as plain text in `config.ini`.
- Cookie is saved as plain text.
