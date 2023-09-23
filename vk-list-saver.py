import tkinter as tk
from tkinter import messagebox, ttk
import vk_api
import re
import os
import pyperclip

def create_config_file():
    with open('config.txt', 'w') as config_file:
        config_file.write("# Подставьте вместо 'вставьте_токен' свой токен пользователя.\n")
        config_file.write("# Получить токен можно используя сайт https://vkhost.github.io/\n")
        config_file.write("ACCESS_TOKEN=вставьте_токен\n")

if os.path.exists('config.txt'):
    with open('config.txt', 'r') as config_file:
        lines = config_file.readlines()
        for line in lines:
            if line.startswith('ACCESS_TOKEN='):
                access_token = line.strip().split('=')[1]
                if '"' in access_token or "'" in access_token:
                    access_token = access_token.replace('"','')
                    access_token = access_token.replace("'",'')
                break
else:
    create_config_file()
    access_token = 'вставьте_токен'

if 'вставьте_токен' in access_token:
    messagebox.showinfo("Токен", "Замените 'вставьте_токен' на свой токен в 'config.txt'\nи перезапустите программу.")
def get_user_info(custom_link):
    vk_session = vk_api.VkApi(token=access_token)
    try:
        vk_session.get_api()
        user_info = vk_session.method('users.get', {'user_ids': custom_link})
        if user_info:
            return user_info[0]
    except vk_api.VkApiError as e:
        error_message = f"VK API Error: {e}"
        if "no access_token passed" in str(e):
            messagebox.showerror("Ошибка", f"Ваш токен отсутсвует в конфиге!\nЧтобы создать конфиг снова - удалите его и перезапустите программу.")
        elif access_token == "вставьте_токен":
            messagebox.showerror("Токен", "Замените 'вставьте_токен' на свой токен в 'config.txt'\nи перезапустите программу.")
        elif "invalid access_token" or 'Anonymous token is invalid' in str(e):
            messagebox.showerror("Ошибка", f"Ваш токен невалиден! Перепроверьте\nили попробуйте создать новый.")
        else:
            messagebox.showerror("Ошибка", f"Произошла ошибка из-за VK! Попробуйте снова позже.")

    return None

def parse_and_save_to_list(custom_link, user_info):
    if user_info:
        user_id = user_info['id']
        full_name = f"{user_info['first_name']} {user_info['last_name']}"
        formatted_line = f"{full_name} - vk.com/{custom_link} (vk.com/id{user_id})\n"

        with open('list.txt', 'a') as list_file:
            list_file.write(formatted_line)
        messagebox.showinfo("Успешно", f"Информация сохранена в list.txt: {formatted_line}")
    else:
        messagebox.showerror("Ошибка", "Похоже такой ссылки не существует.")

def paste_from_clipboard():
    clipboard_text = pyperclip.paste()
    entry.delete(0, tk.END)  # Clear the existing text
    entry.insert(0, clipboard_text)

def retrieve_info():
    custom_link = entry.get()
    custom_link = custom_link.replace('https://','')
    custom_link = custom_link.replace('http://','')
    custom_link_match = re.search(r'vk\.com/(\w+)|(\w+)', custom_link)
    if custom_link_match:
        custom_link = custom_link_match.group(1) or custom_link_match.group(2)
    user_info = get_user_info(custom_link)
    parse_and_save_to_list(custom_link, user_info)

app = tk.Tk()
app.title("Создано vk.com/artdamin")

app.grid_propagate(False)

app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

label = tk.Label(app, text="Введите ссылку или её часть:\n(Например: vk.com/artdamin)")
label.grid(row=0, column=0, columnspan=2, sticky="ew")
label.grid_rowconfigure(0, weight=1)  # Make the label resizable

entry = tk.Entry(app)
entry.grid(row=1, column=0, columnspan=2, sticky="ew")

paste_button = tk.Button(app, text="Вставить", command=paste_from_clipboard)
paste_button.grid(row=2, column=0, columnspan=2, sticky="ew")

retrieve_button = tk.Button(app, text="Записать в список", command=retrieve_info)
retrieve_button.grid(row=3, column=0, columnspan=2, sticky="ew")

exit_button = tk.Button(app, text="Выйти", command=app.quit)
exit_button.grid(row=4, column=0, columnspan=2, sticky="ew")

app.mainloop()
