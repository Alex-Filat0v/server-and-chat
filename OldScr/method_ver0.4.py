import rsa
(pubkey, privkey) = rsa.newkeys(512)
 
message = b"Hello World!"

print(message)

crypto = rsa.encrypt(message, pubkey)
print(crypto)

message = rsa.decrypt(crypto, privkey)
print(str(message))

input ("nothing")
