




def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(byte != ""):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			#encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)
			
			output.write(decompressed_text)

		print("Decompressed")
return output_path


if (sys.argv[1] == "-c"):
    compress()
elif (sys.argv[1] == "-d"):
    decompress()
else:
    print ("ERRO! Acoes possiveis: \"-c\" para compactar ou"+\
          "\n\"-d\" para descompactar")
sys.exit()