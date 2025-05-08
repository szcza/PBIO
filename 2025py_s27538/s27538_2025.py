# -*- coding: utf-8 -*-
"""
Program: Generator sekwencji nukleotydowych w formacie FASTA
Autor: s27538
Rok: 2025

Cel programu:
    Ten skrypt pozwala na wygenerowanie losowej sekwencji DNA o zadanej długości,
    z możliwością wstawienia w losowym miejscu imienia użytkownika (wstawka nie wliczana
do długości ani statystyk). Sekwencja jest zapisywana do pliku FASTA, a program wyświetla
statystyki procentowej zawartości nukleotydów.

Kontekst:
    Ćwiczenie z bioinformatyki – przygotowanie generatora sekwencji w formacie FASTA,
    rozszerzenie kodu wygenerowanego przez LLM o dodatkowe ulepszenia i wyjaśnienia.
"""
import random  # biblioteka do losowego wyboru nukleotydów

# Pobieranie danych od użytkownika:
# ORIGINAL:
# length = int(input("Podaj długość sekwencji: "))
# MODIFIED (dodanie sprawdzenia poprawności i obsługi błędów):
while True:
    try:
        length = int(input("Podaj długość sekwencji (liczba całkowita > 0): "))  # długość sekwencji
        if length <= 0:
            raise ValueError
        break
    except ValueError:
        print("Błąd: proszę wprowadzić dodatnią liczbę całkowitą.")

# ORIGINAL:
# seq_id = input("Podaj ID sekwencji: ")
# MODIFIED (usunięcie spacji w ID i obsługa pustego wprowadzenia):
while True:
    seq_id = input("Podaj ID sekwencji (bez spacji): ").strip()
    if seq_id and " " not in seq_id:
        break
    print("Błąd: ID nie może być puste ani zawierać spacji.")

# ORIGINAL:
# description = input("Podaj opis sekwencji: ")
# MODIFIED (strip i ograniczenie długości opisu):
description = input("Podaj opis sekwencji: ").strip()  # opis wpisany przez użytkownika
if len(description) > 80:
    print("Uwaga: opis długi, zostanie przycięty do 80 znaków.")
    description = description[:80]

# ORIGINAL:
# name = input("Podaj imię: ")
# MODIFIED (strip i obsługa pustego imienia) i zamiana dużych liter 'ACGT' używanych w imieniu na małe
while True:
    name = input("Podaj imię do wstawienia (litery A-Z, bez spacji): ").strip()
    name = ''.join(ch.lower() if ch in 'ACGT' else ch for ch in name)
    if name.isalpha():
        break
    print("Błąd: imię musi zawierać tylko litery i nie może być puste.")

# Generowanie sekwencji DNA bez imienia (tylko A,C,G,T)
nucleotides = ['A', 'C', 'G', 'T']  # możliwe nukleotydy
sequence = ''.join(random.choice(nucleotides) for _ in range(length))  # losowa sekwencja

# Wstawienie imienia w losowej pozycji
insert_pos = random.randint(0, length)  # pozycja w zakresie [0, length]
fasta_sequence = sequence[:insert_pos] + name + sequence[insert_pos:]

# Obliczanie statystyk (bez imienia):
count_A = sequence.count('A')
count_C = sequence.count('C')
count_G = sequence.count('G')
count_T = sequence.count('T')
# Całkowita długość czystej sekwencji
clean_len = length
# Procentowa zawartość nukleotydów
perc_A = count_A / clean_len * 100
perc_C = count_C / clean_len * 100
perc_G = count_G / clean_len * 100
perc_T = count_T / clean_len * 100
# Stosunek C+G do A+T
perc_CG = (count_C + count_G) / clean_len * 100

# Zapis do pliku FASTA
filename = f"{seq_id}.fasta"  # nazwa pliku na podstawie ID
with open(filename, 'w', encoding='utf-8') as fasta_file:
    # Nagłówek FASTA
    fasta_file.write(f">{seq_id} {description}\n")
    # Sekwencja z imieniem
    fasta_file.write(fasta_sequence + '\n')

# Wyświetlenie informacji dla użytkownika
print(f"Sekwencja została zapisana do pliku {filename}")
print("Statystyki sekwencji:")
print(f"A: {perc_A:.1f}%")  # jeden znak po przecinku
print(f"C: {perc_C:.1f}%")
print(f"G: {perc_G:.1f}%")
print(f"T: {perc_T:.1f}%")
print(f"%CG: {perc_CG:.1f}%")

# KONIEC PROGRAMU
# Ulepszenia:
# 1. Walidacja i obsługa błędów przy wprowadzaniu długości, ID oraz imienia
# 2. Ograniczenie długości opisu oraz informacja o przycięciu
# 3. Czytelne formatowanie wyjścia i wyjaśniające komentarze do każdej sekcji
