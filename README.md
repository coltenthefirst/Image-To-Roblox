<!---
Copyright 2024 Colten Wade Parker. All rights reserved.

Licensed under the MIT License;
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://opensource.org/licenses/MIT

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->
<p align="center">
  <img alt="asset" src="https://cdn.vectorstock.com/i/500p/16/54/checkerboard-black-and-white-background-vector-33401654.jpg" width="5000" height="10" style="max-width: 100%;">
  <br/>
  <br/>
</p>

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fcoltenthefirst%2Fimage-to-roblox&env=FLASK_APP&envValue=server.py&env=FLASK_ENV&envValue=development&project-name=image-to-roblox&repository-name=image-to-roblox)

#### Make sure you make a github account and go to https://vercel.com and make a vercel account by connecting your github account to vercel.
##### Set "FLASK_APP" as "server.py"
##### Set "FLASK_ENV" as "development"
##### Once its deployed. Go to the settings tab of your vercel project, click on General and click on Project Settings.
#### Overwrite the Build Command as "flask run --host=0.0.0.0 --port=5000"
#### Overwrite the Install Command as "pip install -r requirements.txt"
##### You can go back to the Project page and click on the thumbnail preview that says "Not Found", don't worry, this is normal. Once you are on the site, click on the spacing where the url ends and type "/send_image". It should look like "https://your-vercel-project-name.vercel.app/send_image". You can go to your copyed Roblox game and open serverscriptservice and open the script "ImageRequestHandler". After that, replace the line "local url = "https://image-to-roblox.vercel.app/send_image"" as your url, like "local url = "https://your-vercel-project-name.vercel.app/send_image"".
### Now you're done! You can visit your github profile and you can find the cloned repo, you can edit this repo and do whatever you want with it.

<p align="center">
  <img alt="asset" src="https://cdn.vectorstock.com/i/500p/16/54/checkerboard-black-and-white-background-vector-33401654.jpg" width="5000" height="10" style="max-width: 100%;">
  <br/>
  <br/>
</p>

<p align="center">
  <img alt="Images To Roblox Parts" src="https://i.postimg.cc/mDfm6ydS/Untitled86-20241130213821.png" width="422" height="422" style="max-width: 100%;">
  <br/>
  <br/>
</p>

<h6 align="center">
    ~ Works For IOS, Android, Windows, Mac, and Console. ~
</h6>

<h1 align="center">
    <a href="https://github.com/coltenthefirst/image-to-roblox">
        <img alt="License Info" src="https://img.shields.io/badge/License-MIT-blue.svg">
    </a>
    <a href="https://github.com/coltenthefirst/image-to-roblox/releases">
        <img alt="Newest Release" src="https://img.shields.io/github/release/coltenthefirst/image-to-roblox.svg">
    </a>
    </a>
        <a href="https://vercel.com/">
        <img alt="Vercel Deploy Status" src="https://deploy-badge.vercel.app/?url=https%3A%2F%2Fvercel.com%2Fcoltenthefirsts-projects%2Fimage-to-roblox&logo=Vercel&name=Vercel+%28image-to-roblox%29">
    </a>
</h1>

<p align="center">
  <img alt="asset" src="https://cdn.vectorstock.com/i/500p/16/54/checkerboard-black-and-white-background-vector-33401654.jpg" width="5000" height="10" style="max-width: 100%;">
  <br/>
  <br/>
</p>

<h1 align="center">
    Images To Roblox Parts
</h1>

<br>

<p align="center">
  <img alt="asset" src="https://cdn.vectorstock.com/i/500p/16/54/checkerboard-black-and-white-background-vector-33401654.jpg" width="5000" height="10" style="max-width: 100%;">
  <br/>
  <br/>
</p>

# THERE IS A ISSUE WITH MODEL-2! PLEASE READ [fix](https://github.com/coltenthefirst/image-to-roblox/issues/5) TO FIX IT!

## Introduction

This repository contains the backend source code for the **Image To Parts** Roblox Game. This tool allows users to convert image URLs into parts within Roblox. Users are free to use the files provided in this repository for their own purposes.

## How It Works
Here’s a overview of the process:
1. Input an image URL and select a quality setting (such as mid, high, low, extra low).
2. The image URL and selected quality are sent to **Vercel**.
3. Vercel downloads the image and runs a Python script based on your selection.
4. A Lua script is generated and sent back to Roblox, where it is processed into parts that resemble the pixels of your image.

