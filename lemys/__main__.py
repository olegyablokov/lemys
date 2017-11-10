from lemys_class import Lemys


def main():
    try:
        _Lemys = Lemys()
        _Lemys.read_csv()

        _Lemys.run()
    except Exception as e:
        print("Unexpected error:", e)  # sys.exc_info()[0])
        raise


if __name__ == '__main__':
    main()
