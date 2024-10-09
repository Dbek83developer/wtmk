import tkinter.filedialog
from tkinter import messagebox
from tkinter import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

IMAGE = ''


# ---------------------------- FUNCTIONS ------------------------------ #
def add_image():
    filename = tkinter.filedialog.askopenfilename()
    image_src_label.config(text=filename)
    global IMAGE
    IMAGE = filename


def watermark():
    print(IMAGE)
    content = content_entry.get()
    print(content)
    try:
        with Image.open(IMAGE).convert('RGBA') as base:

            txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
            font = ImageFont.truetype("arial.ttf", base.height/14, encoding="unic")
            d = ImageDraw.Draw(txt)

            watermark = ''
            for i in range(1, 200):
                watermark = (watermark + content + ' ' * 10)
                if i % 20 == 0:
                    watermark = watermark + '\n\n'

            d.text((0, 0), watermark, font=font, fill=(255, 255, 255, 100))

            w = txt.rotate(17.5)
            out_image = Image.alpha_composite(base, w)
            out_image.show()

            # saving the image
            filename = IMAGE[:IMAGE.find('.')] + '_wm.png'
            out_image.save(filename)

    except FileNotFoundError:
        messagebox.showwarning(title='Warning!', message='The image cannot be opened!')
    except PermissionError:
        messagebox.showwarning(title='Warning!', message='There is no image!')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Watermark Manager')
window.config(padx=50, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file='dbek-logo-black.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0, pady=(10, 20))

# Labels
content_label = Label(text='Content:   ')
content_label.grid(column=0, row=1)
image_label = Label(text='Image source:   ')
image_label.grid(column=0, row=2)

image_src_label = Label(text='There is no image')
image_src_label.grid(column=1, row=2, columnspan=2, pady=5, sticky=W)

# Entries
content_var = StringVar()
content_entry = Entry(width=53, textvariable=content_var)
content_entry.grid(column=1, row=1, columnspan=2, pady=5, sticky=W)
content_entry.insert(0, '@')
content_entry.focus()

# Buttons
add_image_button = Button(text='Add image', command=add_image)
add_image_button.grid(row=3, column=1, pady=5, sticky=W)

watermark_button = Button(text='Watermark!', command=watermark)
watermark_button.grid(row=3, column=2, pady=5)

window.mainloop()
