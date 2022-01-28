# native
import os
# external
import numpy
import matplotlib
from matplotlib import pyplot, image
from PIL import Image
import numpy as np

# COLOURS
# all colours are from the Tango colourmap, see:
# http://tango.freedesktop.org/Tango_Icon_Theme_Guidelines#Color_Palette
COLS = {	"butter": [	'#fce94f',
					'#edd400',
					'#c4a000'],
		"orange": [	'#fcaf3e',
					'#f57900',
					'#ce5c00'],
		"chocolate": [	'#e9b96e',
					'#c17d11',
					'#8f5902'],
		"chameleon": [	'#8ae234',
					'#73d216',
					'#4e9a06'],
		"skyblue": [	'#729fcf',
					'#3465a4',
					'#204a87'],
		"plum": 	[	'#ad7fa8',
					'#75507b',
					'#5c3566'],
		"scarletred":[	'#ef2929',
					'#cc0000',
					'#a40000'],
		"aluminium": [	'#eeeeec',
					'#d3d7cf',
					'#babdb6',
					'#888a85',
					'#555753',
					'#2e3436'],
		}

# # # # #
# FUNCTIONS NEW

def draw_fixations_new(fix, dispsize, imagefile=None, durationsize=True, durationcolour=True, alpha=0.5, savefilename=None):

	"""Draws circles on the fixation locations, optionally on top of an image,
	with optional weigthing of the duration for circle size and colour

	arguments

	fix				-	a list of fixation ending events from a single trial,
					as produced by edfreader.read_edf, e.g.
					edfdata[trialnr]['events']['Efix']
	dispsize		-	tuple or list indicating the size of the display,
					e.g. (1024,768)

	keyword arguments

	imagefile		-	full path to an image file over which the heatmap
					is to be laid, or None for no image; NOTE: the image
					may be smaller than the display size, the function
					assumes that the image was presented at the centre of
					the display (default = None)
	durationsize	-	Boolean indicating whether the fixation duration is
					to be taken into account as a weight for the circle
					size; longer duration = bigger (default = True)
	durationcolour	-	Boolean indicating whether the fixation duration is
					to be taken into account as a weight for the circle
					colour; longer duration = hotter (default = True)
	alpha		-	float between 0 and 1, indicating the transparancy of
					the heatmap, where 0 is completely transparant and 1
					is completely untransparant (default = 0.5)
	savefilename	-	full path to the file in which the heatmap should be
					saved, or None to not save the file (default = None)

	returns

	fig			-	a matplotlib.pyplot Figure instance, containing the
					fixations
	"""

	# IMAGE
	fig, ax = draw_display(dispsize, imagefile=imagefile)

	# CIRCLES
	# duration weigths
	if durationsize:
		siz = 100 * (fix['dur']/30.0)
	else:
		siz = 100 * numpy.median(fix['dur']/30.0)
	if durationcolour:
		col = fix['dur']
	else:
		col = COLS['chameleon'][2]
	# draw circles ( zorder=2 means that circles has to be in the background of lines )
	ax.scatter(fix['x'], fix['y'], s=siz, c=col, marker='o', cmap='jet', alpha=alpha, zorder=2 )
	# write number in the center of circle to recognise the order
	for i, txt in enumerate( range(0, len(fix['x']) )):
		# text has no zorder, it appears in the foreground
		ax.annotate(txt, xy= (fix['x'][i], fix['y'][i]), ha='center')
	# draw lines between circles ( zorder=1 means that lines has to be in the foreground of circles )
	pyplot.plot(fix['x'],fix['y'], lw=2, zorder=1)

    # invert the y axis, as (0,0) is top left on a display
	ax.invert_yaxis()

	# save the figure if a file name was provided  
	if savefilename != None:
		# manage string in order to get path
		filename = str(savefilename.split('\\')[-1])
		mid_dir_name = str(savefilename.replace(filename, ''))
		new_dir_name = mid_dir_name + '\\' + str(filename.split('_')[0]) + '_' + str(filename.split('_')[1])
		# if folder path doen't exist
		if not os.path.exists(new_dir_name):
			# create folder
			os.makedirs(new_dir_name)
		fig.savefig(new_dir_name + '\\' + filename)

		# save also in TOT to have a global vision of fixs images
		tot_dir_name = mid_dir_name + 'TOT'
		# if folder path doen't exist
		if not os.path.exists(tot_dir_name):
			# create folder
			os.makedirs(tot_dir_name)
		fig.savefig(tot_dir_name + '\\' + filename)
	
    # pyplot.show()
	return fig


