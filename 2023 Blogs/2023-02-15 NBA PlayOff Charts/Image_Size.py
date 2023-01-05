from PIL import Image

foo = Image.open('Original/Boston_Celtics.png')  # Large Image
foo.size  # (815, 905)

# downsize the image with an ANTIALIAS filter (gives the highest quality)
foo = foo.resize((815, 905), Image.ANTIALIAS)

foo.save('Scaled/Boston_Celtics.png', quality=95)  # Reduced Quality
