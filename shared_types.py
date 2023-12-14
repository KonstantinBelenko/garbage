class Result[T]:
    
    def __init__(self, result: T, error: Exception):
        self.result = result
        self.error = error

    def is_ok(self) -> bool:
        return self.result is not None
    
    def is_err(self) -> bool:
        return self.error is not None
    
    def unwrap(self) -> T:
        if self.is_ok():
            return self.result
        else:
            raise self.error
    
    def expect(self, message) -> T:
        if self.is_ok():
            return self.result
        else:
            raise Exception(message)

class Ok[T](Result[T]):
    def __init__(self, result: T):
        super().__init__(result, None)

class Err[T](Result[T]):
    def __init__(self, error: Exception):
        super().__init__(None, error)