# # # # #
# FUNCTIONS NEW

def draw_heatmap_new(fix, dispsize, imagefile=None, durationweight=True, alpha=0.5, savefilename=None):

	"""Draws a heatmap of the provided fixations, optionally drawn over an
	image, and optionally allocating more weight to fixations with a higher
	duration.

	arguments

	fix				-	a list of fixation ending events from a single trial,
					as produced by edfreader.read_edf, e.g.
					edfdata[trialnr]['events']['Efix']
	dispsize		-	tuple or list indicating the size of the display,
					e.g. (1024,768)

	keyword arguments

	imagefile		-	full path to an image file over which the heatmap
					is to be laid, or None for no image; NOTE: the image
					may be smaller than the display size, the function
					assumes that the image was presented at the centre of
					the display (default = None)
	durationweight	-	Boolean indicating whether the fixation duration is
					to be taken into account as a weight for the heatmap
					intensity; longer duration = hotter (default = True)
	alpha		-	float between 0 and 1, indicating the transparancy of
					the heatmap, where 0 is completely transparant and 1
					is completely untransparant (default = 0.5)
	savefilename	-	full path to the file in which the heatmap should be
					saved, or None to not save the file (default = None)

	returns

	fig			-	a matplotlib.pyplot Figure instance, containing the
					heatmap
	"""

	# IMAGE
	fig, ax = draw_display(dispsize, imagefile=imagefile)

	# Gaussian
	gwh = 200
	gsdwh = gwh/6
	gaus = gaussian(gwh,gsdwh)
	# matrix of zeroes
	strt = int(gwh/2)
	heatmapsize = int(dispsize[1] + 2*strt), int(dispsize[0] + 2*strt)
	# print(list(heatmapsize))
	heatmap = numpy.zeros(heatmapsize, dtype=float)
	# create heatmap
	for i in range(0,len(fix['dur'])):
		# get x and y coordinates
		x = int(strt + fix['x'][i] - int(gwh/2))
		y = int(strt + fix['y'][i] - int(gwh/2))
		# correct Gaussian size if either coordinate falls outside of
		# display boundaries
		if (not 0 < x < dispsize[0]) or (not 0 < y < dispsize[1]):
			hadj=[0,gwh];vadj=[0,gwh]
			if 0 > x:
				hadj[0] = abs(x)
				x = 0
			elif dispsize[0] < x:
				hadj[1] = int(gwh - int(x-dispsize[0]))
			if 0 > y:
				vadj[0] = abs(y)
				y = 0
			elif dispsize[1] < y:
				vadj[1] = int(gwh - int(y-dispsize[1]))
			# add adjusted Gaussian to the current heatmap
			try:
				heatmap[y:y+vadj[1],x:x+hadj[1]] += gaus[vadj[0]:vadj[1],hadj[0]:hadj[1]] * fix['dur'][i]
			except:
				# fixation was probably outside of display
				pass
		else:
			# add Gaussian to the current heatmap
			heatmap[y:y+gwh,x:x+gwh] += gaus * fix['dur'][i]
	# resize heatmap
	heatmap = heatmap[strt:dispsize[1]+strt,strt:dispsize[0]+strt]
	# remove zeros
	lowbound = numpy.mean(heatmap[heatmap>0])
	heatmap[heatmap<lowbound] = numpy.NaN
	# draw heatmap on top of image
	ax.imshow(heatmap, cmap='jet', alpha=alpha)

	# FINISH PLOT
	# invert the y axis, as (0,0) is top left on a display
	ax.invert_yaxis()
	# save the figure if a file name was provided

	# filename = str(savefilename.split('\\')[-1])
	# mid_dir_name = str(savefilename.replace(filename, ''))
	# new_dir_name = mid_dir_name + '\\' + str(filename.split('_')[0]) + '_' + str(filename.split('_')[1])
	# if not os.path.exists(new_dir_name):
	# 	os.makedirs(new_dir_name)
	# savefilename = new_dir_name + '\\' + filename
	# fig.savefig(savefilename)
	# fig.savefig(mid_dir_name + 'TOT\\' + filename)

	if savefilename != None:
		filename = str(savefilename.split('\\')[-1])
		mid_dir_name = str(savefilename.replace(filename, ''))
		new_dir_name = mid_dir_name + '\\' + str(filename.split('_')[0]) + '_' + str(filename.split('_')[1])
		if not os.path.exists(new_dir_name):
			os.makedirs(new_dir_name)
		savefilename = new_dir_name + '\\' + filename
		fig.savefig(savefilename)

		fig.savefig(mid_dir_name + 'TOT\\' + filename)
	# fig.show()
	# pyplot.waitforbuttonpress()
	return fig



