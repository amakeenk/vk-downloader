#!/usr/bin/python3

# Author: Alexander Makeenkov <amakeenk@altlinux.org>

import argparse
import math
import os
import requests
import sys
import time
import vk


class vk_album_downloader():
    def __init__(self, token, app_id, url, outdir):
        self.token = token
        self.app_id = app_id
        self.url = url
        self.outdir_name = outdir
        self.vk_api_version = '5.30'
        self.owner_id = url.split('/')[-1].split('_')[0].replace('album', '')
        self.album_id = url.split('/')[-1].split('_')[1]

    def init_session(self):
        session = vk.Session(access_token=self.token)
        self.vk_api = vk.API(session, v=self.vk_api_version)

    def create_dirs(self):
        self.album_dir_name = f'{self.get_album_name()}'
        if not os.path.exists(self.outdir_name):
            os.mkdir(self.outdir_name)
        if not os.path.exists(f'{self.outdir_name}/{self.album_dir_name}'):
            self.full_output_path = f'{self.outdir_name}/{self.album_dir_name}'
        else:
            self.full_output_path = f'{self.outdir_name}/{self.album_dir_name}-{time.time()}'
        os.mkdir(self.full_output_path)

    def get_album_name(self):
        return self.vk_api.photos.getAlbums(owner_id=self.owner_id, album_ids=self.album_id)['items'][0]['title']

    def get_images_count(self):
        return self.vk_api.photos.getAlbums(owner_id=self.owner_id, album_ids=self.album_id)['items'][0]['size']

    def get_images(self, offset):
        return self.vk_api.photos.get(owner_id=self.owner_id, album_id=self.album_id, count=1000, offset=offset*1000)

    def download(self):
        images_count = self.get_images_count()
        counter = progress = 0
        for _ in range(math.ceil(images_count / 1000)):
            images = self.get_images(_)
            for image in images['items']:
                quality_list = []
                for key in image.keys():
                    if 'photo_' in key:
                        quality_list.append(int(key.split('_')[1]))
                best_quality = sorted(quality_list)[-1]
                counter += 1
                image_url = image[f'photo_{best_quality}']
                print(f'Downloading image {counter}/{images_count} with quality: {best_quality} [ progress: {progress}%]')
                response = requests.get(image_url)
                output_file = f'{self.full_output_path}/image_{counter}.jpg'
                try:
                    with open(output_file, 'wb') as file:
                        for data in response.iter_content(1024):
                            file.write(data)
                    progress = round(100/images_count*counter, 2)
                except requests.exceptions.RequestException as err:
                    print(f'Some error occured: {err.strerror}')


def main():
    args = argparse.ArgumentParser()
    args.add_argument('token', help='vk access token')
    args.add_argument('app_id', help='vk application id')
    args.add_argument('url', help='album url')
    args.add_argument('outdir', help='directory for downloading')
    args_list = args.parse_args()
    token, app_id, url, outdir = args_list.token, args_list.app_id, args_list.url, args_list.outdir
    downloader = vk_album_downloader(token, app_id, url, outdir)
    downloader.init_session()
    downloader.create_dirs()
    downloader.download()
    print(f'All done. Images dowloading to ./{downloader.full_output_path}')


if __name__ == '__main__':
    main()
