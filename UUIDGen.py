from typing import Callable


class UUIDGen:

    RND_ID = "B6C0F2BE-4CE9-4E4B-84AC-FE79AD5E3533"
    ID_PATTERN = "FFFFFFFF-FFFF-FFFF-{0}-{1}"
    LENS = tuple(map(len, RND_ID.split('-')))

    def __init__(self, start_index: int = 0, start_shift: int = 0, post_func=lambda x: x):
        """
        :param start_index: Стартовое значение предпоследнего блока (XXXXXXXX-XXXX-XXXX-____-XXXXXXXXXXXX)
        :param start_shift: Стартовое значение последнего блока (XXXXXXXX-XXXX-XXXX-XXXX-____________)
        :param post_func: функция, обрабатывающая готовый UUID перед получением в методе get_id
        """
        self._index: int = start_index
        self._shift: int = start_shift
        self._post_func: Callable[[str], str] = post_func

    def get_id(self, index: int) -> str:
        """
        :param index:
        :return: Возвращает ID для указанного индекса и сохранённого сдвига
        """
        if len(str(index)) > self.LENS[-1]:
            raise Exception("Index is too long")

        if len(str(self._shift)) > self.LENS[-2]:
            raise Exception("Shift is too long")

        shift = self._shift

        hex_shift = hex(shift)[2:].rjust(self.LENS[-2], '0')
        hex_index = hex(index)[2:].rjust(self.LENS[-1], '0')

        clear_res = self.ID_PATTERN.format(hex_shift, hex_index)

        return self._post_func(clear_res)

    def get_current(self) -> str:
        """
        :return:
        Настоящий id
        """
        return self.get_id(self._index)

    def get_next(self) -> str:
        """
        :return:
        Следующий id
        """
        next_id = self.get_current()
        self._index += 1
        return next_id

    def set_shift(self, new_shift: int):
        """
        :param new_shift: Новое значение сдвига
        :return: Выставляет указанный сдвиг и обнуляет индекс
        """
        self._shift = new_shift
        self._index = 0

    def increment_shift(self) -> None:
        """
        Увеличивает сдвиг и обнуляет индекс
        """
        self.set_shift(self._shift + 1)

    @classmethod
    def get_lower_gen(cls, start_index: int = 0, start_shift: int = 0) -> 'UUIDGen':
        return UUIDGen(start_index, start_shift, lambda x: x.lower())