## To-Do List

<h6 style="text-align: right;">
    ~ EXPECT THESE TO CHANGE!!! ~
</h6>

### Current Tasks (IN ORDER) - Model-3 Planned

- [ ] NSFW Filter Model-3 (Github/Model-3F) - Last thing I will do is this.

### Completed Tasks

- [x] Frame By Frame Animation Player (Model-2)
- [x] Faster Image Gen Speed (Model-2)
- [x] Enhanced image data privacy (Github)
- [x] Improved support for black and white images and single-color images (Github)
- [x] Add a frame-by-frame animation player (Model-2)
- [x] Add a delete button for parts (Model-2)
- [x] Fix Error 500 (Github/Model-2)
- [x] Resolve issue with the first pixel not generating (Model-2)
- [x] Updated README.md (Github) - released

### Completed Tasks Since Model-2 Released

- [x] Automatic Frame By Frame Animation Player (Github/Model-3) - unreleased
###### ↑ Context: This will import the frames for you, and all you have to do is put in a gif url.
- [x] NSFW Filter (Github/Model-2F) - released
- [x] Making A Logo (Github) - released
- [x] Color Filters (Model-3) - unreleased
- [x] More Customizable Image Options (Model-3) - unreleased
- [x] Fix The Frame By Frame Animation Player Bug (Model-3) - unreleased
- [x] Fix Other Bugs (Github/Model-3) - unreleased
- [x] Updated README.md #2 (Github) - released

## Videos
| Info                            | Video |
|------------------------------------|--------|
| Model-1 Release: |[Model-1 YouTube Link](https://www.youtube.com/watch?v=oFm_znA53r8)|
| Model-2 Release: |[Model-2 YouTube Link](https://www.youtube.com/watch?v=6pRmz4_hoDo)|

## Game Link
| Name                            | Link |
|------------------------------------|--------|
| Create Your Dreams: |[Create Your Dreams Roblox Link](https://www.roblox.com/games/128560311364952/Create-Your-Dreams)|


You can download the place files here:

| Model / Update                            | Download |
|------------------------------------|--------|
| Update 1/Model-1: |[Google Drive Link](https://drive.google.com/file/d/1YdDMn-is_UD_VkbfgQKzQ3mzjJb5QZHY/view?usp=sharing)|
| Update 2/Model-2: |[Google Drive Link](https://drive.google.com/file/d/1GUnPJWO0sX8VsMysFi1eTUbYXyJKcshk/view?usp=sharing)|


## Uploading Custom Images
For obtaining direct image urls, I recommended to use [Postimages.org](https://postimages.org/) to obtain a direct link. Other services can be used as long as they provide a direct link.

## Tested Image Services
### ✅ Use (Works)
- [Postimages.org](https://postimages.org/)
- [imgbb.com](https://imgbb.com/)
- [imghippo.com](https://imghippo.com/)
- [imgbox.com](https://imgbox.com/)
- [snipboard.io](https://snipboard.io/)
- [lunapic.com](https://www7.lunapic.com/editor/?action=quick-upload)
- [imagevenue.com](https://www.imagevenue.com/)
- [pictr.com](https://pictr.com/upload)
- [imagebam.com](https://www.imagebam.com/)
- [imgbly.com](https://imgbly.com/)
- [picsur.org](https://picsur.org/upload)
- [pixhost.to](https://pixhost.to/)

### ❌ Do not use (Won't work)
- [i.imgur.com](https://i.imgur.com/)
- [prnt.sc](https://prnt.sc/)
- [freeimage.host](https://freeimage.host/)
- [dropbox.com](https://www.dropbox.com/)
- [imghostr.com](https://imghostr.com/)

## FAQ

**Q: Does this have a NSFW filter?**  
**A:** This version does NOT have a nsfw filter. If you want a filter use: [Image To Roblox Parts Filtered](https://github.com/coltenthefirst/image-to-roblox-FILTERED)

**Q: Do my uploaded images get logged?**  
**A:** Uploaded images are temporary logged, they cannot be downloaded, viewed, or anything, unless its in Roblox.

**Q: Will I get banned for using exploit images?**  
**A:** I said before that you won't be banned, but you can be banned. Please be careful when using this in your games.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute the files in this repository, as long as you include the original license. For more details, see the [LICENSE](LICENSE) file.

## Contributing
Contributions are welcome. If you have suggestions or improvements, please open an issue or submit a pull request.
