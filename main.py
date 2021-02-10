from menu import Menu


if __name__ == '__main__':
    try:
        menu = Menu()
        menu.execute()
    except KeyboardInterrupt:
        print('\nExiting process...')