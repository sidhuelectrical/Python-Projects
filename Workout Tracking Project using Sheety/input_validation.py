def get_input(prompt, *, cast=str, min_val=None, max_val=None, choices=None):
    # The reason behind using * is that it indicates all other arguments after this are
    # keyword arguments that we have to explicitly use keywords to pass those arguments
    # Also by providing default values to the parameters we can make them optional
    while True:

        try:
            value = cast(input(prompt).strip())

            if min_val is not None and value < min_val:
                raise ValueError(
                    f"The input value is too small,it must be larger than {min_val}")
            if max_val is not None and value > max_val:
                raise ValueError(
                    f"The input value is too large,it must be smaller than {max_val}")
            if choices is not None:
                choices = [c.lower() for c in choices]
                if isinstance(value, str):
                    value = value.lower()
            if choices is not None and value not in choices:
                raise ValueError(
                    f"The input value is not invaild.\n Acceptable choices are {choices}")
            return value
        except ValueError as e:
            print(f"❌ Invalid input :{e} ")
