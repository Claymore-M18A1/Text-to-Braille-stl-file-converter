from stl import mesh
import numpy as np

# Constants for easy adjustment
A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297
DOT_DIAMETER_MM = 1.5
DOT_HEIGHT_MM = 0.5
DOT_SPACING_MM = 2.5
LINE_SPACING_MM = 5  # Spacing between lines of Braille
LETTER_SPACING_MM = 2.5  # Spacing between letters

# Braille dictionary
braille_dict = {
    'a': '100000', 'b': '101000', 'c': '110000', 'd': '110100', 'e': '100100', 'f': '111000',
    'g': '111100', 'h': '101100', 'i': '011000', 'j': '011100', 'k': '100010', 'l': '101010',
    'm': '110010', 'n': '110110', 'o': '100110', 'p': '111010', 'q': '111110', 'r': '101110',
    's': '011010', 't': '011110', 'u': '100011', 'v': '101011', 'w': '011101', 'x': '110011',
    'y': '110111', 'z': '100111', '1': '100000', '2': '101000', '3': '110000', '4': '110100',
    '5': '100100', '6': '111000', '7': '111100', '8': '101100', '9': '011000', '0': '011100',
    '.': '010011', ',': '010000', '?': '010001', ';': '011000', ':': '010010', '!': '011010',
    '(': '011011', ')': '011011', '-': '001001', '/': '001100', ' ': '000000',
    'but': '110100', 'can': '101000', 'do': '110101', 'every': '111000', 'from': '111001',
    'go': '111010', 'have': '111011', 'just': '111100', 'knowledge': '111101', 'like': '111110',
    'more': '111111', 'not': '100011', 'people': '100111', 'quite': '101000', 'rather': '101001',
    'so': '101010', 'that': '101011', 'us': '101100', 'very': '101101', 'will': '101110',
    'it': '101111', 'you': '110000', 'as': '110001', 'and': '110010', 'for': '110011', 'of': '110100',
    'the': '110101', 'with': '110110', 'to': '110111', 'in': '111000'
}

def translate_to_braille(text):
    braille_text = []
    for word in text.split():
        if word.isupper():
            braille_text.append('000001')  # Capitalization indicator for entire word
            braille_text.append('000001')  # Second capitalization indicator
            for char in word:
                braille_text.append(braille_dict[char.lower()])
        else:
            for char in word:
                if char.isupper():
                    braille_text.append('000001')  # Capitalization indicator
                    braille_text.append(braille_dict[char.lower()])
                elif char in braille_dict:
                    braille_text.append(braille_dict[char])
                else:
                    braille_text.append('000000')  # Space or unknown character
        braille_text.append('000000')  # Space between words
    return braille_text

def create_braille_stl(braille_text, filename="braille_output.stl"):
    vertices = []
    faces = []
    x_offset = 10
    y_offset = 10

    for braille_char in braille_text:
        if braille_char == '000000':  # Handle space character
            x_offset += DOT_SPACING_MM * LETTER_SPACING_MM  # Move to the next character column
            if x_offset > A4_WIDTH_MM - 20:
                x_offset = 10  # Reset to left margin
                y_offset += DOT_SPACING_MM * LINE_SPACING_MM  # Move to the next row
            continue
        
        for i, dot in enumerate(braille_char):
            if dot == '1':
                x = x_offset + (i % 2) * DOT_SPACING_MM
                y = y_offset + (i // 2) * DOT_SPACING_MM
                vertices.append([x, y, 0])
                vertices.append([x + DOT_DIAMETER_MM, y, 0])
                vertices.append([x + DOT_DIAMETER_MM, y + DOT_DIAMETER_MM, 0])
                vertices.append([x, y + DOT_DIAMETER_MM, 0])
                
                vertices.append([x, y, DOT_HEIGHT_MM])
                vertices.append([x + DOT_DIAMETER_MM, y, DOT_HEIGHT_MM])
                vertices.append([x + DOT_DIAMETER_MM, y + DOT_DIAMETER_MM, DOT_HEIGHT_MM])
                vertices.append([x, y + DOT_DIAMETER_MM, DOT_HEIGHT_MM])
                
                base_index = len(vertices) - 8
                faces.append([base_index, base_index + 1, base_index + 2])
                faces.append([base_index, base_index + 2, base_index + 3])
                faces.append([base_index + 4, base_index + 5, base_index + 6])
                faces.append([base_index + 4, base_index + 6, base_index + 7])
                faces.append([base_index, base_index + 1, base_index + 5])
                faces.append([base_index, base_index + 5, base_index + 4])
                faces.append([base_index + 1, base_index + 2, base_index + 6])
                faces.append([base_index + 1, base_index + 6, base_index + 5])
                faces.append([base_index + 2, base_index + 3, base_index + 7])
                faces.append([base_index + 2, base_index + 7, base_index + 6])
                faces.append([base_index + 3, base_index, base_index + 4])
                faces.append([base_index + 3, base_index + 4, base_index + 7])
        
        x_offset += DOT_SPACING_MM * LETTER_SPACING_MM  # Adjust for next character column
        if x_offset > A4_WIDTH_MM - 20:
            x_offset = 10  # Reset to left margin
            y_offset += DOT_SPACING_MM * LINE_SPACING_MM  # Move to the next row

    vertices = np.array(vertices)
    faces = np.array(faces)
    
    braille_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            braille_mesh.vectors[i][j] = vertices[face[j], :]

    braille_mesh.save(filename)

input_text = input("Enter the text to convert to Braille: ")
braille_text = translate_to_braille(input_text)
create_braille_stl(braille_text)
