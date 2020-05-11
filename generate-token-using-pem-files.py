"""
This script uses RSA public/private key pair generated using Openssl command line tool.
The series of steps are listed below

1. Import openssl generated public/private key pair
3. Generate the Token using the Private key from step 1
4. Validate the JWT Token using the Public key from step 1

"""
# ______________________________ Step 0 ______________________________________
# import python_jwt
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime

# ______________________________ Step 1 ______________________________________
# ______________________________ IMPORT KEY ______________________________________
# Import the key.
# The private key will be used to Generate the Token

# Path to the private and public key files generated using openssl
PRIVATE_KEY_FILE="./keys/private-key.pem"
PUBLIC_KEY_FILE="./keys/public-key.pem"

# Define payload
# payload that the server will send back the client encoded in the JWT Token
# While generating a token, you can define any type of payload in valid JSON format
# the iss(issuer), sub(subject) and aud(audience) are reserved claims. https://tools.ietf.org/html/rfc7519#section-4.1
# These reserved claims are not mandatory to define in a standard JWT token.
# But when working with Istio, it's better you define these.

payload = {
    'iss':'ISSUER', 
    'sub':'SUBJECT', 
    'aud':'AUDIENCE', 
    'role': 'user', 
    'permission': 'read' 
}


public_key = ""
private_key = ""
token=""

with open(PUBLIC_KEY_FILE, "rb") as pemfile:
    public_key = jwk.JWK.from_pem(pemfile.read())
    public_key = public_key.export()
    


with open(PRIVATE_KEY_FILE, "rb") as pemfile:
    private_key = jwk.JWK.from_pem(pemfile.read())
    private_key = private_key.export()


# ______________________________ Step 2 ______________________________________
# ______________________________ GENERATE JWT TOKEN ______________________________________
# Generate the JWT Tokes using the Private Key
# Provide the payload and the Private Key. RS256 is the Hash used and last value is the expiration time.
# You can set the expiration time according to your need.
# To generate JWT Token, you need the private key as a JWK object
token = jwt.generate_jwt(payload, jwk.JWK.from_json(private_key), 'RS256', datetime.timedelta(minutes=500000))


# Print the public key, private key and the token
print("\n_________________PUBLIC___________________\n")
print(public_key)
print("\n_________________PRIVATE___________________\n")
print(private_key)
print("\n_________________TOKEN___________________\n")
print(token)



# ______________________________ Step 4 ______________________________________
# ______________________________ VALIDATE JWT TOKEN USING PUBLIC KEY ______________________________________


# To validate JWT Token, you need the public key as a JWK object
header, claims = jwt.verify_jwt(token, jwk.JWK.from_json(public_key), ['RS256'])

print("\n_________________TOKEN INFO___________________\n")
print(header)
print(claims)


