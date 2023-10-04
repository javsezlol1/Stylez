onUiLoaded(setupStylez);
let orgPrompt = '';
let orgNegative = '';


function setupStylez() {
    //create new button (t2i)
    const t2i_StyleBtn = document.createElement("button");
    t2i_StyleBtn.setAttribute("class", "lg secondary gradio-button tool svelte-cmf5ev");
    t2i_StyleBtn.setAttribute("id", "t2i_stylez_btn");
    t2i_StyleBtn.setAttribute("onClick", "showHideStylez()");
    t2i_StyleBtn.innerText = `🖌️`;
    //add new button
    const txt2img_tools = gradioApp().getElementById("txt2img_clear_prompt");
    txt2img_tools.parentNode.appendChild(t2i_StyleBtn);
    //create new button (i2i)
    const i2i_StyleBtn = document.createElement("button");
    i2i_StyleBtn.setAttribute("class", "lg secondary gradio-button tool svelte-cmf5ev");
    i2i_StyleBtn.setAttribute("id", "i2i_stylez_btn");
    i2i_StyleBtn.setAttribute("onClick", "showHideStylez()");
    i2i_StyleBtn.innerText = `🖌️`;
    //add new button
    const img2img_tools = gradioApp().getElementById("img2img_clear_prompt");
    img2img_tools.parentNode.appendChild(i2i_StyleBtn);
    //remove old styles items
    const stylesOld_t2i = gradioApp().getElementById("txt2img_styles_row");
    stylesOld_t2i.parentNode.removeChild(stylesOld_t2i);
    const stylesOld_i2i = gradioApp().getElementById("img2img_styles_row");
    stylesOld_i2i.parentNode.removeChild(stylesOld_i2i);
    //Setup Browser
    const tab_t2i = gradioApp().getElementById("tab_txt2img");
    const tab_i2i = gradioApp().getElementById("tab_img2img");
    const t2i_stylez_container = tab_t2i.querySelector("#Stylez");
    const i2i_stylez_container = tab_i2i.querySelector("#Stylez");
    const tabs = gradioApp().getElementById("tabs");
    t2i_stylez_container.parentNode.removeChild(t2i_stylez_container);
    i2i_stylez_container.parentNode.removeChild(i2i_stylez_container);
    tabs.appendChild(t2i_stylez_container);
}

function showHideStylez() {
    const stylez = gradioApp().getElementById("Stylez");
    const computedStyle = window.getComputedStyle(stylez);
    if (computedStyle.getPropertyValue("display") === "none" || computedStyle.getPropertyValue("visibility") === "hidden") {
        stylez.style.display = "block";
    } else {
        stylez.style.display = "none";
    }
}
// get active tab
function getENActiveTab() {
    let activetab = "";
    const tab = gradioApp().getElementById("tab_txt2img");
    const computedStyle = window.getComputedStyle(tab);
    if (computedStyle.getPropertyValue("display") === "none" || computedStyle.getPropertyValue("visibility") === "hidden") {
        activetab = "img2img";
    } else {
        activetab = "txt2img";
    }
    return (activetab);
}

