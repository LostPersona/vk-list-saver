## vk-list-saver

This project aims to implement a simple Python-based tool to save provided VK (Russian social network) user URLs into the text file.
This repo contains both source code and an .exe file compiled through PyInstaller in the Releases tab.
The GUI was created with Tkinter and uses Russian language.

# Example:

![image](https://github.com/LostPersona/vk-list-saver/assets/37241729/a1f41c6e-8a72-44aa-9eb5-c95067f7ef81)


* Provided URL:

**vk.com/artdamin**

* Result saved into list.txt:
  
**Artem Daminov - vk.com/artdamin (vk.com/id399328194)**

# Important note:

* In order to work, program needs to be provided a user access token which will be used
to access VK Api.

* config.txt file gets created automatically in the same directory the program was executed.

* in the config.txt, instead of ***"вставьте_токен"*** user should put in the access token to use.

* list.txt also gets created in the same directory where the program was executed.

# How to get user access token?

* The following website was used to get the user access token initially:

[https://vkhost.github.io/]
