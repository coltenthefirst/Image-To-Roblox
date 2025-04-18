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

## I won't update this for awhile as I work on other projects. Thank you.

<p align="center">
  <img alt="asset" src="https://cdn.vectorstock.com/i/500p/16/54/checkerboard-black-and-white-background-vector-33401654.jpg" width="5000" height="10" style="max-width: 100%;">
  <br/>
  <br/>
</p>

<p align="center">
  <img alt="Images To Roblox Parts" src="https://github.com/user-attachments/assets/bfbaa477-8f75-42a6-97f1-69c2eee7f50b" width="422" height="422" style="max-width: 100%;">
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
    </a>
        <a href="https://vercel.com/">
        <img alt="Vercel Deploy Status" src="https://deploy-badge.vercel.app/?url=https%3A%2F%2Fvercel.com%2Fcoltenthefirsts-projects%2Fimage-to-roblox&logo=Vercel&name=Vercel+%28image-to-roblox%29">
    </a>
        <img src="https://img.shields.io/github/languages/top/coltenthefirst/image-to-roblox?color=%23000000">
    <img src="https://img.shields.io/github/stars/coltenthefirst/image-to-roblox?color=%23000000&logoColor=%23000000">
    <br>
    <img src="https://img.shields.io/github/commit-activity/w/coltenthefirst/image-to-roblox?color=%23000000"> 
    <img src="https://img.shields.io/github/last-commit/coltenthefirst/image-to-roblox?color=%23000000&logoColor=%23000000">
</h1>

<p align="center">
  <img alt="asset" src="https://cdn.vectorstock.com/i/500p/16/54/checkerboard-black-and-white-background-vector-33401654.jpg" width="5000" height="10" style="max-width: 100%;">
  <br/>
  <br/>
</p>

<h1 align="center">
    Images To Roblox Parts (Current: Model-3.5/Model-1G)
</h1>

<h6 align="center">
    ~ Made with Lua, Python, Flask, and Vercel! ~
</h6>

<h6 align="center">
    Python Version: 3.12
</h6>

<h6 align="center">
    Vercel Plan: Hobby (100% Free Plan)
</h6>

<h6 align="center">
    Repository Size: 36.51 KB
</h6>

<br>

<p align="center">
  <img alt="asset" src="https://cdn.vectorstock.com/i/500p/16/54/checkerboard-black-and-white-background-vector-33401654.jpg" width="5000" height="10" style="max-width: 100%;">
  <br/>
  <br/>
</p>

***

<p align="center">
  <img alt="Powered With Vercel" src="https://img.shields.io/badge/Powered%20With%20Vercel-%23000000?style=plastic&logo=vercel&logoColor=white" width="300" />
</p>

***

> [!WARNING]
> This project is AGAINST the Terms of Services of Roblox! Usage is on YOUR risk. This doesn't have a filter so nsfw material can be generated.

> [!WARNING]
> Sometimes this can go down and stop working due to me updating and testing new features in the source code. This doesn't happen as often, but its worth knowing.

> [!IMPORTANT]  
> Model-4 might be the last ever Model I will do for this project. Besides bug fix updates and the GUI Version.

> [!IMPORTANT]  
> I recommend always updating to the latest Model for Security fixes!

##### What makes this special from all the other image to roblox tools?
##### With this you don't have to run anything on your computer! All you need to do is join the Roblox game or download the place file and insert a image url or a gif url. Just wait and you will see your gif or your image! This doesn't have a filter so nsfw material can be generated. This doesn't use Roblox's image API either! So you don't need ID verification!

### If you use Model-2. Please read this: [fix](https://github.com/coltenthefirst/image-to-roblox/issues/5)

***
## I would highly love to credit Netpex, Dallin, and 3xq for the original scripts!
https://devforum.roblox.com/t/converting-image-to-parts-python/2713248 **(Original Python Script Without Flask)**

https://github.com/3xq/image_bypasser **(Original Python Script Without Flask)**

https://discordlookup.com/user/915329055174307850 **(Original Flask Scripts - My Best Friend btw)**

**I just maintain this project and I work on the Roblox code. Dallin made the original scripts that worked on your local computer and connected to my Roblox code with http in Roblox Studio.**
***

## Introduction

This repository contains the backend source code for the **Image To Parts** Roblox Game. This tool allows users to convert image URLs into parts within Roblox. Users are free to use the files provided in this repository for their own purposes.

## How It Works


<p align="center">
  <img alt="Images To Roblox Parts" src="https://github.com/user-attachments/assets/9b33af71-d1ed-48ff-b5c4-26e5650dab77" width="733" height="422" style="max-width: 100%;">
  <br/>
  <br/>
