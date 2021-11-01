STOP_WORDS = [
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has',
    'he', 'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to',
    'were', 'will', 'with'
]

import string

class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def read_contents(self):
        """
        This should read all the contents of the file
        and return them as one string.
        """
        with open(self.filename) as text_file:
            file_as_string = text_file.read()
        return file_as_string


class WordList:
    def __init__(self, text):
        self.text = text

    def extract_words(self):
        """
        This should get all words from the text. This method
        is responsible for lowercasing all words and stripping
        them of punctuation.
        """
        self.text = self.text.replace("\n", "  ")
        self.text = self.text.replace("—", " ")
        self.text = self.text.translate(str.maketrans('', '', string.punctuation))
        self.text = self.text.lower()
        self.text = self.text.split(" ")
        while '' in self.text:
            self.text.remove('')
        return self.text

    def remove_stop_words(self):
        """
        Removes all stop words from our word list. Expected to
        be run after extract_words.
        """
        self.text = [word for word in self.text if word not in STOP_WORDS]
        return self.text

    def get_freqs(self):
        """
        Returns a data structure of word frequencies that
        FreqPrinter can handle. Expected to be run after
        extract_words and remove_stop_words. The data structure
        could be a dictionary or another type of object.
        """
        word_dict = {}
        for word in self.text:
            if word not in word_dict:
                word_dict.update({word : 1})
            else:
                word_dict[word] += 1
        sorted_dict = sorted(word_dict.items(), key=lambda word: word[1], reverse=True)
        return sorted_dict


class FreqPrinter:
    def __init__(self, freqs):
        self.freqs = freqs

    def print_freqs(self):
        """
        Prints out a frequency chart of the top 10 items
        in our frequencies data structure.

        Example:
          her | 33   *********************************
        which | 12   ************
          all | 12   ************
         they | 7    *******
        their | 7    *******
          she | 7    *******
         them | 6    ******
         such | 6    ******
       rights | 6    ******
        right | 6    ******
        """
        longest_word_len = 0
        index = 0
        while index < 9:
            if(len(self.freqs[index][0]) > longest_word_len):
                longest_word_len = len(self.freqs[index][0])
            index += 1
        index = 0
        while index < 9:
            half_print_string  = f"{self.freqs[index][0]} | ".rjust(longest_word_len + 4)
            print(half_print_string + f"{self.freqs[index][1]}".rjust(2) + " " + "*"*self.freqs[index][1])
            index += 1


if __name__ == "__main__":
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='Get the word frequency in a text file.')
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        reader = FileReader(file)
        word_list = WordList(reader.read_contents())
        word_list.extract_words()
        word_list.remove_stop_words()
        printer = FreqPrinter(word_list.get_freqs())
        printer.print_freqs()
    else:
        print(f"{file} does not exist!")
        sys.exit(1)
