from PIL import Image, ImageDraw, ImageFont, ImageFilter
from InstagramAPI import InstagramAPI
from io import BytesIO
from unsplash.api import Api
from unsplash.auth import Auth

import string, requests, json, sys, time, os, random


def load_config():
	with open('config.json') as confFile:
		return json.load(confFile)


def createImg(data):
	print("Creating image...\n")
	#Image size
	x1 = 612
	y1 = 612
	size = 612,612

	#My quote
	sentence = '"' + data['quote'] + '"' + ' -' + data['author']

	#Font chosen
	font_name = random.choice(os.listdir("font/"))
	print "Font: ",font_name

	fnt = ImageFont.truetype('font/'+font_name, 42) #can change the size font here

	un_photo_id = api.photo.random(query=data['topic'])
	un_photo = api.photo.get(un_photo_id[0].id)

	data['un_user'] = un_photo.user.username #get unspash author user
	print(data['un_user'])

	url = un_photo.urls.regular

	response = requests.get(url)
	#img = Image.new('RGB', (x1, y1), color = (255, 255, 255)) #solid color background
	img = Image.open(BytesIO(response.content))

	width, height = img.size #get dimensions
	left = (width - height)/2
	right = (width - height)/2

	crop_rectangle = (0, 0, 612, 612)#making a square
	img = img.crop(crop_rectangle)

	img = img.filter(ImageFilter.GaussianBlur()) #blur filter
	img = img.point(lambda p: p * 0.4) #darker filter

	d = ImageDraw.Draw(img)

	#find the average size of the letter
	sum = 0
	for letter in sentence:
		sum += d.textsize(letter, font=fnt)[0]
	average_length_of_letter = sum/len(sentence)

	#find the number of letters to be put on each line
	number_of_letters_for_each_line = (x1/1.618)/average_length_of_letter
	incrementer = 0
	fresh_sentence = ''

	#add some line breaks
	for letter in sentence:
	    if(letter == '-'):
	        fresh_sentence += '\n\n' + letter
	    elif(incrementer < number_of_letters_for_each_line):
	        fresh_sentence += letter
	    else:
	        if(letter == ' '):
	            fresh_sentence += '\n'
	            incrementer = 0
	        else:
	            fresh_sentence += letter
	    incrementer+=1
	print (fresh_sentence)

	#render the text in the center of the box
	dim = d.textsize(fresh_sentence, font=fnt)
	x2 = dim[0]
	y2 = dim[1]
	qx = (x1/2 - x2/2)
	qy = (y1/2-y2/2)
	d.text((qx,qy), fresh_sentence ,align="center",  font=fnt, fill=(230,230,230))

	img.save('img/quote.jpg')

	ran_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
	img.save('img/quote-'+ran_str+'.jpg') #save a copy


def postQuote(data):
	print("Posting image...\n")
	#Path and caption of image given
	photo_path = 'img/quote.jpg'
	caption = '"' + data['quote'] + '"' + ' -' + data['author'] + ' '
	tags = config['tags']

	#Quote tags added as hashtags to caption
	for i in range(len(tags)):
		caption+=' #' + tags[i]
	caption+=' Photo: @'+ data['un_user']
	InstagramApi.uploadPhoto(photo_path, caption=caption)
	print("Image posted successfully!\n")

    #update index
	with open('config.json', 'r+') as f:
		data = json.load(f)
		data['index'] = data['index'] + 1 
		f.seek(0)   
		json.dump(data, f, indent=4)


#getQuote: Return the quote on index position  from json file
def getQuote():
	index = config['index']
	print("Reading quote number "+str(index)+"...\n")

	with open('quotes.json', 'r') as f:
		distros_dict = json.load(f)
	if(distros_dict['contents']['quotes'][index]):
		return distros_dict['contents']['quotes'][index]
	else:
		print("No more quotes!\n")

def main():
	i = 0
	if(len(sys.argv)>1):
		n = int(sys.argv[1])
	else:
		n = 999
	while i < n:
		print("Iteration number "+str(i)+"...")
		data = getQuote()
		createImg(data)
		postQuote(data)
		time.sleep(config['timeout']);
		i = i + 1
	print("End program\n")


####

config = load_config()
InstagramApi = InstagramAPI(config['ig_username'], config['ig_password'])
print("\nLogin on Instagram:")
print "IG Username:",config['ig_username']
InstagramApi.login()  # login

auth = Auth(config['client_id'], config['client_secret'], config['redirect_uri'], code=config['code'])
api = Api(auth)

main()