</p>

Here’s a overview of the process:
1. Input an image URL and select a quality setting (such as mid, high, low, extra low).
2. The image URL and selected quality are sent to **Vercel**.
3. Vercel downloads the image and runs a Python script based on your selection.
4. A Lua script is generated and sent back to Roblox, where it is processed into parts that resemble the pixels of your image.

## Cloning Vercel and GitHub

#### Make sure you create a GitHub account and go to [Vercel](https://vercel.com) to create a Vercel account by connecting your GitHub account to Vercel.
#### Click This:
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fcoltenthefirst%2Fimage-to-roblox&env=FLASK_APP&envValue=server.py&env=FLASK_ENV&envValue=development&project-name=image-to-roblox&repository-name=image-to-roblox)

### Tutorial Video: [Vercel Setup Tutorial YouTube Link](https://youtu.be/RcwPO3fshEU)

#

##### Set "FLASK_APP" to "server.py"
##### Set "FLASK_ENV" to "development"
##### Once it's deployed, go to the settings tab of your Vercel project, click on **General**, and then click on **Project Settings**.
#### Overwrite the **Build Command** as:  
`flask run --host=0.0.0.0 --port=5000`
#### Overwrite the **Install Command** as:  
`pip install -r requirements.txt`
##### You can go back to the **Project** page and click on the thumbnail preview that says "Not Found", don't worry, this is normal. Once you are on the site, click on the spacing where the URL ends and type `/send_image`. It should look like:  
`https://your-vercel-project-name.vercel.app/send_image`

***

#### MODEL-2 AND BELOW
##### Go to your copied Roblox game, open **ServerScriptService**, and open the script **ImageRequestHandler**. Replace the line:  
`local url = "https://image-to-roblox.vercel.app/send_image"`  
with your URL, like:  
`local url = "https://your-vercel-project-name.vercel.app/send_image"`

***

#### MODEL-3 AND HIGHER
##### Go to your copied Roblox game, open **ServerScriptService**, and open the module script **ServerlessWebsites**. Replace the line:  
`Urls.Image = "https://image-to-roblox.vercel.app/send_image"`  
with your URL, like:  
`Urls.Image = "https://your-vercel-project-name.vercel.app/send_image"`

##### You can also replace:  
`Urls.Gif = "https://image-to-roblox.vercel.app/send_gif"`  
with:  
`Urls.Gif = "https://your-vercel-project-name.vercel.app/send_gif"`

***

#### API Key for the GIF File Processor (Model-3.5)
##### Go to [ImgBB](https://api.imgbb.com/) and create an account. After creating an account, go back to [ImgBB](https://api.imgbb.com/) and generate an API key.  
##### Copy that API key and go to your copied Roblox game, open **ServerScriptService**, and then open the module script **ServerlessWebsites**. Replace the line:  
`Urls.GifAPIkey = "whatever is here"`  
with your API key, like:  
`Urls.GifAPIkey = "YourAPIKey"`

***

### Now you're done! You can visit your GitHub profile to find the cloned repository, and edit it however you like <3.

#

## To-Do List

<h6 style="text-align: right;">
    ~ EXPECT THESE TO CHANGE!!! ~
</h6>

### Current Tasks (NOT IN ORDER) - Model-3.8/Model-4 Planned
- [ ] Better UI (Model-3.8)
- [ ] Add More Image Options for the Cilent-Side (Model-3.8)
- [ ] Image/Gif Placement System - ***if its possible*** (Model-4)
- [ ] Slow or Quick Image Generating Options for Low End Devices. (Model-3.8)
- [ ] I will add more to this list soon. I have a lot planned for these 2 models but I somehow forget 💀

### Completed Tasks

- [x] Release (Github/Model-1)
- [x] Frame By Frame Animation Player (Model-2)
- [x] Faster Image Gen Speed (Model-2)
- [x] Enhanced image data privacy (Github)
- [x] Improved support for black and white images and single-color images (Github)
- [x] Add a frame-by-frame animation player (Model-2)
- [x] Add a delete button for parts (Model-2)
- [x] Fix Error 500 (Github/Model-2)
- [x] Resolve issue with the first pixel not generating (Model-2)
- [x] Updated README.md (Github)
- [x] Automatic Frame By Frame Animation Player (Github/Model-3)
- [x] Making A Logo (Github)
- [x] Color Filters (Model-3)
- [x] More Customizable Image Options (Model-3)
- [x] Fix The Frame By Frame Animation Player Bug (Model-3)
- [x] Fix Other Bugs (Github/Model-3)
- [x] Updated README.md #2 (Github)
- [x] Boring Website (Other)
- [x] Fix vulnerabilitys (Model-3.5)
- [x] Fix Part deletion for the Server-Side (Model-3.5)
- [x] Cut off Part generation on the Server-Side (Model-3.5)
- [x] Working Testing GUI Verison Model (Other) - Unreleased Dev Build
- [x] Full GUI Model (Model-1G)
- [x] HUGE SECURITY UPDATE (Github)
- [x] Update The README.md for Model-3.5 stuff (Github)
- [x] Clean Up Source Code (Github)