function tabCheck(mutationsList, observer) {
    for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
            const tabTxt2img = gradioApp().getElementById('tab_txt2img');
            const tabImg2img = gradioApp().getElementById('tab_img2img');
            const stylez = gradioApp().getElementById("Stylez");
            // Check if the display property of tab_txt2img is 'none'
            if (tabTxt2img.style.display === 'none') {
                stylez.style.display = "none";
            }
            // Check if the display property of tab_img2img is 'none'
            if (tabImg2img.style.display === 'none') {
                stylez.style.display = "none";
            }
        }
    }
}
//check to see if gradio is fully loaded
function checkElement() {
    const tabTxt2img = gradioApp().getElementById('tab_txt2img');
    if (tabTxt2img) {
        const observer = new MutationObserver(tabCheck);
        const tab_txt2img = gradioApp().getElementById('tab_txt2img');
        const tab_img2img = gradioApp().getElementById('tab_img2img');
        const config = {attributes: true};
        observer.observe(tab_txt2img, config);
        observer.observe(tab_img2img, config);
        const firstStyleCard = gradioApp().querySelector(".style_card");
        var styleCardHeight = window.getComputedStyle(firstStyleCard).height;
        var heightWithoutPx = parseInt(styleCardHeight, 10);
        const slider = gradioApp().querySelector("#card_thumb_size > div > div > input");
        applyValues(slider,heightWithoutPx)
        const style_savefolder_temp = gradioApp().querySelector("#style_savefolder_temp > label > textarea")
        console.log(style_savefolder_temp)
        applyValues(style_savefolder_temp,"Styles")
        gradioApp().getElementById('style_save_btn').addEventListener('click', () => {
            saveRefresh();
        });
        gradioApp().getElementById('style_delete_btn').addEventListener('click', () => {
            deleteRefresh();
        });
    } else {
        setTimeout(checkElement, 100);
    }
}
checkElement();
//apply styles
function applyStyle(prompt, negative) {
    const tabname = getENActiveTab();
    const applyStylePrompt = gradioApp().querySelector('#styles_apply_prompt > label > input');
    if (applyStylePrompt.checked === true) {
        const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
        if (prompt.includes("{prompt} .")) {
            orgPrompt = promptPos.value;
            prompt = prompt.replace('{prompt} .',", "+ orgPrompt+", ");
            promptPos.value = prompt;
            updateInput(promptPos);
        } else {
            if (orgPrompt === '') {
                orgPrompt = prompt;
            } else {
                orgPrompt += `,${prompt}`;
            }
            applyPrompts(promptPos, prompt);
        }
    }
    const applyStyleNeg = gradioApp().querySelector('#styles_apply_neg > label > input');
    if (applyStyleNeg.checked === true) {
        const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
        if (negative !== '') {
            if (orgNegative === '') {
                orgNegative = negative;
            } else {
                orgNegative += `,${negative}`;
            }
            applyPrompts(promptNeg, negative);
        }
    }
}

function applyPrompts(a, b) {
    if (a.value === '') {
        a.value = b;
    } else {
        a.value = `${a.value},${b}`;
    }
    updateInput(a);
}
function applyValues(a, b) {
    a.value = b;
    updateInput(a);
}

function hoverPreviewStyle(prompt, negative) {
    const enablePreviewChk = gradioApp().querySelector('#HoverOverStyle_preview > label > input');
    const enablePreview = enablePreviewChk.checked;
    if (enablePreview === true) {
      const tabname = getENActiveTab();
      const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
      const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
      orgPrompt = promptPos.value;
      orgNegative = promptNeg.value;
      const previewPrompt = `${promptPos.value},${prompt}`;
      const previewNegative = `${promptNeg.value},${negative}`;
      const applyStylePrompt = gradioApp().querySelector('#styles_apply_prompt > label > input');
      if (applyStylePrompt.checked === true) {
        if (prompt !== '') {
          if (prompt.includes('{prompt}')) {
            prompt = prompt.replace('{prompt} .',", " + orgPrompt + ", ");
            promptPos.value = prompt;
            updateInput(promptPos);
          } else {
            promptPos.value = previewPrompt;
            updateInput(promptPos);
          }
        }
      }
      const applyStyleNeg = gradioApp().querySelector('#styles_apply_neg > label > input');
      if (applyStyleNeg.checked === true) {
        if (negative !== '') {
          promptNeg.value = previewNegative;
          updateInput(promptNeg);
        }
      }
    }
}

function hoverPreviewStyleOut() {
    const enablePreview = gradioApp().querySelector('#HoverOverStyle_preview > label > input').checked;
    if (enablePreview === true) {
      const tabname = getENActiveTab();
      const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
      const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
      promptPos.value = orgPrompt;
      promptNeg.value = orgNegative;
      updateInput(promptPos);
      updateInput(promptNeg);
      orgPrompt = '';
      orgNegative = '';
    }
  }

function cardSizeChange(value) {
    const styleCards = gradioApp().querySelectorAll('.style_card');
    styleCards.forEach((card) => {
        card.style.height = value + 'px';
    });
}

