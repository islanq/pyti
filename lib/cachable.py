
class Cachable:
    _cache = {}

    _cache_include_attrs = set()
    _cache_exclude_attrs = set()

    def __new__(cls, *args, **kwargs):
        kwargs_items = tuple(sorted(kwargs.items()))
        cache_key = (cls, args, kwargs_items)
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        else:
            obj = super().__new__(cls)
            cls._cache[cache_key] = obj
            return obj

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if not name.startswith("_"):
            self._update_cache()

    def __getattribute__(self, name):
        if name.startswith("_") or name in ("_update_cache",):
            return super().__getattribute__(name)
        attr = super().__getattribute__(name)
        self._update_cache()
        return attr

    # def _update_cache(self):
    #     public_attrs = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
    #     cache_key = (self.__class__, tuple(public_attrs.items()))
    #     self.__class__._cache[cache_key] = self

    def _update_cache(self):
        # Get all public attributes
        all_attrs = {k: v for k, v in self.__dict__.items()
                     if not k.startswith("_")}

        # Apply inclusion and exclusion criteria
        if self._cache_include_attrs:
            attrs = {k: v for k, v in all_attrs.items(
            ) if k in self._cache_include_attrs}
        else:
            attrs = {k: v for k, v in all_attrs.items(
            ) if k not in self._cache_exclude_attrs}
        cache_key = (self.__class__, tuple(attrs.items()))
        self.__class__._cache[cache_key] = self

    @classmethod
    def clear_cache(cls):
        for key in list(cls._cache.keys()):
            if key[0] == cls:
                del cls._cache[key]

    @staticmethod
    def clear_global():
        Cachable._cache = {}

    @classmethod
    def cache_size(cls):
        return len(cls.cache_keys())

    @classmethod
    def cache_keys(cls):
        return [key for key in cls._cache.keys() if key[0] == cls]

    @staticmethod
    def cached_types():
        return list(set([key[0] for key in Cachable._cache.keys()]))

    @classmethod
    def include_attributes(cls, *attr_names):
        if not isinstance(cls, type):
            raise TypeError(
                "This method can only be called from the class, not from an instance")
        cls._cache_include_attrs.update(attr_names)

    @classmethod
    def exclude_attributes(cls, *attr_names):
        if not isinstance(cls, type):
            raise TypeError(
                "This method can only be called from the class, not from an instance")
        cls._cache_exclude_attrs.update(attr_names)

    @classmethod
    def find_by_type(cls, type):
        return [key for key in cls._cache.keys() if key[0] == type]
