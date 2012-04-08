import random
names = ['Abadom', 'Abaeze', 'Abayomrunkoje', 'Abebi', 'Abegunde', 'Abeni', 'Abeo', 'Abidemi', 'Abidugun', 'Abiodun', 'Abiodun', 'Abioye', 'Abioye', 'Achebe', 'Achike', 'Achutebe', 'Ada-afo', 'Adamma', 'Adankwo', 'Adaoma', 'Adaora', 'Adebambo', 'Adebamgbe', 'Adebisi', 'Adebiyi', 'Adebowale', 'Adeboye', 'Adedayo', 'Adedeji', 'Adedoyin', 'Adefolake', 'Adejola', 'Adekola', 'Adeleke', 'Adeleye', 'Adenike', 'Adenike', 'Adeola', 'Adeolu', 'Aderinola', 'Aderiyike', 'Adesewa', 'Adesola', 'Adetokunbo', 'Adetosoye','Adetowumi', 'Adewemimo', 'Adewole', 'Adeyemi', 'Adeyemo', 'Adigun', 'Adimabua', 'Adodoola', 'Adunola', 'Afafa', 'Afiba']

sex = ["male", "female"]

age = range(16, 121)

reg = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

registrationnumber = []
while len(registrationnumber) < 14:
	registrationnumber.append(random.choice(reg))
numbers = range(0, 10)
pin = []
while len(pin) < 5:
	pin.append(random.choice(numbers))

subjects = ["maths", "english", "physics", "chemistry", "biology"]

