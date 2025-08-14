import os
import sys

from src.views import generate_full_report


sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def main():
    custom_date = "2019-11-25 14:30:00"
    print(generate_full_report(custom_date))


if __name__ == "__main__":
    main()
