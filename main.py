import socket
import argparse
from typing import Dict, NoReturn
from requests_html import HTMLSession
from colorama import Fore


banner: str = """
 _____       _    ______                    ______          
/  ___|     | |   | ___ \                   | ___ \         
\ `--. _   _| |__ | |_/ /___  ___ ___  _ __ | |_/ / __ ___  
 `--. \ | | | '_ \|    // _ \/ __/ _ \| '_ \|  __/ '__/ _ \ 
/\__/ / |_| | |_) | |\ \  __/ (_| (_) | | | | |  | | | (_) |
\____/ \__,_|_.__/\_| \_\___|\___\___/|_| |_\_|  |_|  \___/                                                                                                                                            
                                              by Niko13TeeN \n"""


class GetAddrInfo(object):
    def __init__(self, host: str = None):
        self.host = host
        self.session: object = HTMLSession()

    def __repr__(self) -> str:
        return self.host

    def get_info(self) -> Dict[str, str]:
        try:
            response: object = self.session.get(f"https://{self}")
            title: str = response.html.find("title", first=True)
            information: Dict[str, str] = {
                "[*] Basic information for:": f"https://{self}",
                "[+] Host:": self,
                "[+] Status:": response.status_code,
                "[+] IP:": socket.gethostbyname(self.host),
                "[+] Title:": title.text if title else None,
            }
            return information
        except ConnectionError as error:
            return Fore.RED + f"[?] Host: {self.host} : Connection Error!"
        except Exception as error:
            return Fore.RED + f"[?] Host: {self.host} : Unhandled Exception!"


class FindSubdomains(object):
    def __init__(self, host: str = None):
        self.host = host
        self.session: object = HTMLSession()

    def __repr__(self) -> str:
        return self.host

    def sub_find(self) -> NoReturn:
        try:
            with open("wordlist.txt", "r") as word:
                for payload in map(lambda line: line.rstrip("\n"), word):
                    try:
                        response: object = self.session.get(f"https://{payload}.{self}")
                        if response:
                            ip_addr: str = socket.gethostbyname(
                                f"{payload}.{self.host}"
                            )
                            title: str = response.html.find("title", first=True)
                            print(
                                f"[+] Found: https://{payload}.{self} | {Fore.CYAN}{ip_addr}{Fore.GREEN} | Title: {Fore.WHITE}{title.text if title else None} {Fore.GREEN}| Status: {Fore.CYAN}{response.status_code}{Fore.GREEN}"
                            )
                    except Exception as error:
                        #print(f"{Fore.CYAN}DEBUG: {payload}.{self} - Not Found!") <--- Debug MODE
                        pass
        except FileNotFoundError as error:
            print(Fore.RED + "{FAILED} File: wordlist.txt NOT FOUND!\n")


def main_function(hostname: str = None):
    basic_information: object = GetAddrInfo(hostname)
    finder_fubdomains: object = FindSubdomains(hostname)

    def return_basic_information():
        print(
            f"{Fore.CYAN + banner}\nTelegramChannel: https://t.me/niko13teen_channel\nTelegramAuthor : https://t.me/niko13teen\n "
        )
        try:
            data: Dict[str, str] = basic_information.get_info()
            for title, value in data.items():
                print(Fore.GREEN + f"{title} {value}")
        except AttributeError as error:
            print(
                Fore.RED
                + "[?] Attribute Error: Please check the url is correct and try again!"
            )

    def return_find_subdomains():
        print("\n[ SubReconPRO in processing ... Good Luck! ]: \n")
        return finder_fubdomains.sub_find()

    return return_basic_information(), return_find_subdomains()


if __name__ == "__main__":
    parser: object = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        "-t",
        action="store",
        dest="hostname",
        help="Input hostname, example: site.com",
        default=None,
    )
    args: str = parser.parse_args()
    main_function(args.hostname)
