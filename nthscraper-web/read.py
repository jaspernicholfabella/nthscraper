import yaml

with open("config.yml", "r") as file:
    prime_service = yaml.safe_load(file)

print(prime_service)

print(prime_service["rest"]["url"])
print(prime_service["rest"]["port"])

print(prime_service["prime_numbers"], type(prime_service["prime_numbers"]))
