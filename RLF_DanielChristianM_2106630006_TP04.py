# TP 04
# Nama  : Daniel Christian Mandolang
# Kelas : A
# NPM   : 2106630006

from tkinter import *
from tkinter.font import *
from tkinter.messagebox import *


def flip_bits(s: str) -> str:
    """Flip the bits of a binary string"""

    ret = ''
    for i in s:
        ret += '0' if i == '1' else '1'
    return ret

encode_key = ['LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG',
              'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL']

encode_bit = {}
encode_bit['L'] = ['0001101', '0011001', '0010011', '0111101', '0100011',
                   '0110001', '0101111', '0111011', '0110111', '0001011']
encode_bit['R'] = [flip_bits(i) for i in encode_bit['L']]
encode_bit['G'] = [i[::-1] for i in encode_bit['R']]


def encode_front(code: str, fst_digit: int) -> str:
    """Encode the first half of a code"""

    ret = ''
    for i in range(len(code)):
        digit = int(code[i])
        ret += encode_bit[encode_key[fst_digit][i]][digit]
    return ret


def encode_back(code: str) -> str:
    """Encode the second half of a code"""

    ret = ''
    for i in range(len(code)):
        digit = int(code[i])
        ret += encode_bit['R'][digit]
    return ret


def check_sum(code: str) -> str:
    """Calculate the check digit of a code"""

    digit_sum = 0
    for i in range(len(code)):
        digit = int(code[i])
        if (i % 2 == 0):
            digit_sum += digit
        else:
            digit_sum += 3*digit

    if (digit_sum % 10 == 0):
        return '0'
    return str(10 - digit_sum % 10)


def encode(code: str) -> str:
    """Encode a code"""

    fst_digit = int(code[0])
    front, back = code[1:7], code[7:]
    return encode_front(front, fst_digit) + encode_back(back)


class Barcode:
    def __init__(self):
        window = Tk()
        window.title('EAN-13 [by Daniel C.M.]')
        window.geometry('455x555')
        window.resizable(False, False)

        self.font_style_bold = Font(window, size=17, weight=BOLD)
        self.font_style = Font(window, size=17)

        file_name_label = Label(window, font=self.font_style_bold)
        file_name_label['text'] = 'Save barcode to PS file [eg: EAN13.eps]:'
        file_name_label.pack()

        self.file_name_var = StringVar()
        file_name_entry = Entry(window, width=16, font=self.font_style)
        file_name_entry['textvariable'] = self.file_name_var
        file_name_entry.pack()

        code_label = Label(window, font=self.font_style_bold)
        code_label['text'] = 'Enter code (first 12 decimal digits):'
        code_label.pack()

        self.code_var = StringVar()
        code_entry = Entry(window, width=16, font=self.font_style)
        code_entry['textvariable'] = self.code_var
        code_entry.pack()

        window.bind('<Return>', self.validate_input)

        frame = Frame(window, borderwidth=12)
        frame.pack()

        self.canvas = Canvas(frame, width=340, height=400, bg='white')
        self.canvas.pack()

        window.mainloop()

    def create_barcode(self):
        """Create barcode from code"""

        self.canvas.delete('all')
        self.canvas.create_text(173, 75, font=self.font_style_bold,
                                         text = 'EAN-13 Barcode:')

        lst_digit = check_sum(self.code)
        self.code += lst_digit

        bit_str = encode(self.code)
        pos_x, pos_y = 53, 110
        size_x, size_y = 2.5, 180

        for i in (range(len(bit_str))):
            if (i == 0):
                self.canvas.create_rectangle(pos_x, pos_y,
                                             pos_x+size_x, pos_y+size_y+10,
                                             fill='blue', outline='')
                pos_x += 2*size_x
                self.canvas.create_rectangle(pos_x, pos_y,
                                             pos_x+size_x, pos_y+size_y+10,
                                             fill='blue', outline='')
                pos_x += size_x

            if (i == 42):
                pos_x += size_x
                self.canvas.create_rectangle(pos_x, pos_y,
                                             pos_x+size_x, pos_y+size_y+10,
                                             fill='blue', outline='')
                pos_x += 2*size_x
                self.canvas.create_rectangle(pos_x, pos_y,
                                             pos_x+size_x, pos_y+size_y+10,
                                             fill='blue', outline='')
                pos_x += 2*size_x

            if (bit_str[i] == '1'):
                self.canvas.create_rectangle(pos_x, pos_y,
                                             pos_x+size_x, pos_y+size_y,
                                             fill='green', outline='')
            pos_x += size_x

            if (i == len(bit_str)-1):
                self.canvas.create_rectangle(pos_x, pos_y,
                                             pos_x+size_x, pos_y+size_y+10,
                                             fill='blue', outline='')
                pos_x += 2*size_x
                self.canvas.create_rectangle(pos_x, pos_y,
                                             pos_x+size_x, pos_y+size_y+10,
                                             fill='blue', outline='')

        pos_x, pos_y = 42, 310
        size_x = 16
        for i in range(len(self.code)):
            self.canvas.create_text(pos_x, pos_y, text=self.code[i],
                                    font=self.font_style_bold)
            if (i == 0 or i == 6):
                pos_x += size_x
            pos_x += size_x

        self.canvas.create_text(170, 345, text=f'Check Digit: {lst_digit}',
                                font=self.font_style_bold, fill='orange')

        self.canvas.postscript(file=self.file_name, colormode='color')

    def validate_input(self, event):
        """Validate file name input and code input"""

        self.code = self.code_var.get()
        self.file_name = self.file_name_var.get()

        if (len(self.code) != 12 or not self.code.isnumeric()):
            showerror(title='Wrong input!',
                      message='Please enter correct input code.')
            return

        if (len(self.file_name) <= 4 or self.file_name[-4:] != '.eps'):
            showerror(title='Wrong input!',
                      message='Output file must have .eps at the end.')
            return
        
        if (' ' in self.file_name):
            showerror(title='Wrong input!',
                      message='Output file name must not contain space(s)')
            return
        
        self.create_barcode()

if (__name__ == '__main__'):
    Barcode()
