import math
from decimal import Decimal
from enum import Enum

def prime_factors(n):
    factors = {}
    for i in range(2, int(math.sqrt(n)) + 1):
        count = 0
        while n % i == 0:
            count += 1
            n //= i
        if count > 0:
            factors[i] = count
    if n > 1:
        factors[n] = 1
    return factors


def prime_factors_n_power(num, n=2.0):
    factors = prime_factors(num)
    results = []
    for key in factors.keys():
        curr_power = factors[key]
        if curr_power == n:
            results.append(key)
    return results


class Operations(Enum):
    Add = 0
    Minus = 1
    Divide = 2
    Multiply = 3
    Power = 4


up_notes:str = '⁰¹²³⁴⁵⁶⁷⁸⁹'
oper_symbols = {Operations.Add:'+', Operations.Minus:'-', Operations.Divide:'/', Operations.Multiply:'*', Operations.Power:'^'}


def check_type(obj:tuple[tuple]|list[list]|list[tuple]|tuple[list]):
    """
    Check the type of the object.
    :param obj: format: [ (para, expected type(s) ), (~, ~), ...]
    :return: None
    """
    for i in obj:
        if not isinstance(i[0], i[1]):
            raise TypeError('expected type ' + str(i[1]) + ' but got ' + str(type(i[0])) + 'instead.')
        else:
            pass
    return None



class Root:
    def __init__(self, num:float=1, n:int=2, coefficient:float=1.0):
        factors = prime_factors_n_power(num, n)
        self.num, self.n = num, n
        self.coefficient = coefficient
        if len(factors) != 0:
            for curr in factors:
                self.num /= (curr**n)
                self.coefficient += curr



    def evalf(self):
        return self.coefficient*math.pow(self.num, 1/self.n)

    def __add__(self, other):
        if isinstance(other, Root):
            if other.n == self.n and other.num == self.num:
                return Root(self.num, self.n, self.coefficient+other.coefficient)
            else:
                raise TypeError("Unmatched Roots:"+str(self.num)+','+str(self.n)+' and '+str(other.num)+','+str(other.n))
        else:
            return Root(self.num + math.pow(other, self.n), self.n, self.coefficient+1)

    def __sub__(self, other):
        if isinstance(other, Root):
            if other.n == self.n and other.num == self.num:
                return Root(self.num, self.n, self.coefficient-other.coefficient)
            else:
                raise TypeError("Unmatched Roots:"+str(self.num)+','+str(self.n)+' and '+str(other.num)+','+str(other.n))
        else:
            return Root(self.num - math.pow(other, self.n), self.n, self.coefficient+1)

    def __eq__(self, other):
        if isinstance(other, Root):
            return (self.num == other.num) and (self.n == other.n) and (self.coefficient == other.coefficient)

    def __pow__(self, power:int|float):
        if power == self.n:
            self.num *= (self.coefficient**self.n)
            #(2√3)^2 = 4 * 3 = 12
            self.n = 1
        else:
            self.coefficient **= power
            self.n *= (1/power)

    def __mul__(self, other):
        if isinstance(other, Root):
            if other.n == self.n:
                return Root(self.num*other.num, self.n, self.coefficient*other.coefficient)
            else:
                raise TypeError("Unmatched Roots:"+str(self.n)+' and '+str(other.n))
        else:
            return Root(self.num, self.n, self.coefficient*other)

    def __truediv__(self, other):
        if isinstance(other, Root):
            if other.n == self.n:
                return Root(self.num/other.num, self.n, self.coefficient/other.coefficient)
            else:
                raise TypeError("Unmatched Roots:"+str(self.n)+' and '+str(other.n))
        else:
            return Root(self.num, self.n, self.coefficient/other)

    def __floordiv__(self, other):
        if isinstance(other, Root):
            if other.n == self.n:
                return Root(self.num/other.num, self.n, self.coefficient/other.coefficient)
            else:
                raise TypeError("Unmatched Roots:"+str(self.n)+' and '+str(other.n))
        else:
            return Root(self.num, self.n, self.coefficient/other)

    def __lt__(self, other):
        if isinstance(other, Root):
            return self.evalf() < other.evalf()
        else:
            return self.evalf() < other

    def __gt__(self, other):
        if isinstance(other, Root):
            return self.evalf() > other.evalf()
        else:
            return self.evalf() > other

    def __le__(self, other):
        if isinstance(other, Root):
            return self.evalf() <= other.evalf()
        else:
            return self.evalf() <= other

    def __ge__(self, other):
        if isinstance(other, Root):
            return self.evalf() >= other.evalf()
        else:
            return self.evalf() >= other

    def __str__(self):
        if self.n >= 2:
            n_str = str(self.n)
            answer_str = str(self.coefficient) + '*'
            total_up_notes = ''
            for i in n_str:
                total_up_notes += up_notes[int(i)]
            answer_str += total_up_notes
            answer_str += '√'; answer_str += str(self.num)
            return answer_str
        elif self.n == 1:
            return str(self.coefficient) + '*' + str(self.num)
        else:
            return str(self.coefficient) + '*' + str(self.num) + '*(1/' + str(self.n) + ')'


