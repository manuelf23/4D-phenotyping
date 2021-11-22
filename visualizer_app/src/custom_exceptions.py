from builtins import Exception

class EmptyMultispectralDataError(Exception):
    def __str__(self):
        return f"There is not multispectral pcd data in .pickle format"