function filterSearch(cat, search) {
    let searchString = search.toLowerCase();
    const styleCards = gradioApp().querySelectorAll('.style_card');
    if (searchString == "") {
        if (cat == "All") {
            styleCards.forEach(card => {
                card.style.display = "flex";
            });
        } else if (cat == "Favourites") {
            styleCards.forEach(card => {
                var btn = card.querySelector(".favouriteStyleBtn");
                let computedelem = getComputedStyle(btn);
                if (computedelem.color === "rgb(255, 255, 255)") {
                    card.style.display = "none";
                } else {
                    card.style.display = "flex";
                }
            });
        } else {
            styleCards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');
                if (cardCategory == cat) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            });
        }
    } else {
        if (cat == "All") {
            styleCards.forEach(card => {
                const cardTitle = card.getAttribute('data-title');
                if (cardTitle.includes(searchString)) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            });
        } else if (cat == "Favourites") {
            styleCards.forEach(card => {
                const cardTitle = card.getAttribute('data-title');
                var btn = card.querySelector(".favouriteStyleBtn");
                let computedelem = getComputedStyle(btn);
                if (cardTitle.includes(searchString)) {
                    if (computedelem.color === "rgb(255, 255, 255)") {
                        card.style.display = "none";
                    } else {
                        card.style.display = "flex";
                    }
                } else {
                    card.style.display = "none";
                }
            });
        } else {
            styleCards.forEach(card => {
                const cardTitle = card.getAttribute('data-title');
                const cardCategory = card.getAttribute('data-category');
                if (cardTitle.includes(searchString) && cardCategory == cat) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            });
        }
    }
}

function editStyle(title, img, description, prompt, promptNeggative, folder, filename) {
    // title
    const editorTitle = gradioApp().querySelector('#style_title_txt > label > textarea');
    applyValues(editorTitle, title);
    // img
    const imgUrlHolderElement = gradioApp().querySelector('#style_img_url_txt > label > textarea');
    applyValues(imgUrlHolderElement, img);
    // applyValues(editor_img, title);
    // description
    const editorDescription = gradioApp().querySelector('#style_description_txt > label > textarea');
    applyValues(editorDescription, description);
    // prompt
    const editorPrompt = gradioApp().querySelector('#style_prompt_txt > label > textarea');
    applyValues(editorPrompt, prompt);
    // promptNeggative
    const editorPromptNeggative = gradioApp().querySelector('#style_negative_txt > label > textarea');
    applyValues(editorPromptNeggative, promptNeggative);
    // Category
    const editorSaveFolder = gradioApp().querySelector('#style_savefolder_txt > label > div > div > div > input');
    const editorTempFolder = gradioApp().querySelector('#style_savefolder_temp > label > textarea');
    applyValues(editorTempFolder, folder);
    applyValues(editorSaveFolder, folder);
    // filename
    const editorFilename = gradioApp().querySelector('#style_filename_txt > label > textarea');
    filename = decodeURIComponent(filename); // Decode the filename
    filename = filename.replace('.json', '');
    applyValues(editorFilename, filename);
    // press tab button
    const tabsdiv = gradioApp().getElementById(`Stylez`);
    function findEditorButton() {
        const buttons = tabsdiv.querySelectorAll('button');
        for (const button of buttons) {
            if (button.innerText === 'Style Editor') {
                return button;
            }
        }
        return null;
    }
    const editorButton = findEditorButton();
    if (editorButton) {
        editorButton.click();
    }
}
function grabLastGeneratedimage() {
    const tabname = getENActiveTab();
    const imagegallery = gradioApp().querySelector(`#${tabname}_gallery`);
    if (imagegallery) {
        const firstImage = imagegallery.querySelector('img');
        if (firstImage) {
            let imageSrc = firstImage.src;
            imageSrc = imageSrc.replace(/.*file=/, '');
            imageSrc = decodeURIComponent(imageSrc); // Decode the URL-encoded file name
            const imgUrlHolderElement = gradioApp().querySelector('#style_img_url_txt > label > textarea');
            applyValues(imgUrlHolderElement, imageSrc);
        }
    }
}

