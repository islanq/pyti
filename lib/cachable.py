class Cache:
    def __init__(self, max_size):
        self._max_size = max_size
        self._miss = 0
        self._hit = 0
        self.cache = {}
        self.order = []
        
    @property
    def max(self) -> int:
        return self._max_size
    
    @property
    def miss(self) -> int:
        return self._miss
    
    @property
    def hit(self) -> int:
        return self._hit
    
    @property
    def ratio(self) -> float:
        return self._hit / self._miss
    
    @max.setter
    def max(self, value) -> None:
        self._max_size = value
        if len(self.cache) > value:
        # Remove the oldest elements until the cache is the correct size
            for _ in range(len(self.cache) - value):
                oldest = self.order.pop(0)
                del self.cache[oldest]

    def add(self, key, value) -> None:
        self._miss += 1
        if key in self.cache:
            return
        if len(self.cache) >= self.max:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)

    def get(self, key) -> object:
        obj =  self.cache.get(key)
        if obj is not None:
            self._hit += 1
        return obj

    def clear(self) -> None:
        self.cache = {}
        self.order = []

    def size(self) -> int:
        return len(self.cache)

    def __repr__(self):
        return str(self.cache)

class Cachable:
    _caches = {}

    def __new__(cls, *args, **kwargs):
        cache = cls.cache()
        cache_key = (args, tuple(sorted(kwargs.items())))
        cached_object = cache.get(cache_key)
        # we have a cache hit
        if cached_object is not None:
            return cached_object
        # we have a cache miss
        else:
            obj = super().__new__(cls)
            cache.add(cache_key, obj)
            return obj


    @classmethod
    def cache(cls) -> Cache:
        if cls not in Cachable._caches:
            max_size = 50
            Cachable._caches[cls] = Cache(max_size)
        return Cachable._caches[cls]
    
    
    @classmethod
    def cache_max(cls, size = None):
        cache = cls.cache()
        if size is not None:
            cache.max = size
        else:
            return cache.max

    @classmethod
    def cache_clear(cls, clear_global:bool = False):
        if clear_global:
            Cachable._caches = {}
        else:
            cls.cache().clear()

    @classmethod
    def cache_size(cls):
        return cls.cache().size()

if __name__ == "__main__":
    
    class Person(Cachable):
        def __init__(self, name, age):
            self.name = name
            self.age = age


        def __repr__(self):
            return "Person(name={}, age={})".format(self.name, self.age)
    
    class Person2(Person):
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
    count = 60
    
    for i in range(count):
        Person("John", i) # Cache miss
    Person("John", 2) # Cache hit
    
    assert Person.cache_size() == 50
    Person.cache_clear()
    assert Person.cache_size() == 0
    assert Person.cache_max() == 50
    Person.cache_max(2)
    assert Person.cache_max() == 2