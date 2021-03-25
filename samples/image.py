with open('photo.txt', 'rb') as text_file:
    bytestring = text_file.read()

with open('photo.jpg', 'wb') as image_file:
    image_file.write(bytestring)