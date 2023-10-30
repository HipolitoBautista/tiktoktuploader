from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend
from selenium.webdriver.chrome.options import Options
import json
import os

def upload(user, data):
  try: 
      # Path to the directory containing the videos
      directory_path = data["videos"]

      #Path to the captions for the specific video 
      with open(data["captions"], 'r') as captionFile:
        captions = json.load(captionFile)

      # Grab the first key in "captions" list, then get the first value of the first key
      first_caption_key = list(captions['captions'].keys())[0]
      first_caption_value = captions['captions'][first_caption_key] 

      # List all files in the directory
      all_files = os.listdir(directory_path)
      specific_path = directory_path+"/"+ all_files[1] 

      # Details of video we're about to uplaod
      videos = [
      {
      'path': specific_path, 
      'description': first_caption_value + " " + data["hashtag"]
      }
      ]

      # Options for the web browser
      options = Options()
      options.add_argument('start-maximized')

      # Authentication of the tiktok account
      auth = AuthBackend(cookies=data["cookies"])
      failed_videos = upload_videos(videos=videos, auth=auth, browser='chrome', options=options)

      #Check if video's have failed  
      for video in failed_videos: # each input video object which failed
        print("upload Failed")
        return

      if os.path.exists(directory_path):
        # Remove the video since it's already uploaded
        os.remove(specific_path)
        print(f"{specific_path} has been deleted!")

        # check if 'captions' is in captions and if it's a dict. If it is the description gets deleted
        if 'captions' in captions and isinstance(captions['captions'], dict) and captions['captions']:
            print(captions['captions'][first_caption_key])
            del captions['captions'][first_caption_key]

        #write captions to captionFile  
        with open(data["captions"], 'w') as captionFile:
            json.dump(captions, captionFile, indent=4)
            print("Caption has been deleted!")
      else: 
        print(f"No Failed Videos or Directory")

  # catch any exception
  except Exception as e:
      print(f"An error occurred: {e}")
      return


  
