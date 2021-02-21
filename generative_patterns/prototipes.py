import copy


class PrototypeMixin:
    """
    Класс прототип для создания копии самого себя
    """
    def clone(self):
        """
        Создает копию самого себя
        """
        return copy.deepcopy(self)
