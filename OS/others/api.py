import random
import string

# Define the length of the random string
length = 100

# Generate the random string
rand_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Print the random string
print(rand_string)
