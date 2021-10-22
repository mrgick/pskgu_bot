def get_first_arg(args: list) -> str:
    if len(args) == 0:
        elem = None
    else:
        elem = str(args[0])
    return elem