function grabCurrentSettings() {
    // prompt
    const tabname = getENActiveTab();
    const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
    const editorPrompt = gradioApp().querySelector('#style_prompt_txt > label > textarea');
    applyValues(editorPrompt, promptPos.value);
    // promptNeggative
    const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
    const editorPromptNeggative = gradioApp().querySelector('#style_negative_txt > label > textarea');
    applyValues(editorPromptNeggative, promptNeg.value);
}
function deleteRefresh() {
    const galleryrefresh = gradioApp().querySelector('#style_refresh');
    const stylesclear = gradioApp().querySelector('#style_clear_btn');
    galleryrefresh.click();
    stylesclear.click();
}
function saveRefresh() {
    setTimeout(() => {
        const galleryrefresh = gradioApp().querySelector('#style_refresh');
        galleryrefresh.click();
    }, 1000); // 1000 milliseconds = 1 second
}

function addFavourite(folder, filename, element) {
    let computedelem = getComputedStyle(element);
    const addfavouritebtn = gradioApp().querySelector('#stylezAddFavourite');
    const removefavouritebtn = gradioApp().querySelector('#stylezRemoveFavourite');
    filename = decodeURIComponent(filename);
    const favTempFolder = gradioApp().querySelector('#favouriteTempTxt > label > textarea');
    if (computedelem.color === "rgb(255, 255, 255)") {
        element.style.color = "#EBD617";
        applyValues(favTempFolder, folder + "/" + filename);
        addfavouritebtn.click();
    } else {
        element.style.color = "#ffffff";
        applyValues(favTempFolder, folder + "/" + filename);
        removefavouritebtn.click();
    }
}

function addQuicksave () {
    const ulElement = gradioApp().getElementById('styles_quicksave_list');
    const tabname = getENActiveTab();
    const promptPos = gradioApp().querySelector(`#${tabname}_prompt > label > textarea`);
    const promptNeg = gradioApp().querySelector(`#${tabname}_neg_prompt > label > textarea`);
    var liElement = document.createElement('li');
    var deleteButton = document.createElement('button');
    var innerButton = document.createElement('button');
    var promptParagraph = document.createElement('button');
    var negParagraph = document.createElement('button');
    if (promptPos.value !== "" || promptNeg.value !== "") {
       
        if (promptPos.value == "")
        {
            promptParagraph.disabled = true  
            promptParagraph.textContent = "EMPTY"
        }
        else {
            promptParagraph.disabled = false  
            promptParagraph.textContent = promptPos.value;
        }
        if (promptNeg.value == "")
        {
            negParagraph.disabled = true
            negParagraph.textContent = "EMPTY"
        } else {
            negParagraph.disabled = false
            negParagraph.textContent = promptNeg.value;
        }
        liElement.className = 'styles_quicksave';
        deleteButton.className = 'styles_quicksave_del';
        deleteButton.textContent = '❌';
        deleteButton.onclick = function() {
            deletequicksave(this)
        };
        promptParagraph.onclick = function() {
            applyValues(promptPos,this.textContent)
        };
        promptParagraph.className = 'styles_quicksave_prompt styles_quicksave_btn';

        negParagraph.onclick = function() {
            applyValues(promptNeg,this.textContent)
        };
        negParagraph.className = 'styles_quicksave_neg styles_quicksave_btn';
        innerButton.className = 'styles_quicksave_apply';
        innerButton.appendChild(promptParagraph);
        innerButton.appendChild(negParagraph);
        liElement.appendChild(deleteButton);
        liElement.appendChild(innerButton);
        ulElement.appendChild(liElement);
    }
}

function deletequicksave(elem) {
    const quicksave = elem.parentNode;
    const list = quicksave.parentNode;
    list.removeChild(quicksave);
}

function clearquicklist() {
    const list = gradioApp().getElementById("styles_quicksave_list")
    while (list.firstChild) {
        list.removeChild(list.firstChild);
    }
}
