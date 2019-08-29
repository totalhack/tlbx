from toolbox import Script, arg


@Script([arg("name", help="A name")])
def main(name):
    print("Name:", name)


if __name__ == "__main__":
    main()
