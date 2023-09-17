class GenericEnum:
    @classmethod
    def values(cls) -> list[any]:
        values = [value for name, value in cls.__dict__.items()
                  if not name.startswith("_")]
        for i, val in enumerate(values):
            if 'value' in dir(val):
                values[i] = val.value
        return values

    @classmethod
    def names(cls) -> list[str]:
        names = [name for name, _ in cls.__dict__.items()
                 if not name.startswith("_")]
        for i, name in enumerate(names):
            if 'name' in dir(name):
                names[i] = name.name
        return names

    @classmethod
    def items(cls) -> dict[str, any]:
        kvps = {item.name: item.value for key,
                item in cls.__dict__.items() if not key.startswith("_")}
        for k, v in kvps.items():
            if 'value' in dir(v):
                kvps[k] = v.value
        return kvps
