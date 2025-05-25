# Twitch Category Hider

A simple Tampermonkey script to hide and restore Twitch categories on your Following → Live page.

![Screenshot](https://github.com/RSKCS2/Hide-Twitch-Categories/blob/main/hide_twitch_category.png)

## ✅ Features
- Hide any category with a gray ❌ button  
- Hidden categories are remembered  
- Restore them easily from a dropdown panel  
- Clean, Twitch-style UI  

## 🚀 Install
1. Install [Tampermonkey](https://tampermonkey.net)  
2. [Click here to install the script](https://yourgithub.io/twitch-category-hider/twitch-category-hider.user.js)  
3. Visit [Twitch Following → Live](https://www.twitch.tv/directory/following/live)  

## 💡 Notes
- Hidden categories are stored in localStorage  
- Works on desktop browsers (Chrome, Firefox, Edge)  

## 🛠 License
MIT — use it however you like

## 🐛 Issues?
Open one [here](https://github.com/yourname/twitch-category-hider/issues)

## 🔍 How It Works
- The script monitors the Twitch Following → Live page and hides any stream tiles that match blocked **categories** or **keywords in titles**.
- A ❌ button appears next to each category label. Clicking it adds that category to a hidden list and removes it from view.
- Hidden categories and keywords are stored in the browser’s `localStorage`, so your preferences stick between sessions.
- You can manage your hidden filters from a floating “Filters” panel, which includes add/remove options for both categories and keywords.
- You can also manually type a category name or keyword to hide.
- The script uses a `MutationObserver` to detect when Twitch dynamically loads new streams, so filtering keeps working even as the page updates.
- It only runs on the `/following` directory page and cleans itself up when you leave that view.
