"""
This script generates RSA public/private key pair using python.
And uses the Keys to Generate JWT Token.
The series of steps are listed below

1. Generate the Key
2. Generate the Public and Private Keys
3. Generate the Token using the Private Key from step 2
4. Validate the JWT Token using the Public key from step 2

"""


# ______________________________ Step 0 ______________________________________
# import python_jwt
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime

# ______________________________ Step 1 ______________________________________
# ______________________________ GENERATE KEY ______________________________________
# Generate the keys.
# The private key will be used to Generate the Token
# The 2048-bit is about the RSA key pair: 
# RSA keys are mathematical objects which include a big integer, and a "2048-bit key" is a key such that 
# the big integer is larger than 2^2047 but smaller than 2^2048.
key = jwk.JWK.generate(kty='RSA', size=2048)

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

# ______________________________ Step 2 ______________________________________
# ______________________________ GENERATE PUBLIC AND PRIVATE KEY ______________________________________
# Export the private and public key

private_key = key.export_private()
public_key = key.export_public()


# ______________________________ Step 3 ______________________________________
# ______________________________ GENERATE JWT TOKEN ______________________________________
# Generate the JWT Tokes using the Private Key
# Provide the payload and the Private Key. RS256 is the Hash used and last value is the expiration time.
# You can set the expiration time according to your need.
# To generate JWT Token, you need the private key as a JWK object
token = jwt.generate_jwt(payload, jwk.JWK.from_json(private_key), 'RS256', datetime.timedelta(minutes=50))



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

❯ python generate-keys-and-tokens-using-python.py

_________________PUBLIC___________________

{"e":"AQAB","kty":"RSA","n":"3LlzeRY6gbIVwGO7AxO1bN3-CgWwIpWOT8m485AzkOdhxgCWc2F-3OqAigDyyDMqXtH1ovCaZnEIf3ZkJin7Y_zC48TNQwlKnuM29CrTjnYR1c_w30ZT4PNIisEwLKuEX5uRHuIrKYBxwwVf4eqoFmtpZbrmwDPCA1ZMFox0v40q1m_SecCB286alE42Ohb6j0ZuntjO5rg2ZyQt3EmxEDPE2Iuh737gYhXLuFhTiYH5S_kFokX1Yv0RdUyiGcmaxXgGaF3iglnsOHv9209uwlzrcDAouOD7PYbLjCoqpWydVLyxcJGqjF5i7CK36q_SVmpGHbIsdOlZQLWNA97AgQ"}

_________________PRIVATE___________________

