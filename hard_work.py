import functions as f


# Simplifies a fraction
def simplifies(num, denominator, fir=2):
    if num % denominator == 0:
        return [int(num / denominator), 1]
    if num % fir == 0 and denominator % fir == 0:
        return simplifies(num / fir, denominator / fir, fir + 1)
    if fir == 20:
        return [int(num), int(denominator)]
    return simplifies(num, denominator, fir + 1)


# Creates a ROL (Organized list) of the input data
def get_rol_inside(my_list1):
    my_list1 = [int(value) for value in my_list1.strip().split(" ")]  # Transform my list into integer list
    rol_inside_inside = sorted(my_list1)  # sort the new list
    return rol_inside_inside


# Creates a dictionary with each value of the ROL and his frequency
def get_frequency(rol_inside):
    new_dict = {}
    ind = 0
    for r in rol_inside:
        if r in new_dict:
            new_dict[r] += 1
        else:
            new_dict[r] = 1
        ind += 1
    return new_dict


# Given the frequency dictionary and the size of the intervals it returns the list of intervals
def get_intervals(new_dict, size, maximum):
    range_f, range_i, interval = 0, 0, []
    for d in new_dict:
        if range_f == 0 and range_i == 0:
            range_i, range_f = d, d + size
        if range_f >= maximum:
            interval.append([range_i, range_f])
            break
        interval.append([range_i, range_f])
        range_i, range_f = range_f, range_f + size
    return interval


# Returns a list. Each element represents the value of the absolute frequency for the corresponding line of the table
def absolute_frequency(interval, new_dict, ultimo):
    fr_tot = 0
    lines = []
    for i in interval:
        current = i[0]
        if i[-1] == ultimo:
            while current <= i[1]:
                if current in new_dict:
                    fr_tot += new_dict[current]
                current += 1
            lines.append(fr_tot)
            fr_tot = 0
        else:
            while current < i[1]:
                if current in new_dict:
                    fr_tot += new_dict[current]
                current += 1
            lines.append(fr_tot)
            fr_tot = 0
    return lines


# Returns a list. Each element represents the value of the relative frequency for the corresponding line of the table
def relative_frequency(freq_abs, num_elem):
    return [simplifies(freq, num_elem) for freq in freq_abs]


# Returns a list. Each element represents the value of the relative frequency percentage
# for the corresponding line of the table
def relative_frequency_percentage(freq_rel):
    return [round(freq[0]/freq[1], 3) for freq in freq_rel]


# Returns a list. Each element represents the value of the cumulative frequency for the corresponding line of the table
def cumulative_frequency(freq_abs):
    acum, lines = 0, []
    for freq in freq_abs:
        acum += freq
        lines.append(acum)
    return lines


# Returns a list. Each element represents the value of the cumulative frequency percentage
# for the corresponding line of the table
def cumulative_frequency_percentage(cumulative_freq):
    num_elem = cumulative_freq[-1]
    lines = [round(freq * 100 / num_elem, 3) for freq in cumulative_freq]
    return lines


# changes the format in which the relative frequency values appear in the table
def change_format1(f_rel):
    return [str(int(freq[0])) + "/" + str(int(freq[1])) for freq in f_rel]


# changes the format in which the classes appear in the table
def change_format2(cla):
    return [str(int(c[0])) + "|-" + str(int(c[1])) for c in cla]


# draws the frequency table on the terminal
def display_table(columns):
    lines, numbers = [], [7, 14, 14, 22, 17, 21]
    columns[2], columns[0] = change_format1(columns[2]), change_format2(columns[0])
    line, i, columns_size = "| ", 0, len(columns[0])-1
    while i <= columns_size:
        for c in columns:
            space = (numbers[columns.index(c)] - len(str(c[i]))) // 2
            line += " " * space + str(c[i]) + " " * space + "  |"
        lines.append(line)
        line = "| "
        i += 1
    print(
        " Classe      | Freq. Absoluta | Freq. Relativa| Freq. Rel. Percentual| Freq. Acumulativa| Freq. Acum."
        "Percentual|")
    separator = "-"*114  # a line that will separate the lines of the table
    for line in lines:  # draws the table. for each iterations a line is drawn and then the correspondent table line
        print(separator)
        print(line)


def write_table_content(content):
    with open("data.txt", "a") as file:
        for i in range(len(content[0])):
            for column in content:
                file.write(f"{column[i]} ")
            file.write("\n")


