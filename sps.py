# sum boilerplate code

def main(argv: list[str]) -> int:
    print("hello world!", argv, sep='\n')
    return 0

if __name__=="__main__":
    from sys import argv
    assert type(argv)==list
    exit(main(argv[1:]))