# # # # #
# HELPER FUNCTIONS

def draw_display(dispsize, imagefile=None):

	"""Returns a matplotlib.pyplot Figure and its axes, with a size of
	dispsize, a black background colour, and optionally with an image drawn
	onto it

	arguments

	dispsize		-	tuple or list indicating the size of the display,
					e.g. (1024,768)

	keyword arguments

	imagefile		-	full path to an image file over which the heatmap
					is to be laid, or None for no image; NOTE: the image
					may be smaller than the display size, the function
					assumes that the image was presented at the centre of
					the display (default = None)

	returns
	fig, ax		-	matplotlib.pyplot Figure and its axes: field of zeros
					with a size of dispsize, and an image drawn onto it
					if an imagefile was passed
	"""

	# construct screen (black background)
	screen = numpy.zeros((dispsize[1],dispsize[0],3), dtype='float32')
	# if an image location has been passed, draw the image
	if imagefile != None:
		# check if the path to the image exists
		if not os.path.isfile(imagefile):
			raise Exception("ERROR in draw_display: imagefile not found at '%s'" % imagefile)

		Image.open(imagefile).convert('RGB').save(imagefile)
		# load image
		img = image.imread(imagefile)
		# flip image over the horizontal axis
		# (do not do so on Windows, as the image appears to be loaded with
		# the correct side up there; what's up with that? :/)
		if not os.name == 'nt':
			img = numpy.flipud(img)
		# width and height of the image
		w, h = int(len(img[0])), int(len(img))
		# print(w, h)
		# x and y position of the image on the display
		x = int(dispsize[0]/2 - w/2)
		y = int(dispsize[1]/2 - h/2)
		# draw the image on the screen
		# print(img)
		# print(screen[y:y+h,x:x+w,:])
		# screen[y:y+h,x:x+w,:] += img
		numpy.add(screen[y:y+h,x:x+w,:], img, out=screen[y:y+h,x:x+w,:] , casting="unsafe")
		# print(img)
		# print(screen[y:y+h,x:x+w,:])
		# print(numpy.array_equal(img, screen[y:y+h,x:x+w,:]))

	# dots per inch
	dpi = 100.0
	# determine the figure size in inches
	figsize = (dispsize[0]/dpi, dispsize[1]/dpi)
	# create a figure
	fig = pyplot.figure(figsize=figsize, dpi=dpi, frameon=True, clear=True) #, facecolor='w')
	ax = pyplot.Axes(fig, [0,0,1,1])
	ax.set_axis_off()
	fig.add_axes(ax)
	# plot display
	ax.axis([0,dispsize[0],0,dispsize[1]])
	ax.imshow(screen)#, origin='upper')

	return fig, ax


def gaussian(x, sx, y=None, sy=None):

	"""Returns an array of numpy arrays (a matrix) containing values between
	1 and 0 in a 2D Gaussian distribution

	arguments
	x		-- width in pixels
	sx		-- width standard deviation

	keyword argments
	y		-- height in pixels (default = x)
	sy		-- height standard deviation (default = sx)
	"""

	# square Gaussian if only x values are passed
	if y == None:
		y = x
	if sy == None:
		sy = sx
	# centers
	xo = x/2
	yo = y/2
	# matrix of zeros
	M = numpy.zeros([y,x],dtype=float)
	# gaussian matrix
	for i in range(x):
		for j in range(y):
			M[j,i] = numpy.exp(-1.0 * (((float(i)-xo)**2/(2*sx*sx)) + ((float(j)-yo)**2/(2*sy*sy)) ) )

	return M
