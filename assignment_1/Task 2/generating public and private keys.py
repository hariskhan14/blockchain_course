import rsa

# Load keys from files
with open("public.pem", "rb") as pub_file:
    publicKey = rsa.PublicKey.load_pkcs1(pub_file.read())

with open("private.pem", "rb") as priv_file:
    privateKey = rsa.PrivateKey.load_pkcs1(priv_file.read())

print(publicKey)
print(privateKey)
