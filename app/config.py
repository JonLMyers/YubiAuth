
# Flask
DEBUG = True

# Change this when not testing >.> You know how.
SECRET_KEY = "I_Love_Puppies"
SECRET_KEY = "I_Love_Kitties"
SECURITY_PASSWORD_SALT = "I_Love_Candy"

# Database
# MONGODB_DB = ''
# MONGODB_HOST = ''
# MONGODB_PORT = 
# MONGODB_USER = ''
# MONGODB_PASSWORD = ''

# Database Mock
MONGODB_DB = 'authdb'
MONGODB_HOST = 'mongomock://localhost'
MONGODB_PORT = 27017
MONGODB_USER= 'yubi'
MONGODB_PASSWORD = 'key'

# ----- U2F ----- #
U2F_APPID = 'https://localhost:5000'

# Set to True to enable facets
U2F_FACETS_ENABLED = False
U2F_FACETS_LIST = [
    'https://localhost:5000'
]