# Calculates the number of classes that will be created for the given sample
def get_classes_number(rol_inside):
    n = len(rol_inside)
    k = n ** (1 / 2)
    return int(k // 1 + 1) if type(k) == float else k


# Returns the index of the element that repeats the most
def get_mode_class(freq_abs):
    biggest_frequency, index = 0, 0
    for freq in freq_abs:
        if freq > biggest_frequency:
            biggest_frequency = freq
            index = freq_abs.index(freq)
    return index


def get_mode(roll):
    mode, repetitions = None, 0
    for element in roll:
        elem_repet = roll.count(element)
        if elem_repet > repetitions:
            mode, repetitions = element, elem_repet
    return mode


# returns the median element (the one that divides the sample in half)
def get_median(rol_inside):
    if len(rol_inside) % 2 == 0:
        return rol_inside[int(len(rol_inside) / 2)]
    else:
        return [rol_inside[int(len(rol_inside) // 2) - 1], rol_inside[int(len(rol_inside) / 2)] + 1]


def get_desvio_padrao(media_inside, rol_inside, tamanho_inside):
    current = [(r - media_inside) ** 2 for r in rol_inside]
    # print(current)
    value = (sum(current) / tamanho_inside)**(1/2)
    return value


def do_the_work_customized():
    with open("data.txt", "r") as file:
        my_list = file.readline()
    escolha = input("deseja especificar o tamanho das classes? (y/n): ")
    rol = get_rol_inside(my_list)
    amplitude_total = rol[-1] - rol[0]
    num_classes = get_classes_number(rol)
    if escolha == "y":
        amplitude_classe = int(input("Insira o valor dos intervalos das classes:"))
    else:
        amplitude_classe = amplitude_total / num_classes
        if amplitude_classe // 1 != amplitude_classe:
            amplitude_classe = int(amplitude_classe // 1 + 1)

    # print(f"maximo: {max(rol_inside)}; minimo: {min(rol_inside)}") #MOSTRAR O MAXIMO E O MINIMO DA my_list
    # NESTA PARTE PODEM SER FEITAS AS OPERAçOES QUE SE DESEJAM REALIZAR COM OS DADOS DO ENUNCIADO
    f.clean_screen()
    tamanho = len(rol)
    freq = get_frequency(rol)
    intervalos = get_intervals(freq, amplitude_classe, max(rol))
    fr_abs = absolute_frequency(intervalos, freq, rol[-1])
    fr_rel = relative_frequency(fr_abs, len(rol))
    fr_rel_perc = relative_frequency_percentage(fr_rel)
    fr_acum = cumulative_frequency(fr_abs)
    fr_acum_perc = cumulative_frequency_percentage(fr_acum)
    media = round(sum(rol) / len(rol), 4)
    moda = intervalos[get_mode(fr_abs)]
    mediana = get_median(rol)
    desvio_padrao = get_desvio_padrao(media, rol, tamanho)
    varianca = desvio_padrao ** 2
    if escolha == "y":
        num_classes = len(fr_abs)

    print(f" rol dos dados: {rol};")
    print(f" Amplitude total (R): {amplitude_total};")
    print(f" Amplitude das classes (h): {int(amplitude_classe)};")
    print(f" Tamanho da amostra (n): {tamanho};")
    print(f" Numero de classes (K): {num_classes};")
    print(f" Media aritmetica: {media};")
    print(f" Moda (Mo): {moda};")
    print(f" Mediana : {mediana};")
    print(f" varianca : {varianca};")
    print(f" Desvio Padrao : {desvio_padrao};\n")
    display_table([intervalos, fr_abs, fr_rel, fr_rel_perc, fr_acum, fr_acum_perc])


def do_the_work_standard():
    with open("data.txt", "r") as file:
        my_list = file.readline()
    rol = get_rol_inside(my_list)
    amplitude_total = rol[-1] - rol[0]
    num_classes = get_classes_number(rol)
    amplitude_classe = amplitude_total / num_classes
    if amplitude_classe // 1 != amplitude_classe:
        amplitude_classe = int(amplitude_classe // 1 + 1)
    tamanho = len(rol)
    freq = get_frequency(rol)
    intervalos = get_intervals(freq, amplitude_classe, max(rol))
    fr_abs = absolute_frequency(intervalos, freq, rol[-1])
    fr_rel = relative_frequency(fr_abs, len(rol))
    fr_rel_perc = relative_frequency_percentage(fr_rel)
    fr_acum = cumulative_frequency(fr_abs)
    fr_acum_perc = cumulative_frequency_percentage(fr_acum)
    media = round(sum(rol) / len(rol), 4)
    moda = get_mode(rol)
    class_moda = intervalos[get_mode_class(fr_abs)]
    mediana = get_median(rol)
    desvio_padrao = get_desvio_padrao(media, rol, tamanho)
    varianca = desvio_padrao ** 2
    with open("data.txt", "w") as file:
        file.write(f"{' '.join(map(str, rol))} \n{amplitude_total} {int(amplitude_classe)} {tamanho} {num_classes}"
                   f" {media} {moda} {class_moda} {mediana} {round(varianca, 4)} {round(desvio_padrao, 4)} \n")
    write_table_content([intervalos, fr_abs, fr_rel, fr_rel_perc, fr_acum, fr_acum_perc])
