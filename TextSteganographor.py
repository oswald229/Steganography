import imageio

class TextSteganographor:

    def __init__(self, img, msg=''):

        self.idx_changed = []
        self._idx_to_change = []
        self._img = img
        self._msg = msg + "_end_of_transmission"
        self._binaryMsg = self.message_to_binary_array(self._msg)
        self._imgHeight = img.shape[0]
        self._imgWidth = img.shape[1]
        self._coded = False

    def message_to_binary_array(self, msg):
        """
        Convert a character to its ASCII value formatted to binary.

        :param: msg
        :return : Array
        """
        
        binary = []
        
        msg = str(msg)

        for i in range(0, len(msg)):
            temp = ord(msg[i])
            temp = format(temp, '08b')            
            binary.append(temp)

        return binary

    def to_8_binary(self, val):
        """
        Convert an integer to 8-bits binary.
        :param : val : int
        :return: String
        """        
        return format(int(val), '#010b')
    
    def get_idxs(self, start, amount, tab):
        """
        Get pixels to modify indexes.
        :param : start : [,] Starting point.
        :param : amount : Amount of pixels needed.
        :param : tab : Array to get pixels from.
        :return : Array
        """

        idxs = []
        target_amount = 0
        i = start[0]
        j = start[1]

        while target_amount < amount:

            if j < tab.shape[1]:
                if i < tab.shape[0]:
                    idxs.append([i, j])
                    target_amount += 1
                    j += 1
                else:
                    break
            else:
                j = 0
                i += 1       

        return idxs
 
    def put_message(self, start_idx_i, start_idx_j, color='R'):
        """
        Hide the text message, given the starding indexes, and color layer.
        :param start_idx_i : Starting row index.
        :param start_idx_j :Starting column index.
        :param color : Layer to process.
        :return : Imageio
        """
        to_change = 0
        if color == 'R':
            color = 0
        if color == 'G':
            color = 1
        if color == 'B':
            color = 2

        self._idx_to_change = self.get_idxs([start_idx_i, start_idx_j], 4 *
                      len(self._binaryMsg), self._img)

        for x in range(0, len(self._binaryMsg)):

            current_msg = self._binaryMsg[x]

            idxMsgLetter = 0

            # Select group of 4 pixels
            pixelsACoder = self._idx_to_change[4*x:4*x + 4]

            for idx in pixelsACoder:
                
                # Select layer
                pixel_layer = self._img[idx[0]][idx[1]][color]

                pixel_layer = self.to_8_binary(pixel_layer)

                pixel_layer = list(pixel_layer)

                pixel_layer[-2] = current_msg[idxMsgLetter]
                
                pixel_layer[-1] = current_msg[idxMsgLetter + 1]

                idxMsgLetter += 2

                self.idx_changed.append(idx)
                
                pixel_layer = "".join(pixel_layer)

                self._img[idx[0]][idx[1]][color] = int(pixel_layer, 2)

        self._coded = True
        return self._img

def decode_stegano(image, start_index_x, start_index_y, length, color):
    """
    :param image: Image to decode. (Imageio)
    :param start_index_x: Starting row index.
    :param start_index_y: Starting col index.
    :param length: Guessed length of the message.
    :param color: Layer to process on.
    :return: List of indexes. 
    """
    if color == 'R':
        color = 0
    if color == 'G':
        color = 1
    if color == 'B':
        color = 2

    decoded = ""
    idxs = TextSteganographor.get_idxs([start_index_x, start_index_y], 4 * length, image)

    for i in range(0, length):
        indexs = idxs[i * 4:i * 4 + 4]

        letter = '0b'

        for k in indexs:
            pix = bin(image[k[0],k[1]][color])
            letter += pix[-2:]

        if letter!='0b':
            letter = chr(int(letter, 2))
            decoded += letter

        if "_end_of_transmission" in decoded:
            break

    
    return decoded

