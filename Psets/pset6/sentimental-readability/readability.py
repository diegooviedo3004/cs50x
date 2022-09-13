# TODO
count_letter = 0
count_word = 1
count_sentence = 0


text = input("Text: ")
text_length = len(text)

# recorrer la longitud del texto
for i in range(text_length):
    if(text[i].isalpha()):
        count_letter += 1

# contar el numero de palabras en dependencia de los espacios
    if (text[i].isspace()):
        count_word += 1

# contar el numero de oraciones
    if(text[i] == '.' or text[i] == '?' or text[i] == '!'):
        count_sentence += 1

# calculo
calculation = (0.0588 * count_letter / count_word * 100) - (0.296 * count_sentence / count_word * 100) - 15.8

# redondeo
index = round(calculation)

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")