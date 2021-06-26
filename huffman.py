import sys
import argparse
import shutil


#Node creation
class Node:
    def __init__(self,freq):
        self.left = None
        self.right = None
        self.root = None
        self.freq = freq
        
    def isLeft(self):
        return self.root.left == self
    
    
#create nodesCreate leaf nodes
def createNodes(freqs):
    return [Node(freq) for freq in freqs]


#create Huffman-Tree
def createHuffmanTree(nodes):
    queue = nodes[:]
    
    #create a huffman tree until the len(queue) becomes as root(means len(queue)==1)
    while len(queue) > 1:
        queue.sort(key=lambda item:item.freq)
        node_left = queue.pop(0)
        node_right = queue.pop(0)
        node_root = Node(node_left.freq + node_right.freq)
        node_root.left = node_left
        node_root.right = node_right
        node_left.root = node_root
        node_right.root = node_root
        queue.append(node_root)
    queue[0].root = None
    return queue[0]


#Huffman coding and returns the huffmancode for each different character
def huffmanEncoding(nodes,root):
    
    codes = [''] * len(nodes)
    for i in range(len(nodes)):
        node_tmp = nodes[i]
        
        #update "0" and "1" for each nodes until it becomes sub_root
        while node_tmp != root:
            #Add "0" for left most nodes
            if node_tmp.isLeft():
                codes[i] = '0' + codes[i]
            #Add "1" for left most nodes
            else:
                codes[i] = '1' + codes[i]
            node_tmp = node_tmp.root
    return codes

 

#Get Huffman encoding
def encode(input_file,output_file):   
    
    print("encoding ", input_file, output_file)
    
    #read the file and store it in the string
    f=open(input_file,'r')
    string=list(f.read())
    
    #create a dictionary of chars with frequency
    dict1 ={}
    for  i in string:
        if i in dict1.keys():
            dict1[i] += 1
        else :
            dict1[i] = 1 
            
    #Sort characters according to frequency
    chars_freqs  = sorted(dict1.items(), key = lambda kv:(kv[1], kv[0]))
    
    #Create huffman node tree
    nodes = createNodes([item[1] for item in chars_freqs])
    root = createHuffmanTree(nodes)
    
    #Huffman encoding of each character
    codes = huffmanEncoding(nodes,root)
   
    #create dictionary to store the values with frequency
    dict2 = {}
    for item in zip(chars_freqs,codes):
        dict2[item[0][0]] = item[1]
        
    #Huffman encoded bits
    str = ''
    for v in string:
        str += dict2[v]
        
    #print(string)
    #write the file as .huff
    f=open(output_file,'w+')
    f.write(str)
        
    #store the bits with characters
    f1=open("code.txt",'w+')
    
    #update the each values into the file
    for i in dict2.items():
         f1.write(i[1]+':'+i[0]+'\n')
    if input_file != "" and output_file != "":
		shutil.copyfile(input_file, output_file)
        
    
def decode (input_file,output_file):
    
    
    f_code = open("code.txt",'r')
    dictionary = {}
    codes = f_code.readlines()
    
    
    #creation of dictionry for code.txt file
    for code in codes:
        if ':' in code:
            tmp = code.split(':')
            key = tmp[0]
            
            if len(tmp[1])==1:
                value = tmp[1]
            else:
                value = tmp[1].replace('\n','')

            dictionary[key] = value
            
    #print(dictionary)

    f_content = open(input_file,'r')
    text1 = f_content.readlines()
    #print(text1)
    
    text=""
    for i in range(len(text1[0])):
        text=text+str(text1[0][i])
        
    #print(text)
    
    #result of the decoded text and stores into given output_path
    res = ""
    while text:
        for k in dictionary:
            if text.startswith(k):
                res += dictionary[k]
                text = text[len(k):]
    #return res 
    f=open(output_file,'w+')
    f.write(res) 
    
    print("decoded done")
    if input_file != "" and output_file != "":
		shutil.copyfile(input_file, output_file)
    

    
    


def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Huffman compression.")
    groups = parser.add_mutually_exclusive_group(required=True)
    groups.add_argument("-e", type=str, help="Encode files")
    groups.add_argument("-d", type=str, help="Decode files")
    parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
    options = parser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()
    if options.e is not None:
        encode(options.e, options.o)
    if options.d is not None:
        decode(options.d, options.o) 