{"d":"Tf9-zcBMJn6-7wCPGnRBfVopJnOCHYaKBqn7IJ7JiiApzeVxRQ6j3P9FMv9Iy_RAuccqLU0m0qKI5Tn6A_575oZwfDqUamcDJoiWZ8wmfEY-4TadINliVLDD5ryEAJUPrxVzP92ecQkBqm_gxR2-DkYgtaFJX4wquDErrCAwNWvN_gyJNUluH77l0tzLAypQRG-_RYYAFqmtO_qc8V9V-vsO0bgrFzpeKaJ5_yG8Rf3qWylqCT4TXsarEmyy91awdVw4rq154pJa_tWXkgqGaDLrvXp31xfFw-ks5tkCbgmF9D7cNdmrTCMOhp6H2_IuvPj7h9E9cSKKJec_zHVc0Q","dp":"jKAqKCXjnub2gejWvadsiWxHBeN13SbJbL0oXStV-H482iEC0SqBugfT7H4i-NC4fJEif2GmTpFH17PS3c4sFBj7_r5RRvhxJT_Fw_vKScl-eKFP3uACTo2MY7F7gZ8KNLn8t5FFJFA19BMYGoRcxVMKbrcMWy0VIHQFqe6gQ-U","dq":"UzpJX6d_19J2ixG9olYrEzSBWoIt1g5Tq-AkRRMoBiThEIbi9veHQc5alLwlbe2oqoVDfj_k0rt_87GAFDyoljkuXyXE4zi2jHJF3gDix34Yi6aXKt-obheJjm1hVK_g58--aacSAr0EsIskq1xdhvCCLZDUl6ZwBp8Rof5PesE","e":"AQAB","kty":"RSA","n":"3LlzeRY6gbIVwGO7AxO1bN3-CgWwIpWOT8m485AzkOdhxgCWc2F-3OqAigDyyDMqXtH1ovCaZnEIf3ZkJin7Y_zC48TNQwlKnuM29CrTjnYR1c_w30ZT4PNIisEwLKuEX5uRHuIrKYBxwwVf4eqoFmtpZbrmwDPCA1ZMFox0v40q1m_SecCB286alE42Ohb6j0ZuntjO5rg2ZyQt3EmxEDPE2Iuh737gYhXLuFhTiYH5S_kFokX1Yv0RdUyiGcmaxXgGaF3iglnsOHv9209uwlzrcDAouOD7PYbLjCoqpWydVLyxcJGqjF5i7CK36q_SVmpGHbIsdOlZQLWNA97AgQ","p":"-3G0cditFFmFrlHR7yecKBik50HwLXWLe4mbmCAmeBBMDIdy0XGxENmtGN835ylHsKsVd3vIYKlY3qISC486jWLWUnJAVeR33U7MYF4xnUfZvX4pwRHMLfTcBJhIYVpJUiGTxCvd-6MffqfkjGsGOI77vqoCH_TwVKjCJxKoIfU","q":"4LlBlNmwAN47YBvEeQlsRS9Mmp20UPYlZvrwXGMHL45V8-7-Hv4f_jPwK3DVv7y8lam-5eD7TXYn_Hiy8JvlMtBKgicxii8veW1gh7_htm6z_qQPCNjiRonz6aD9Jyno9jgXjlFLMvQYx_jMbgnhqLvAMM06T0MTi2GgfxI9sN0","qi":"EcdpxgKF8f13ShXGoo49HC3BOA4eMXx64TRmeZ_1r_YxHKq5al4JNfX06VmhC2C6BCtbMmikoLpF7YWktbE50vH8xRoSa_nsl4HjTcobBM1jwUEAf_z86Ip1RMbPs77f1WB1OCtLgQ5JRlErL-hVnFzhQh4sj8TiA3Zr1qq8uAI"}

_________________TOKEN___________________

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJBVURJRU5DRSIsImV4cCI6MTU4ODQxMTIzMCwiaWF0IjoxNTg4NDA4MjMwLCJpc3MiOiJJU1NVRVIiLCJqdGkiOiJuUXljNnhyMHh3cFRKM0l5YkV3S0tBIiwibmJmIjoxNTg4NDA4MjMwLCJwZXJtaXNzaW9uIjoicmVhZCIsInJvbGUiOiJ1c2VyIiwic3ViIjoiU1VCSkVDVCJ9.Vh3HLkK1tPpHDNN_g1wVJmUUmdN-SImKSMmwBgCOlrinPvWA6ti-y1up5_ImcmTl1QlAUg1nrnGS-hdh7fVUpuhbZqstFBKibjkXVJm40m45qxcYsK957xvssACFyKjt--AslgFxhvHzZt24p1MKPitNNvcok0OZMRaZtzKxK6ZpSWXApDWPwxd_6_NmFFCUeJM3tsinGZ-YnHQdOou_IVk5Hs_agF4BJypy_7cYGg3SaC_rt7aUXpgPrL-EsBibi50zGxZTIJHcYhJVpvnvHR9LCi0rraYurt31Bv2T1s8gW6W_lNccsMgvIXlbc8nPlXsKFQhGDwzXHxdiJk31lw

_________________TOKEN INFO___________________

{'alg': 'RS256', 'typ': 'JWT'}
{'aud': 'AUDIENCE', 'exp': 1588411230, 'iat': 1588408230, 'iss': 'ISSUER', 'jti': 'nQyc6xr0xwpTJ3IybEwKKA', 'nbf': 1588408230, 'permission': 'read', 'role': 'user', 'sub': 'SUBJECT'}
"""


