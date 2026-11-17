
class Calculator:
    """
    Singleton Calculator instance performs basic calculations on numbers.

    Numbers can be given in various forms: as int, float, double or as string
    numbers, e.g. "123" or "1.600" or as Latin numbers "X", as single digit
    words: "three" (English, 3), "cinco" (Spanish, 5), "семь" (Russian, 7),
    "X" (Latin, 10) or "三" (Chinese, sān 3).

    See: https://sgra64.github.io/py-fun.github.io/src.calculator.html.
    """

    _instance = None

    # Number words in supported languages
    NUMBER_WORDS = {
        # English
        "zero": 0, "one": 1, "two": 2, "three": 3,
        "four": 4, "five": 5, "six": 6, "seven": 7,
        "eight": 8, "nine": 9, "ten": 10,
        # German
        "null": 0, "eins": 1, "ein": 1, "zwei": 2,
        "drei": 3, "vier": 4, "fünf": 5, "fuenf": 5,
        "sechs": 6, "sieben": 7, "acht": 8, "neun": 9,

        # Spanish
        "cero": 0, "uno": 1, "una": 1, "dos": 2,
        "tres": 3, "cuatro": 4, "cinco": 5,
        "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,

        # Russian
        "ноль": 0, "один": 1, "одна": 1, "два": 2,
        "две": 2, "три": 3, "четыре": 4, "пять": 5,
        "шесть": 6, "семь": 7, "восемь": 8, "девять": 9,

        # Chinese
        "零": 0, "〇": 0, "一": 1, "二": 2,
        "两": 2, "三": 3, "四": 4, "五": 5,
        "六": 6, "七": 7, "八": 8, "九": 9,
    }

    # Roman numeral values
    ROMAN_VALUES = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    def __new__(cls):
        """Implement the Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    @classmethod
    def _roman_to_int(cls, value):
        """Convert a valid Roman numeral into an integer."""
        import re

        value = value.upper()

        pattern = (
            r"M{0,3}(CM|CD|D?C{0,3})"
            r"(XC|XL|L?X{0,3})"
            r"(IX|IV|V?I{0,3})"
        )

        if not value or not re.fullmatch(pattern, value):
            return None

        total = 0

        for i, char in enumerate(value):
            current = cls.ROMAN_VALUES[char]

            if i + 1 < len(value):
                following = cls.ROMAN_VALUES[value[i + 1]]

                if current < following:
                    total -= current
                else:
                    total += current
            else:
                total += current

        return total

    @classmethod
    def _to_number(cls, value, invalid_as_zero=False):
        """
        Convert supported number representations into numeric values.

        Supports numeric values, numeric strings, number words and
        Roman numerals.
        """

        if value is None:
            return 0

        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            value = value.strip()

            if not value:
                if invalid_as_zero:
                    return 0
                raise ValueError("Empty number.")

            # Numeric strings, including decimal numbers
            try:
                number = float(value)

                if number.is_integer():
                    return int(number)

                return number

            except ValueError:
                pass

            # Number words in supported languages
            word = value.casefold()

            if word in cls.NUMBER_WORDS:
                return cls.NUMBER_WORDS[word]

            # Roman numerals
            roman = cls._roman_to_int(value)

            if roman is not None:
                return roman

        if invalid_as_zero:
            return 0

        raise ValueError(f"Number not understood: {value!r}")

    def add(self, a, b):
        """
        Add two numbers.

        Args:
            a: the base number.
            b: the number to add.

        Returns:
            The sum of both numbers.
        """
        return (
            self._to_number(a, invalid_as_zero=True)
            + self._to_number(b, invalid_as_zero=True)
        )

    def sub(self, a, b):
        """
        Subtract two numbers.

        Args:
            a: the base number.
            b: the number to subtract.

        Returns:
            The subtraction of both numbers.
        """
        return (
            self._to_number(a, invalid_as_zero=True)
            - self._to_number(b, invalid_as_zero=True)
        )

    def mul(self, a, b):
        """
        Multiply two numbers.

        Args:
            a: the base number.
            b: the number to multiply.

        Returns:
            The product of both numbers.
        """
        return (
            self._to_number(a, invalid_as_zero=True)
            * self._to_number(b, invalid_as_zero=True)
        )

    def div(self, a, b):
        """
        Divide two numbers.

        Args:
            a: the base number.
            b: the number to divide.

        Returns:
            The division of both numbers.

        Note:
            Division by zero returns positive infinity, matching
            the existing Calculator test expectation.
        """
        numerator = self._to_number(a, invalid_as_zero=True)
        denominator = self._to_number(b, invalid_as_zero=True)

        if denominator == 0:
            return float("inf")

        return numerator / denominator

    def factorize(self, n):
        """
        Factorize number into prime factors.

        Args:
            n: the number to factorize into prime factors.

        Returns:
            The list of prime factors.

        Raises:
            ValueError: If an input number is invalid, not understood,
                        negative or not an integer.
        """

        n = self._to_number(n)

        if isinstance(n, float):
            if not n.is_integer():
                raise ValueError("Factorization requires an integer.")
            n = int(n)

        if n < 0:
            raise ValueError("Negative argument.")

        factors = []
        divisor = 2

        while divisor * divisor <= n:
            while n % divisor == 0:
                factors.append(divisor)
                n //= divisor

            divisor += 1

        if n > 1:
            factors.append(n)

        return factors