class Fraction:
    def __init__(self, numerator, denominator):
        if type(numerator) == int and type(denominator) == int:
            gcd = math.gcd(numerator, denominator)
            self.numerator = numerator // gcd
            self.denominator = denominator // gcd
            self.value = numerator / denominator
        elif type(numerator) == Decimal and type(denominator) == Decimal:
            m = max(len(str(numerator).split(".")[1]), len(str(denominator).split('.')[1]))
            numerator *= 10 ** m
            denominator *= 10 ** m
            numerator = int(numerator)
            denominator = int(denominator)
            gcd = math.gcd(numerator, denominator)
            self.numerator = numerator // gcd
            self.denominator = denominator // gcd
            self.value = numerator / denominator
        elif type(numerator) == Decimal and type(denominator) == int:
            m = len(str(numerator).split(".")[1])
            numerator *= 10 ** m
            denominator *= 10 ** m
            numerator = int(numerator)
            gcd = math.gcd(numerator, denominator)
            self.numerator = numerator // gcd
            self.denominator = denominator // gcd
            self.value = numerator / denominator
        elif type(numerator) == int and type(denominator) == Decimal:
            m = len(str(denominator).split(".")[1])
            numerator *= 10 ** m
            denominator *= 10 ** m
            denominator = int(denominator)
            gcd = math.gcd(numerator, denominator)
            self.numerator = numerator // gcd
            self.denominator = denominator // gcd
            self.value = numerator / denominator
        else:
            raise TypeError('unsupported types ' + str(type(numerator)) + ' and ' + str(type(denominator)))

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)

    def __add__(self, other):
        if type(other) != int and type(other) != float and type(other) != Fraction:
            raise TypeError('unsupported types to add with ' + str(type(other)))
        elif type(other) == Fraction:
            newDenominator = math.lcm(self.denominator, other.denominator)
            mul = newDenominator // self.denominator
            add_numerator = self.numerator * mul
            other_mul = newDenominator // other.denominator
            other_add_numerator = other.numerator * other_mul
            newNumerator = add_numerator + other_add_numerator
            result = Fraction(newNumerator, newDenominator)
            return result
        elif type(other) == int or type(other) == float or type(other) == Decimal:
            new_other = Fraction(other, 1)
            newDenominator = math.lcm(self.denominator, new_other.denominator)
            mul = newDenominator // self.denominator
            add_numerator = self.numerator * mul
            other_mul = newDenominator // new_other.denominator
            other_add_numerator = new_other.numerator * other_mul
            newNumerator = add_numerator + other_add_numerator
            result = Fraction(newNumerator, newDenominator)
            return result
        else:
            raise TypeError('unsupported type' + str(type(other)))

    def __eq__(self, other):
        if type(other) == Fraction:
            if self.numerator == other.numerator and self.denominator == other.denominator:
                return True
            else:
                return False
        elif type(other) == int or type(other) == float:
            if self.value == other:
                return True
            else:
                return False
        else:
            raise TypeError("unsupported type" + str(type(other)))

    def __sub__(self, other):
        if type(other) != int and type(other) != float and type(other) != Fraction and type(other) != Decimal:
            raise TypeError('unsupported types to add with ' + str(type(other)))
        elif type(other) == Fraction:
            newDenominator = math.lcm(self.denominator, other.denominator)
            mul = newDenominator // self.denominator
            add_numerator = self.numerator * mul
            other_mul = newDenominator // other.denominator
            other_add_numerator = other.numerator * other_mul
            newNumerator = add_numerator - other_add_numerator
            result = Fraction(newNumerator, newDenominator)
            return result
        elif type(other) == int or type(other) == float or type(other) == Decimal:
            new_other = Fraction(other, 1)
            newDenominator = math.lcm(self.denominator, new_other.denominator)
            mul = newDenominator // self.denominator
            add_numerator = self.numerator * mul
            other_mul = newDenominator // new_other.denominator
            other_add_numerator = new_other.numerator * other_mul
            newNumerator = add_numerator - other_add_numerator
            result = Fraction(newNumerator, newDenominator)
            return result
        else:
            raise TypeError('unsupported type' + str(type(other)))

    def __mul__(self, other):
        if type(other) == Fraction:
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
        elif type(other) == int or type(other) == float or type(other) == Decimal:
            new_other = Fraction(other, 1)
            return Fraction(self.numerator * new_other.numerator, self.denominator * new_other.denominator)
        else:
            raise TypeError('unsupported type' + str(type(other)))

    def __truediv__(self, other):
        if type(other) == Fraction:
            return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)
        elif type(other) == int or type(other) == float:
            new_other = Fraction(other, 1)
            return Fraction(self.numerator * new_other.denominator, self.denominator * new_other.numerator)
        else:
            raise TypeError('unsupported type' + str(type(other)))

    def __floordiv__(self, other):
        if type(other) == Fraction:
            return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)
        elif type(other) == int or type(other) == float:
            new_other = Fraction(other, 1)
            return Fraction(self.numerator * new_other.denominator, self.denominator * new_other.numerator)
        else:
            raise TypeError('unsupported type' + str(type(other)))

    def __abs__(self):
        return Fraction(abs(self.numerator), abs(self.denominator))

    def __ne__(self, other):
        if not self == other:
            return True
        else:
            return False

    def __lt__(self, other):
        if type(other) == Fraction:
            if self.value < other.value:
                return True
            else:
                return False
        elif type(other) == int or type(other) == float:
            if self.value < other:
                return True
            else:
                return False
        else:
            raise TypeError('unsupported type' + str(type(other)))

    def __gt__(self, other):
        if not self < other and self == other:
            return True
        else:
            return False

    def __le__(self, other):
        if self < other or self == other:
            return True
        else:
            return False

    def __ge__(self, other):
        if self > other or self == other:
            return True
        else:
            return False

    def evalf(self):
        return self.value


