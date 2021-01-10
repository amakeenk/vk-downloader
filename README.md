# Preconditions
1. Create standalone application on https://vk.com/editapp?act=create and get it's ID
2. Get access token for VK API on https://vkhost.github.io
3. Create file ~/.vk-downloader.conf
```
token = <token>
app_id = <id>
```

# Usage
```
$ ./vk_album_downloader.py <album_url> <outdir>
```
