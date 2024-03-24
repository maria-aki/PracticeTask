import os
import winreg
import sys

#функция поиска файла по стандартным каталогам установки ("Program Files", "Program Files (x86)") на доступных дисках
def search_in_program_files(app_name):
    ans = ''
    disks = ['C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\']
    dirs = ['Program Files', 'Program Files (x86)']
    for disk in disks:
        for dir in dirs:
            path = os.path.join(disk, dir)
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    if app_name.lower() in root.lower():
                        ans += '\n' + root
    return ans

#функция поиска файла по реестру windows
def search_in_registry(app_name):
    ans = ''
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            skey_name = winreg.EnumKey(key, i)
            with winreg.OpenKey(key, skey_name) as skey:
                try:
                    display_name = winreg.QueryValueEx(skey, 'DisplayName')[0]
                    if app_name.lower() in display_name.lower():
                        ans += '\n' + r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" + display_name
                except OSError as e:
                    pass
    return ans

def main():
    app_name = sys.argv[1]
    found = search_in_registry(app_name) + search_in_program_files(app_name)
    count = len(found.split('\n')) - 1

    match count:
        case 0:
            print('No locations found')
        case 1:
            print('Detected 1 location:')
        case _:
            print(f'Detected {count} locations:')

    for f in found:
        print(f, end='')

if __name__ == "__main__":
    main()
    print()
