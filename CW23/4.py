class LibraryInterface:
    def perform_operation(self, data):
        pass


class NewLibrary:
    def perform_operation(self, data):
        pass


class Adapter(LibraryInterface):
    def __init__(self, new_library):
        self.new_library = new_library

    def perform_operation(self, data):
        self.new_library.perform_operation(data)


class ClientCode:
    def __init__(self, library):
        self.library = library

    def execute_operation(self, data):
        self.library.perform_operation(data)


new_library = NewLibrary()
adapter = Adapter(new_library)
client_code = ClientCode(adapter)
client_code.execute_operation("Data to process")
