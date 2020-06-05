from google_images_download import google_images_download as gid

def download(word):
    response = gid.googleimagesdownload()
    return response.download({"keywords":word, "limit":1, "no_directory":True, "no_numbering":True})