"""
Sample output of the script. You can use these Keys and Tokens to play around. These are valid.
You can use the JWT debugger in this link https://jwt.io/#debugger-io

❯ python generate-token-using-pem-files.py       

_________________PUBLIC___________________

{"e":"AQAB","kid":"oaEC1Z-cdo5YPfZkNZ3CNr73cAjBA6_TMxgBmLIRKfI","kty":"RSA","n":"xXH05CS7qG9gZxMPBL2TemZLNp9Hn8Jyaklb7PfDs4rbKtkcUWGRfHdqO1cOYsMuuRNp5iOyeuDxR9YgnngrNPxcynqY_wAuoZFLNtCjPT1SQnr_8neSNs2Jm57yIgaUWlMj3Xf9T2orzVwX0bmo-R4EQHYLhNgZ6ETHWj8i4_CXme67v-yyqGiPtKkZ10XNBmGb9QV71kfuH9B-M74xoaGH1EnXcCTGaob0URk7sr6nKZjf16WWPb4DwkdaHmrt3B_JIHUfK5iQ8fRSWCKtpZ4FeDVaFHa-IGIQdbTmoh2tgH_1eh9QLQLxfpysAYv3hg-Jclg25TQRpLmoYL1TVQ"}

_________________PRIVATE___________________

{"d":"eGsx8lq84NNctkCXbkq4wXPV93BZXIRZB53KJNJPVxce6BkV_kRFWOXzslE8AtwLiPDgK24mEm9SeH-N0Vh08ZHgfdUbrppL1looxzuj81uM6eLeauCmGips_K6J-lqM7DG8s_vUUDTulgbOuChFd_nome_kwpaR5mjcNJxBCUbGWcvjZxND2MrP5fvcYODIB3BCjiQnltZI-0wEIF5nhT1fr9pCbB0m1_jVh4F9kf9u3ThToCzF8SvbB9nglr2kCHi0WWt79zADV4k6MADEUL03JbctIY3kWSYwN1ejaPkh3iPZTGJP2PhHuZMIL3UAfT4pTx9IdXk6gO69teNLQQ","dp":"K2I6lNUCmqzuByBFWNggmrby782fP2_QljxEldvebab1UelCP_KjVWoeZQagyrKgjh2nc2AkgBUd-TpNig2ndOQ0QjNu30IU1iIki8GeNXq8VMPvNX7sekJQhXuaHC7WsDh_RPwPdSCYi3XzXIyulweqEYXOkAGG0YZvQjsLEuk","dq":"YsLzFGkZBca6U7yNN1G6sh6r5kuQhAzHQn2zS4Y9vDJBB_3unkupCWVKYxsM7BIagmCc2qARNlZwkXDz1uIM0U-swNxhyYNdOuKlg7x52RADoDnl0qToEjHU3MUXgzx2BNFkMxHkmwrR2dMLaWJp2Fxo-hDhnKWe4tsR1Hgknkk","e":"AQAB","kid":"oaEC1Z-cdo5YPfZkNZ3CNr73cAjBA6_TMxgBmLIRKfI","kty":"RSA","n":"xXH05CS7qG9gZxMPBL2TemZLNp9Hn8Jyaklb7PfDs4rbKtkcUWGRfHdqO1cOYsMuuRNp5iOyeuDxR9YgnngrNPxcynqY_wAuoZFLNtCjPT1SQnr_8neSNs2Jm57yIgaUWlMj3Xf9T2orzVwX0bmo-R4EQHYLhNgZ6ETHWj8i4_CXme67v-yyqGiPtKkZ10XNBmGb9QV71kfuH9B-M74xoaGH1EnXcCTGaob0URk7sr6nKZjf16WWPb4DwkdaHmrt3B_JIHUfK5iQ8fRSWCKtpZ4FeDVaFHa-IGIQdbTmoh2tgH_1eh9QLQLxfpysAYv3hg-Jclg25TQRpLmoYL1TVQ","p":"7mL9o-k8dQLeqvHoitw1NKQw_yzGWWYEuR-BUp_TjzcpYS31KkgPdIQKtq4GgrPk-K9vyN840d2osTZBePmHYnKZWMogjdqcpe_frFZTu5flX8GVGPcihJP9KZQHHxQhYK1q24-12KLnbM-o0wi3o5T2LG13vjyLwKpauIKdSVk","q":"1AiRyC6sYRPgWqExSyYsrk_r6h_B3wCdY0j1fm2JGlDr12bSMitNHMjVSJZIWX2H6Y0IxAMeS3Cvkw7avygABzdiNT7nEzbaQ4aAswOEzS2LGNpc24riDas5MxbDROsYWQYhajRtqsHDsPEITlfhw_kZ1XJenDakI_oReSGjXl0","qi":"q7fooPp1eWRyfDDyfVj9XsdF-c2MXM-S3Oq8OXHsVCj6MceelTkve9xlk8Y587aEBLCCYYdglpYn8bHgHTpvQ2Ao39d563UbCRULZCpZU7Qpjc0i0BXMEUy4INr4_KMnfat-sryz1W88EOHeXHoNZiuAC59-GYzBwgKYv17H0bM"}

_________________TOKEN___________________

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJBVURJRU5DRSIsImV4cCI6MTYxODQwODE4OSwiaWF0IjoxNTg4NDA4MTg5LCJpc3MiOiJJU1NVRVIiLCJqdGkiOiJjMEJSV3E1eFdmcVFhOGVYOFZISVdRIiwibmJmIjoxNTg4NDA4MTg5LCJwZXJtaXNzaW9uIjoicmVhZCIsInJvbGUiOiJ1c2VyIiwic3ViIjoiU1VCSkVDVCJ9.bHKmtgb8FzNCRvFNKzgyEDMU-DTgkK7_yhoDWqLFSRmIFWhyAi6sI2DYP3EtKNhcO6tt6GviBpCncdJLr_64Q6EZEaWxf4ohkxhHtc8vEJVyZd37gR47qL4HEw8BAsmKz5H_nTV5YP0WjbuhKNX3AkMLDdFI8nfR7AFXd1eECzTRxEYt6nv62fMXQwwvAUr6IBTIYe7j20nRwhopTo3Kwo6PKqNjGE6yb3HKbhJAcHdCorYTuH8WZISWwe91A7LyRqLiKIo4MJbwYxRkFOyJf--CtYrX7QXze-WY3I-qt3jBaf5qVmzzJqU2h5MthobukI68e0HT8ROdREXPbFp6XA

_________________TOKEN INFO___________________

{'alg': 'RS256', 'typ': 'JWT'}
{'aud': 'AUDIENCE', 'exp': 1618408189, 'iat': 1588408189, 'iss': 'ISSUER', 'jti': 'c0BRWq5xWfqQa8eX8VHIWQ', 'nbf': 1588408189, 'permission': 'read', 'role': 'user', 'sub': 'SUBJECT'}

"""
