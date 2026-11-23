from abc import ABC, abstractmethod
import math

class Expression(ABC):

    @abstractmethod
    def evaluate(self, x: float) -> float:
        pass

    @abstractmethod
    def derivative(self) -> "Expression":
        pass
        
    def __call__(self, x):
        return self.evaluate(x)
    


class Polynomial(Expression):
    def __init__(self, coefficients):
        if len(coefficients) == 0:
            raise ValueError("Coefficients cannot be empty")
        self.coeff = coefficients[:]
        


    def evaluate(self, x):
        total = 0
        for idx, val in enumerate(self.coeff):
            power = len(self.coeff) - (idx + 1)
            total += (val * (x) ** power)

        return total

        

    def derivative(self):
        derived = []

        for idx, val in enumerate(self.coeff):
            power = len(self.coeff) - (idx + 1)
            derived.append(val * power) 

        if len(derived) > 1 and derived[-1] == 0:
            derived.pop()

        return Polynomial(derived)

    def __repr__(self):
        return f"Polynomial({self.coeff})"

    def __str__(self):
        terms = []
        for idx, val in enumerate(self.coeff):
            power = len(self.coeff) - (idx + 1)
            if val == 0:
                continue
            if power == 0:
                terms.append(f"{val}")
            elif power == 1:
                if val == 1:
                    terms.append(f"x")
                else:
                    terms.append(f"{val}x")
            else: # power > 1
                if val == 1:
                    terms.append(f"x^{power}")
                else:
                    terms.append(f"{val}x^{power}")
        if not terms:
            return "0"
        return " + ".join(terms).replace("+ -", "- ")

    

class Trigonometric(Expression):
    def __init__(self, func, amp=1.0, freq=1.0):
        if func not in ("sin", "cos"):
            raise ValueError("Invalid function name entered")

        self.func = func
        self.amp = amp
        self.freq = freq

    def evaluate(self, x):
        return self.amp * getattr(math, self.func)((self.freq * x))

    def derivative(self):
        if self.func == "sin":
            return Trigonometric("cos", self.amp * self.freq, self.freq)
        elif self.func == "cos":
            return Trigonometric("sin", (-1) * self.amp * self.freq, self.freq)
        else:
            raise ValueError(f"Unsupported function: {self.func}")
        
    def __repr__(self):
        return f"Trigonometric('{self.func}', amp={self.amp}, freq={self.freq})"

    def __str__(self):
        prefix = ""
        arg = ""

        if self.amp == 0:
            return "0"
        elif self.amp == 1.0:
            prefix = ""
        elif self.amp == -1.0:
            prefix = "-"
        else:
            prefix = str(self.amp)

        if self.freq == 0:
            arg = "0"
        elif self.freq == 1.0:
            arg = "x"
        elif self.freq == -1.0:
            arg = "-x"
        else:
            arg = f"{self.freq}x"
        
        return f"{prefix}{self.func}({arg})"

        
    
                    

class Exponential(Expression):
    def __init__(self, amp=1.0, k=1.0):
        self.amp = amp
        self.k = k

    def evaluate(self, x):
        return self.amp * math.exp(self.k * x)

    def derivative(self):
        return Exponential(self.amp * self.k, self.k)

    def __repr__(self):
        return f"Exponential(amp={self.amp}, k={self.k})"

    def __str__(self):

        prefix = ""
        exponent = ""

        if self.amp == 0:
            return "0"
        elif self.amp == 1.0:
            prefix = ""
        elif self.amp == -1.0:
            prefix = "-"
        else:
            prefix = str(self.amp)

        if self.k == 0:
            exponent = "0"
        elif self.k == 1.0:
            exponent = "x"
        elif self.k == -1.0:
            exponent = "-x"
        else:
            exponent = f"{self.k}x"
        
        return f"{prefix}e^{exponent}"
    
    