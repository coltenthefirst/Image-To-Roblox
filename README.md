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
  <img alt="Images To Roblox Parts" src="https://i.postimg.cc/MGx8XrT6/Roblox-Logo-2022.jpg" width="422" height="422" style="max-width: 100%;">
  <br/>
  <br/>
</p>

<h1 align="center">
    <a href="https://github.com/coltenthefirst/image-to-roblox">
        <img alt="License Info" src="https://img.shields.io/badge/License-MIT-blue.svg">
    </a>
    <a href="https://github.com/coltenthefirst/image-to-roblox/releases">
        <img alt="Newest Release" src="https://img.shields.io/github/release/coltenthefirst/image-to-roblox.svg">
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

## Introduction

This repository contains the backend source code for the **Image To Parts** Roblox Game. This tool allows users to convert image URLs into parts within Roblox. Users are free to use the files provided in this repository for their own purposes.

## How It Works
Here’s a overview of the process:
1. Input an image URL and select a quality setting (such as mid, high, low, extra low).
2. The image URL and selected quality are sent to **Vercel**.
3. Vercel downloads the image and runs a Python script based on your selection.
4. A Lua script is generated and sent back to Roblox, where it is processed into parts that resemble the pixels of your image.

## Game Links
- [Image-To-Parts (Deleted)](https://www.roblox.com/games/78950815879906/Image-To-Parts)
- [Create Your Dreams (Online)](https://www.roblox.com/games/128560311364952/Create-Your-Dreams)


If both games are offline, you can download the place file here:

- Update 1:  [Google Drive Link](https://drive.google.com/file/d/1YdDMn-is_UD_VkbfgQKzQ3mzjJb5QZHY/view?usp=sharing).
- Update 2: Soon...


## Uploading Custom Images
For obtaining direct image urls, I recommended to use [Postimages.org](https://postimages.org/) to obtain a direct link. Other services can be used as long as they provide a direct link.

## Tested Image Services
- ✅ = Works
- ❌ = Does not work

- [Postimages.org](https://postimages.org/) ✅
- [imgbb.com](https://imgbb.com/) ✅
- [i.imghippo.com](https://i.imghippo.com) ✅
- [i.imgur.com](https://i.imgur.com) ❌
- [imgbox.com](https://imgbox.com/) ✅
- [snipboard.io](https://snipboard.io/) ✅
- [prnt.sc](https://prnt.sc/) ❌
- [lunapic.com](https://www7.lunapic.com/editor/?action=quick-upload) ✅
- [imagevenue.com](https://www.imagevenue.com/) ✅
- [pictr.com](https://pictr.com/upload) ✅

## FAQ

**Q: Do my uploaded images get logged?**  
**A:** Uploaded images are saved in a temporary file called "tmp."

**Q: Will I get banned for using exploit images?**  
**A:** No, you will not be banned. The project generates parts based on your image, not Roblox assets.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute the files in this repository, as long as you include the original license. For more details, see the [LICENSE](LICENSE) file.

## Contributing
Contributions are welcome. If you have suggestions or improvements, please open an issue or submit a pull request.
