import sys, os
sys.path.append(sys.argv[0] + '/..')  # to include parent packages

from lemys_class import Lemys


def main():
    try:
        _Lemys = Lemys()
        _Lemys.read_csv()

        _Lemys.run()
    except ValueError as e:
        print("Unexpected error:", e)  # sys.exc_info()[0])
        raise


if __name__ == '__main__':
    main()
