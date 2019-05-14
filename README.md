
# AutoQuotes
This is a simple python script that allows you to create a post for Instagram that contains a quote that accompanies a randomly chosen background from Unspash.

### Instalation
1. Clone or Download this repo

 `git clone https://github.com/fermarval/AutoQuotes.git`
 
 2. Go to the directory
 
 `cd AutoQuotes`
 
 3. Install the dependencies
 
 `pip install -r requirements.txt`
 
 4. Duplicate and rename the file `config.example.json` to `config.json`
 
 5. Edit the file `config.json` with your data
 
 - `ig_username` : Instagram account user where the image will be uploaded
 - `ig_password` : The account password
 - `client_id`: Unspash application access key 
 - `client_secret`: Unspash application secret key
 - `redirect_uri` : Unsplash rediect uri (Default: "/")
 - `topic` : Topic for the query of images (Example: "Architecture") 
 - `index` : 0, Index of the quote (not edit, it is updated automatically) (Default: 0)
 - `timeout` : Time between upload photos in seconds (Example: 600)
 - `tags`: List of tags for the subject of the photo 
	 
### Run

Execute this command `python autoquotes.py <number of quotes>`. Example, for 1 upload quotes image:

`python autoquotes.py 1`

