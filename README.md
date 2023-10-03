# Stylez

Created a styles library with 600+ artists already included.

I hope the community enjoys and creates their own styles to share.

<img src="screenshots/Screenshot 2023-10-03 141019.png" alt="Alt text" title="Optional title">


#installation 
launch webui normally (make sure your up-to-date) goto Extensions > Install form url and Paste

https://github.com/javsezlol1/Stylez.git

in the URL for extension's git repository


#Usage

Stylez is installed into the extensions folder, and it uses some CSS and JS to remove the old styles.
the old styles will be replaced by this button

<img src="screenshots/Screenshot 2023-10-03 141150.png" alt="Alt text" title="Optional title">


Don’t worry though on first launch all your saved styles will be converted into individual JSON files.
This will allow you to use them with the library. Adding blank preview images to later be changed if desired.

#Features:

Keyword:
Any prompts containing the keyword: {prompt} will automatically take you current prompt and instert it in place of the {prompt}.

  Example:
  
  prompt:
      
      a red house
      
applying the style 3d model will result in: 

    professional 3d model a red house octane render, highly detailed, volumetric, dramatic lighting.

Auto Convert:
Auto convert all your styles in your csv to JSON files ready for use with the library.

Categories:
Any folder within \Stylez\styles will be considered a category on the Stylez UI for easy sorting.

Styles Editor:
used to create styles grabbing current prompts as well as last generated images.
allows deletion and overwriting of existing images.


#Uninstall:

unistall as you usually would you will also have to remove the Stylez.js in the WebUI 'Javascript' folder