### Completed Tasks Since Model-3.5/Model-1G Released

- [x] Update The Website (Other)


## Videos
| Info                            | Video |
|------------------------------------|--------|
| Model-1 Release: |[Model-1 YouTube Link](https://www.youtube.com/watch?v=oFm_znA53r8)|
| Model-2 Release: |[Model-2 YouTube Link](https://www.youtube.com/watch?v=6pRmz4_hoDo)|
| Vercel Setup Tutorial: |[Vercel Setup Tutorial YouTube Link](https://youtu.be/RcwPO3fshEU)|

## Game Link
| Name                            | Link |
|------------------------------------|--------|
| Img To Rbx (Demo): |[Img To Rbx Demo Roblox Link](https://www.roblox.com/games/131711989085615/Img-To-Rbx-Demo)|
| Img To Roblox - GUI Version (Demo): |[Img To Roblox - GUI Version (Demo) Roblox Link](https://www.roblox.com/games/99939943838127/Img-To-Roblox-GUI-Version-Demo)|

<!--
| Create Your Dreams: |[Create Your Dreams Roblox Link](https://www.roblox.com/games/128560311364952/Create-Your-Dreams) OUTDATED|
-->

You can download the place files here:

| Model / Update                            | Download |
|------------------------------------|--------|
| Update 1/Model-1: |[Google Drive Link](https://drive.google.com/file/d/1YdDMn-is_UD_VkbfgQKzQ3mzjJb5QZHY/view?usp=sharing)|
| Update 2/Model-2: |[Google Drive Link](https://drive.google.com/file/d/1GUnPJWO0sX8VsMysFi1eTUbYXyJKcshk/view?usp=sharing)|
| Update 3/Model-3 - (⚠️ DO NOT USE! ⚠️): |[Google Drive Link](https://drive.google.com/file/d/17ZLL6-GvSCIvHV76Q4nytUkpEa8sWtXW/view?usp=sharing)|
| Update 4/Model-3.5: |[Google Drive Link](https://drive.google.com/file/d/1YXN_ACZsuZWUorV84D2IoJtSqGu3a7w1/view?usp=sharing)|
| | |
| Update 1/Model-1G: |[Google Drive Link](https://drive.google.com/file/d/1Yga1RLW9s6LPJNklf5HJWv4d5AnU_YqU/view?usp=sharing)|


## Uploading Custom Images
For obtaining direct image urls, I recommended to use [Postimages.org](https://postimages.org/) to obtain a direct link. Other services can be used as long as they provide a direct link.

## Tested Image Services
### ✅ Recommended (Works)
#### Free, No Account Needed:
- **[Postimages.org](https://postimages.org/)** — *Highly recommended*. Supports GIF uploads.
- **[imgbb.com](https://imgbb.com/)** — *Highly recommended*. Supports GIF uploads. **(API Key Provider For /send_gif)**
- [imghippo.com](https://imghippo.com/) — Supports GIF uploads. **(API Key Service Provider)**
- [softgateon.herokuapp.com/directlink/](http://softgateon.herokuapp.com/directlink/) — Supports GIF uploads. **(For Google Drive Files)**
- [imgbox.com](https://imgbox.com/) — Supports GIF uploads.
- [lunapic.com](https://www7.lunapic.com/editor/?action=quick-upload) — Supports GIF uploads.
- [imagevenue.com](https://www.imagevenue.com/) — Supports GIF uploads.
- [pictr.com](https://pictr.com/upload) — Supports GIF uploads.
- [imagebam.com](https://www.imagebam.com/) — Supports GIF uploads.
- [imgbly.com](https://imgbly.com/) — Supports GIF uploads.
- [picsur.org](https://picsur.org/upload) — Supports GIF uploads.
- [pixhost.to](https://pixhost.to/) — Supports GIF uploads.
- [catbox.moe](https://catbox.moe/) — Supports GIF uploads.
- [litterbox.catbox.moe](https://litterbox.catbox.moe/) — Supports GIF uploads.
- [endpot.com](https://i.endpot.com/) — Supports GIF uploads.
- [dc.missuo.ru](https://dc.missuo.ru/) — Supports GIF uploads.
- [gifyu.com](https://gifyu.com/) — Supports GIF uploads.
- [freeimage.host](https://freeimage.host/) — Supports GIF uploads.
- [imgcdn.dev](https://imgcdn.dev/) — Supports GIF uploads.

#### Free, But Limited Functionality:
- **[snipboard.io](https://snipboard.io/)** — Does *not* support GIF uploads.
- **[paste.pics](https://paste.pics/)** — Does *not* support GIF uploads.
- **[imghostr.com](https://imghostr.com/)** — Does *not* support GIF uploads.

### ❌ Not Recommended (Does Not Work)

- [imgur.com](https://imgur.com/) — Direct Links Are Broken
- [prnt.sc](https://prnt.sc/) — Direct Links Are Broken **(THE OWNER BANNED MY IP ADDRESS BECAUSE OF A BUG 😭)**
- [dropbox.com](https://www.dropbox.com/) — Direct Links Are Broken


## FAQ

**Q: Does this have a NSFW filter? (All Models and Github)**
######
**A:** No, this does NOT have a NSFW filter.

##### -

**Q: What happened to the NSFW filter version? (Other)**
######
**A:** The NSFW filter wasn't very good at detecting NSFW images or NSFW words in images. It was very buggy and was very messy to take care of. Sorry for shutting it down but, I couldn't keep working on it anymore. You can always make a fanmade NSFW Filter. Thank you. If you want the archive files then just download the repository: https://github.com/coltenthefirst/image-to-roblox-FILTERED. The place file still works along with the vercel server for it.

##### -

**Q: Do my uploaded images get logged? (All Models and Github)**
######
**A:** Uploaded images are temporary logged, they cannot be downloaded, viewed, or anything, unless its in Roblox.

##### -

**Q: Will I get banned for using exploit images? (Other)**
######
**A:** I said before that you won't be banned, but you can be banned. Please be careful when using this in your games.

##### -

**Q: Why does the game not process my chosen image hosting service? (Other)**
######
**A:** Either 1. The image hosting service you use is not on the allow list, or 2. The image hosting service's direct links don't work properly. Check this README for the allowed image hosting services. You can also make a issue so I could test out and add that image hoster to the allow list.

##### -

**Q: Why does the game have a website domain allow list? (Other/Github)**
######
**A:** The reason why it has a allow list is because of security. I don't want this vulnerable to attacks, and url links would be a easy attack.

##### -

**Q: Why is the animation player not working? (Model-2)**
######
**A:** Please read this: [fix](https://github.com/coltenthefirst/image-to-roblox/issues/5)

##### -

**Q: Why is the animation player not working? (Model-3 and Higher)**
######
**A:** Sometimes the api key can get rate limited and for it to work again, you would have to wait a hour. Or you can make another api key, delete the old one, and use the new one.

##### -

**Q: Why should I not use Model-3? (Model-3)**
######
**A:** The way I stored the API key for the gif processor, made the API key REALLY VULNERABLE and EASY for exploiters (aka **"hackers"**) to get ahold of. I recommend you use Model-3.5 since it solves Model-3's issues. Or a later Model.

##### -

**Q: How can I help on this project? (Other)**
######
**A:** You can star this project or, dm me on discord if you want to help another way: "unknowingly_exists"

##### -

***

<p align="center">
  <img alt="Project For Roblox" src="https://img.shields.io/badge/Project%20For%20Roblox-%2338B5E4?style=plastic&logo=roblox&logoColor=white" width="300" />
</p>

<p align="center">
  <img alt="Coded With Python" src="https://img.shields.io/badge/Coded%20With%20Python-%233B8D99?style=plastic&logo=python&logoColor=white" width="300" />
  <img alt="Coded With Lua" src="https://img.shields.io/badge/Coded%20With%20Lua-%232C2D72?style=plastic&logo=lua&logoColor=white" width="300" />
</p>

<p align="center">
  <img alt="Source Code Powered With GitHub" src="https://img.shields.io/badge/Source%20Code%20Powered%20By%20GitHub-%23121011?style=plastic&logo=github&logoColor=white" width="300" />
      <img alt="Powered With Flask" src="https://img.shields.io/badge/Powered%20With%20Flask-%23FF7F0E?style=plastic&logo=flask&logoColor=white" width="300" />
  <img alt="Powered With Vercel" src="https://img.shields.io/badge/Powered%20With%20Vercel-%23000000?style=plastic&logo=vercel&logoColor=white" width="300" />
</p>

***

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute the files in this repository, as long as you include the original license. For more details, see the [LICENSE](LICENSE) file.

## Contributing
Contributions are welcome. If you have suggestions or improvements, please open an issue or submit a pull request.
