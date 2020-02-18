"""

install pillow and requests module with command : pip3 install pillow requests

run this file in command line argument with command : python3 problem2.py {{image_url/path_to_csv_file}}

it will create a new JSON file as output in the same folder, where this file is located

I wrote this code in mac.So i'm not sure how it will work with windows or any other OS.
In case you are using Windows or any other OS, please try to analyze my code.

"""


import sys
import requests
from time import time
from multiprocessing.pool import ThreadPool
import csv
from PIL import Image
from io import BytesIO
import base64
import json

client_id = '6dbd8c8e16595f4'
client_secret = 'bdafc3f3b753ed3f8ff65e84646281520cbbe6ca'
refresh_token = 'bdca98c8431b1518a131412cf2e97cc5b7e2dbdf'
access_token = 'e560b17d5976785009a342bac71a9ffeb40bf905'
account_id = '124054135'
user_name = 'gautamBharfa'
url_header = 'Client-ID {}'
imgur_url = 'https://api.imgur.com/3/upload'


def fetch_image(url):
    """ function to fetch a image and return it in Json format """
    url = url[0]
    json_dict = {'image_url': url}
    status = 'Success'
    try:
        # fetching the image from url
        image_file = requests.get(url, stream=True).content
        # check if given url returns a image file or not
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        url_headers = requests.head(url)
        if url_headers.headers["content-type"] not in image_formats:
            status = 'URL does not lead to image file'
            json_dict['status'] = status
            return json_dict

        # opening the image to get its size, resolution
        binary_img_file = BytesIO(image_file)
        proccessed_image_file = Image.open(binary_img_file)
        size = proccessed_image_file.size
        width, height = size
        image_file_size = proccessed_image_file.tell()

        # resizing the image to given constraints
        resize_to = (320, 568)
        resized_image_file = proccessed_image_file.resize(resize_to)
        # encoding the image file to base64 binary array format
        original_image64 = base64.b64encode(image_file)
        # saving the resized image file into a variable
        buf = BytesIO()
        resized_image_file.save(buf, format='JPEG')
        resized_image_byte_array = buf.getvalue()
        # encoding the resized image file to base64 binary array format
        resized_image64 = base64.b64encode(resized_image_byte_array)

        json_dict['original_image64'] = repr(original_image64)
        json_dict['resized_image64'] = repr(resized_image64)
        json_dict['size'] = image_file_size
        json_dict['resolution'] = 'resolution of image ({}x{})'.format(width, height)

        # uploading the image to IMGUR API
        imgur_post_request = requests.post(imgur_url,
                                           data={'image': image_file},
                                           headers={'Authorization': url_header.format(client_id)})
        # uncomment below two lines to see response of post request

        # if imgur_post_request.status_code == 200:
        #     print(imgur_post_request.json())

    except Exception as e:
        # if exception is raised, then update status
        if isinstance(e, requests.exceptions.InvalidSchema) or isinstance(e, requests.exceptions.InvalidURL):
            status = 'error - unable to open image'
        elif isinstance(e, requests.exceptions.TooManyRedirects):
            status = 'error - too many redirects'
        elif isinstance(e, requests.exceptions.URLRequired):
            status = 'error - A valid URL is required to make a request'
        elif isinstance(e, requests.exceptions.ConnectionError):
            status = 'error - connection error'
        elif isinstance(e, requests.exceptions.ChunkedEncodingError) or isinstance(e,
                                                                                   requests.exceptions.ContentDecodingError):
            status = 'error - 429 while downloading image'
        else:
            status = 'unknown error occurred.the error occured is \n{}\n'.format(e)

    json_dict['status'] = status
    return json_dict


if __name__ == '__main__':
    start = time()
    output_list = []

    if len(sys.argv) == 1:
        print("please enter one argument in command line")
        exit(0)
    elif len(sys.argv) > 2:
        print("you entered two command line argument, but this code only considers first argument")

    url = sys.argv[1]
    # check if given cammanf line argument is csv file or not
    csv_file = True if str.lower(sys.argv[1][-3:]) == 'csv' else False

    if not csv_file:
        # check if url leads to valid image or not
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        url_headers = requests.head(url)
        if url_headers.headers["content-type"] not in image_formats:
            print('please enter a valid url, either a image url or a csv file path')
            exit(0)
        output_list.append(fetch_image(url))
    else:
        try:
            with open(sys.argv[1], 'r') as csv_file:
                csv_contents = csv.reader(csv_file)
                print('Running.Please wait !!!')
                # creating a thread poll for multiproccessing
                for i in ThreadPool(9).imap_unordered(fetch_image, csv_contents):
                    output_list.append(i)

        except Exception as e:
            print("please enter valid csv file path or check your internet connection and try again")
            exit(0)
    # writing the json to a file
    with open('output_json.json', 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(output_list))

    print("total time taken == ", time() - start)
