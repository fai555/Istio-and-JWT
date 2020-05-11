## Setup 
Clone the repo
  ```git clone https://github.com/fai555/Istio-and-JWT.git```


Setup a environment
  ```
  cd 
  virtualenv -p python3 env
  pip install -r requirements.txt
  ```

## Generate Public/Private Key Pair Using OpenSSL

```
chmod +x generate-pem-key-pairs.sh

./generate-pem-key-pairs.sh
```

## Generate JWT Using the Private Key Generated in Previous Step
```
python generate-token-using-pem-files.py
```

## Generate RSA Public/Private Key Pairs and JWT Using Python
```
python generate-keys-and-tokens-using-python.py
```

## Create a JWKS - JSON Web Key Set
You need your public key in JSON format to create JWKS. You will get the public keys in JSON format in the last 2 steps. Whichever you may choose to use.

An example public key is 

```
{"e":"AQAB","kty":"RSA","n":"3LlzeRY6gbIVwGO7AxO1bN3-CgWwIpWOT8m485AzkOdhxgCWc2F-3OqAigDyyDMqXtH1ovCaZnEIf3ZkJin7Y_zC48TNQwlKnuM29CrTjnYR1c_w30ZT4PNIisEwLKuEX5uRHuIrKYBxwwVf4eqoFmtpZbrmwDPCA1ZMFox0v40q1m_SecCB286alE42Ohb6j0ZuntjO5rg2ZyQt3EmxEDPE2Iuh737gYhXLuFhTiYH5S_kFokX1Yv0RdUyiGcmaxXgGaF3iglnsOHv9209uwlzrcDAouOD7PYbLjCoqpWydVLyxcJGqjF5i7CK36q_SVmpGHbIsdOlZQLWNA97AgQ"}
```

Then you need to encapsulate this key as an item in the following array. Like this.

```
{ "keys":[ 


{"e":"AQAB","kty":"RSA","n":"3LlzeRY6gbIVwGO7AxO1bN3-CgWwIpWOT8m485AzkOdhxgCWc2F-3OqAigDyyDMqXtH1ovCaZnEIf3ZkJin7Y_zC48TNQwlKnuM29CrTjnYR1c_w30ZT4PNIisEwLKuEX5uRHuIrKYBxwwVf4eqoFmtpZbrmwDPCA1ZMFox0v40q1m_SecCB286alE42Ohb6j0ZuntjO5rg2ZyQt3EmxEDPE2Iuh737gYhXLuFhTiYH5S_kFokX1Yv0RdUyiGcmaxXgGaF3iglnsOHv9209uwlzrcDAouOD7PYbLjCoqpWydVLyxcJGqjF5i7CK36q_SVmpGHbIsdOlZQLWNA97AgQ"}

]}
```

This is a valid JWKS.

## Create a JWKSURI - JSON Web Key Set URI
Put the JWKS created above in a publicly accessible place. I will be storing it in this public repo as a json file. The JWKS is stored in the ```json-web-key-set.json``` file. You can use the raw file URL from GitHub and use it in Istio.