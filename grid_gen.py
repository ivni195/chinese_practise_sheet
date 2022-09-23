from PIL import Image, ImageDraw, ImageFont
from argparse import ArgumentParser

def calc_padding(el_size, page_size):
    n = page_size // el_size # number of elements that fit
    pixels_left = page_size - (n * el_size)
    padding = pixels_left // (n-1) 
    return n, padding

def calc_shifted_bbox(im, dx, dy):
    x0, y0, x1, y1 = im.getbbox()
    return x0 + dx, y0 + dy, x1 + dx, y1 + dy

def calc_shifted_upper_left(im, dx, dy):
    x0, y0, x1, y1 = im.getbbox()
    sizex, sizey = x1 - x0, y1 - y0
    return x0 + dx, y0 + dy


def create_sheet(kanji='', repeat_rows=2, margin_size=50):
	if len(kanji) != 4:
		raise Exception("You must provide exactly 4 characters.")

	a4x = 2480
	a4y = 3508 # 300 dpi

	x_margin = margin_size
	y_margin = margin_size

	font = ImageFont.truetype("kaiti.ttf", size=540)

	a4 = Image.new('RGB',
	                 (a4x, a4y), 
	                 (255, 255, 255))  # White
	grid_el = Image.open("single_grid.png")

	*_, gridx, gridy = grid_el.getbbox()

	available_x = a4x - 2 *x_margin
	available_y = a4y - 2 *y_margin

	nx, paddingx = calc_padding(gridx, available_x)
	ny, paddingy = calc_padding(gridy, available_y)

	xpos = x_margin
	ypos = y_margin

	draw = ImageDraw.Draw(a4)
	draw.text((0,0), 'a', font=font)
	for y in range(ny):
	    xpos = x_margin
	    for x in range(nx):
	        a4.paste(grid_el, calc_shifted_bbox(grid_el, xpos, ypos))
	        if y < repeat_rows:
	        	draw.text(calc_shifted_upper_left(grid_el, xpos, ypos), kanji[x], font=font, fill='grey')
	        xpos += gridx + paddingx
	    ypos += gridy + paddingy

	a4.save('practise_sheet.pdf')


if __name__ == '__main__':
	parser = ArgumentParser(description='Create custom practice sheets for chinese/japanese calligraphy.')
	parser.add_argument('kanji', type=str, help='The chinese characters (without spaces between).')
	parser.add_argument('--repeat-rows', '-n', type=int, default='2', help='Number of rows of traceable characters.')
	parser.add_argument('--margin-size', '-msize', type=int, default='50', help='Number of rows of traceable characters.')
	args = parser.parse_args()
	create_sheet(**args.__dict__)
	
	