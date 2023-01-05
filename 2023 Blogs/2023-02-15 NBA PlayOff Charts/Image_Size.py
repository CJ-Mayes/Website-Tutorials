from PIL import Image

foo = Image.open('Original/Miami_Heat.png')  # Large Image
foo.size  # (1200, 1656)
# downsize the image with an ANTIALIAS filter (gives the highest quality)
foo = foo.resize((300, 414), Image.ANTIALIAS)

foo.save('Scaled/Miami_Heat.png', quality=2)  # Reduced Quality