def check_roots(obj1:Root, obj2:Root, oper:Operations):
    check_type(((obj1, Root), (obj2, Root)))
    if oper in [Operations.Add, Operations.Minus]:
        return obj1.n == obj2.n and obj1.num == obj2.num
    else:
        return obj1.n == obj2.n


class CompoundExpression:

    def __init__(self, obj1:Decimal|float|int|Root|Fraction=None, obj2:Decimal|float|int|Root|Fraction=None, oper:Operations=Operations.Add):
        self.obj1, self.obj2 = obj1, obj2
        self.oper = oper

    def __str__(self):
        if self.obj2 is None:
            if self.obj1 is None:return ''
            else:return str(self.obj1)
        else:
            answer_str = ''
            if isinstance(self.obj1, (float, Decimal, int)):
                answer_str += str(self.obj1)
            else:
                answer_str += ('('+str(self.obj1)+')')

            answer_str += oper_symbols[self.oper]

            if isinstance(self.obj2, (float, Decimal, int)):
                answer_str += str(self.obj2)
            else:
                answer_str += ('('+str(self.obj2)+')')
            return answer_str

    def __add__(self, other):
        if self.obj2 is None:
            if self.obj1 is None:self.obj1 = other
            else:
                if ( (isinstance(self.obj1, (float, Decimal, int)) and isinstance(other, (float, Decimal, int))) or
                        (isinstance(self.obj1, Fraction) and isinstance(other, (Fraction, Decimal, int))) or
                        (isinstance(self.obj1, Root) and isinstance(other, Root)) ):
                    if isinstance(other, Root) and isinstance(self.obj1, Root):
                        if check_roots(self.obj1, other, Operations.Add):
                            self.obj1 += other
                        else:
                            self.obj2 = other
                            self.oper = Operations.Add
                    else:
                        self.obj1 += other
                else:
                    self.obj2 = other
                    self.oper = Operations.Add
        else:
            temp = CompoundExpression(self.obj1, self.obj2, self.oper)
            self.obj1 = temp
            self.obj2 = other
            self.oper = Operations.Add



    def __sub__(self, other):
        if self.obj2 is None:
            if self.obj1 is None:
                self.obj1 = other
            else:
                if ((isinstance(self.obj1, (float, Decimal, int)) and isinstance(other, (float, Decimal, int))) or
                        (isinstance(self.obj1, Fraction) and isinstance(other, (Fraction, Decimal, int))) or
                        (isinstance(self.obj1, Root) and isinstance(other, Root))):
                    if isinstance(other, Root) and isinstance(self.obj1, Root):
                        if check_roots(self.obj1, other, Operations.Minus):
                            self.obj1 -= other
                        else:
                            self.obj2 = other
                            self.oper = Operations.Minus
                    else:
                        self.obj1 -= other
                else:
                    self.obj2 = other
                    self.oper = Operations.Minus
        else:
            temp = CompoundExpression(self.obj1, self.obj2, self.oper)
            self.obj1 = temp
            self.obj2 = other
            self.oper = Operations.Minus

    def __eq__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self.evalf() == other
        else:
            return self.evalf() == other.evalf()

    def __pow__(self, power:int|float):
        if self.obj2 is None:
            if self.obj1 is not None:
                if isinstance(self.obj1, (float, Decimal, int)):
                    self.obj1 **= power
                else:
                    self.obj2 = power
                    self.oper = Operations.Power
        else:
            temp = CompoundExpression(self.obj1, self.obj2, self.oper)
            self.obj1 = temp
            self.obj2 = power
            self.oper = Operations.Power

    def __mul__(self, other: Root|float|int|Decimal):
        if self.obj2 is None:
            if self.obj1 is None:
                self.obj1 = other
            else:
                if ((isinstance(self.obj1, (float, Decimal, int)) and isinstance(other, (float, Decimal, int))) or
                        (isinstance(self.obj1, Fraction) and isinstance(other, (Fraction, Decimal, int))) or
                        (isinstance(self.obj1, Root) and isinstance(other, Root))):
                    if isinstance(other, Root) and isinstance(self.obj1, Root):
                        if check_roots(self.obj1, other, Operations.Multiply):
                            self.obj1 *= other
                        else:
                            self.obj2 = other
                            self.oper = Operations.Multiply
                    else:
                        self.obj1 *= other
                else:
                    self.obj2 = other
                    self.oper = Operations.Multiply
        else:
            temp = CompoundExpression(self.obj1, self.obj2, self.oper)
            self.obj1 = temp
            self.obj2 = other
            self.oper = Operations.Divide

    def __truediv__(self, other: Root|float|int|Decimal):
        if self.obj2 is None:
            if self.obj1 is None:
                self.obj1 = other
            else:
                if ((isinstance(self.obj1, (float, Decimal, int)) and isinstance(other, (float, Decimal, int))) or
                        (isinstance(self.obj1, Fraction) and isinstance(other, (Fraction, Decimal, int))) or
                        (isinstance(self.obj1, Root) and isinstance(other, Root))):
                    if isinstance(other, Root) and isinstance(self.obj1, Root):
                        if check_roots(self.obj1, other, Operations.Divide):
                            self.obj1 /= other
                        else:
                            self.obj2 = other
                            self.oper = Operations.Divide
                    else:
                        self.obj1 /= other
                else:
                    self.obj2 = other
                    self.oper = Operations.Divide
        else:
            temp = CompoundExpression(self.obj1, self.obj2, self.oper)
            self.obj1 = temp
            self.obj2 = other
            self.oper = Operations.Divide

    def __floordiv__(self, other: Root|float|int|Decimal):
        if self.obj2 is None:
            if self.obj1 is None:
                self.obj1 = other
            else:
                if ((isinstance(self.obj1, (float, Decimal, int)) and isinstance(other, (float, Decimal, int))) or
                        (isinstance(self.obj1, Fraction) and isinstance(other, (Fraction, Decimal, int))) or
                        (isinstance(self.obj1, Root) and isinstance(other, Root))):
                    if isinstance(other, Root) and isinstance(self.obj1, Root):
                        if check_roots(self.obj1, other, Operations.Divide):
                            self.obj1 /= other
                        else:
                            self.obj2 = other
                            self.oper = Operations.Divide
                    else:
                        self.obj1 /= other
                else:
                    self.obj2 = other
                    self.oper = Operations.Divide
        else:
            temp = CompoundExpression(self.obj1, self.obj2, self.oper)
            self.obj1 = temp
            self.obj2 = other
            self.oper = Operations.Divide

    def __lt__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self.evalf() < other
        else:
            return self.evalf() < other.evalf()

    def __gt__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self.evalf() > other
        else:
            return self.evalf() > other.evalf()

    def __le__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self.evalf() <= other
        else:
            return self.evalf() <= other.evalf()

    def __ge__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self.evalf() >= other
        else:
            return self.evalf() >= other.evalf()

    def evalf(self):
        if self.obj2 is None:
            if self.obj1 is None:return 0.0
            else:
                if isinstance(self.obj1, (float, Decimal, int)):
                    return self.obj1
                else:
                    return self.obj1.evalf()
        else:
            if self.oper == Operations.Add:
                op1 = self.obj1 if isinstance(self.obj1, (float, Decimal, int)) else self.obj1.evalf()
                op2 = self.obj2 if isinstance(self.obj2, (float, Decimal, int)) else self.obj2.evalf()
                return op1 + op2
            elif self.oper == Operations.Minus:
                op1 = self.obj1 if isinstance(self.obj1, (float, Decimal, int)) else self.obj1.evalf()
                op2 = self.obj2 if isinstance(self.obj2, (float, Decimal, int)) else self.obj2.evalf()
                return op1 - op2
            elif self.oper == Operations.Divide:
                op1 = self.obj1 if isinstance(self.obj1, (float, Decimal, int)) else self.obj1.evalf()
                op2 = self.obj2 if isinstance(self.obj2, (float, Decimal, int)) else self.obj2.evalf()
                return op1 / op2
            elif self.oper == Operations.Multiply:
                op1 = self.obj1 if isinstance(self.obj1, (float, Decimal, int)) else self.obj1.evalf()
                op2 = self.obj2 if isinstance(self.obj2, (float, Decimal, int)) else self.obj2.evalf()
                return op1 * op2
            elif self.oper == Operations.Power:
                op1 = self.obj1 if isinstance(self.obj1, (float, Decimal, int)) else self.obj1.evalf()
                op2 = self.obj2 if isinstance(self.obj2, (float, Decimal, int)) else self.obj2.evalf()
                return math.pow(op1, op2)


a = Root(2, 2, 2)
b = Root(2,2,3)
print(str((a+b).evalf()))