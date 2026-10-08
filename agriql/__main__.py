import sys

from agriql import connect


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else ":memory:"
    sql = sys.argv[2] if len(sys.argv) > 2 else "SHOW VERSION;"
    print(connect(target).query(sql).text)


if __name__ == "__main__":
    main()
