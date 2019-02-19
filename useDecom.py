from decom import HuffmanCoding

#input file path
path = "C:\Users\Dell\Desktop\Marcus\UnB\10º semestre\Teoria da Informação\Trabalho\teste.arq"

h = HuffmanCoding(path)

#output_path = h.compress()
h.decompress(path)
