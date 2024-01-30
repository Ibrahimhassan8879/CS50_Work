# TODO
from cs50 import get_string
from cs50 import get_int


def count_letters(Text):
    i = 0
    Letters = 0
    for i in range(0, len(Text), 1):
        if ord(f"{Text[i]}") in range(65, 91, 1):
            Letters = Letters + 1
        elif ord(f"{Text[i]}") in range(97, 123, 1):
            Letters = Letters + 1
    return Letters


def count_words(Text):
    Words = 0
    Words = len(Text.split())
    return Words


def count_sentences(Text):
    Sentences = 0
    for i in range(0, len(Text), 1):
        if Text[i] == '.' or Text[i] == '?' or Text[i] == '!':
            Sentences += 1
    return Sentences


def main():
    Text = get_string("Text : \n")

    Av_Letters = 100*count_letters(Text)/(count_words(Text))
    Av_Sentences = 100*count_sentences(Text)/(count_words(Text))

    index = 0.0588*Av_Letters - 0.296*Av_Sentences - 15.8

    print(index)

    if index > 16:
        print("Grade 16+\n")
    elif index < 1:
        print("Before Grade 1 \n")
    else:
        x = round(index)
        print(f"The Grade is {x}\n")

    print(count_letters(Text))
    print(count_words(Text))
    print(count_sentences(Text))


if __name__ == "__main__":
    main()

