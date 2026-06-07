from database import *

initialize_database()

save_message("user", "Hello")
save_message("assistant", "Hi there")

print(load_messages())