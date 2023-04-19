class Module:
    """
    Abstract class representing a module.
    """

    def __init__(self, name: str, description: str):
        """
        Initializes the Module with a name and description.
        """
        self.name = name
        self.description = description

    def execute(self):
        """
        Executes the module.
        """
        pass