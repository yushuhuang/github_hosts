import requests
import re
from bs4 import BeautifulSoup
from sys import platform


def main():
    if platform == 'linux' or platform == 'linux2':
        hosts_loc = '/etc/hosts'
    elif platform == 'win32':
        hosts_loc = 'C:\\Windows\\System32\\drivers\\etc\\hosts'

    urls = [
        'github.com',
        'gist.github.com',
        'api.github.com',
        'assets-cdn.github.com',
        'raw.githubusercontent.com',
        'github.githubassets.com'
    ]

    write_urls = [
        'gist.githubusercontent.com',
        'cloud.githubusercontent.com',
        'camo.githubusercontent.com',
        'avatars0.githubusercontent.com',
        'avatars1.githubusercontent.com',
        'avatars2.githubusercontent.com',
        'avatars3.githubusercontent.com',
        'avatars4.githubusercontent.com',
        'avatars5.githubusercontent.com',
        'avatars6.githubusercontent.com',
        'avatars7.githubusercontent.com',
        'avatars8.githubusercontent.com',
        'user-images.githubusercontent.com'
    ]

    def getIP(url):
        BASE_URL = '.ipaddress.com/'
        splitted = url.split('.')
        if len(splitted) == 2:
            URL = 'https://' + url + BASE_URL
        else:
            front = '.'.join(splitted[-2:])
            URL = 'https://' + front + BASE_URL + url

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find(
            'table', class_='panel-item table table-border-row table-v faq')
        rows = table.find('tbody').find_all('tr')
        return [row.find('td').text.strip() for row in rows]

    def check_charset(file_path):
        import chardet
        with open(file_path, "rb") as f:
            data = f.read(4)
            charset = chardet.detect(data)['encoding']
        return charset

    if platform == 'win32':
        charset = check_charset(hosts_loc)
        with open(hosts_loc, 'r', encoding=charset) as f:
            lines = f.readlines()

        with open(hosts_loc, 'w', encoding=charset) as f:
            for line in lines:
                if 'github' not in line.strip('\n'):
                    f.write(line)
    elif platform == 'linux' or platform == 'linux2':
        with open(hosts_loc, 'r') as f:
            lines = f.readlines()

        with open(hosts_loc, 'w') as f:
            for line in lines:
                if 'github' not in line.strip('\n'):
                    f.write(line)

    pattern = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"

    if platform == 'win32':
        hosts = open(hosts_loc, 'a', encoding=charset)
    elif platform == 'linux' or platform == 'linux2':
        hosts = open(hosts_loc, 'a')
    hosts.write('#github Start\n')

    for url in urls:
        for i in getIP(url):
            ips = re.findall(pattern, i)
            if ips:
                hosts.write(ips[0] + '\t' + url + '\n')
                print(ips[0] + '\t' + url)
                if url == 'raw.githubusercontent.com':
                    for write_url in write_urls:
                        hosts.write(ips[0] + '\t' + write_url + '\n')

    hosts.write('#github End\n')
    hosts.close()


if platform == 'win32':
    import ctypes
    import sys

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        main()
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)

else:
    main()
