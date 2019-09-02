from icrawler.builtin import GoogleImageCrawler
import os
from PIL import Image
import shutil

# Extract images from Google Image
brands = ["Auchan","Carrefour","Decathlon","McDonald's"]

def extractFrames(inGif, outFolder):
    frame = Image.open(inGif)
    nframes = 0
    while frame:
        frame.save( '%s/%s-%s.jpg' % (outFolder, os.path.basename(inGif).split('.')[0], nframes ) , 'GIF')
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break;
    return True

# delete gifs and change location & name of images
def change_name_location(brand_file):
	for n, image_file in enumerate(os.scandir('./images/'+brand_file)):
		if 'gif' in image_file.name:
			#extractFrames('./images/'+brand_file+'/'+str(image_file),'./images/'+brand_file)
			os.remove(image_file.path)
		else:
			if not image_file.name.startswith('.'):
				shutil.move(image_file.path, './images/'+brand_file+'_'+image_file.name)	

if __name__ == '__main__':

	# Extract images from Google Image
	for b in brands:
		google_crawler = GoogleImageCrawler(storage={'root_dir': './images/'+b})
		google_crawler.crawl(keyword=b+' logo', max_num=50)
		google_crawler.crawl(keyword=b+' devanture', max_num=100)
		google_crawler.crawl(keyword=b+' facade du magasin', max_num=400)
		change_name_location(b)
				
