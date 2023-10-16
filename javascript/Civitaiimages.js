let currentPage = 1;
let isLoading = false;
let nopreview = ""
let loadedStyleIDs = [];

function refreshfetchCivitai(nswflvl, sortcivit, periodcivit)
{
    loadedStyleIDs = []
    const cardholderElement = document.getElementById("civitai_cardholder");
    while (cardholderElement.firstChild) {
        cardholderElement.removeChild(cardholderElement.firstChild);
    }
    currentPage = 1
    fetchCivitai(nswflvl, sortcivit, periodcivit, currentPage)
}

function civitaiaCursorLoad(elem) {
    if (elem.scrollTop + elem.clientHeight >= elem.scrollHeight) {
        currentPage++; // Increment the current page
        const nswflvl = gradioApp().querySelector('#civit_nsfwfilter > label > div > div > div > input').value;
        const sortcivit = gradioApp().querySelector('#civit_sortfilter > label > div > div > div > input').value;
        const periodcivit = gradioApp().querySelector('#civit_periodfilter > label > div > div > div > input').value;
        fetchCivitai(nswflvl, sortcivit, periodcivit, currentPage); // Fetch new results for the next page
    }
};

async function fetchCivitai(nswflvl, sortcivit, periodcivit, page) {
    const api_url = "https://civitai.com/api/v1/images";
    const Cardslider = gradioApp().querySelector('#card_thumb_size > div > div > input');
    const cardholderElement = document.getElementById("civitai_cardholder");
    const loadingElement = document.getElementById("civitaiimages_loading");
    loadingElement.style.display = "block";
    if (isLoading) {
        return; // Prevent concurrent requests
    }

    try {
        isLoading = true;
        const params = new URLSearchParams({
            limit: 50,
            nsfw: nswflvl,
            sort: sortcivit,
            period: periodcivit,
            cursor: (page - 1) * 50,
        });

        const response = await fetch(`${api_url}?${params.toString()}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.status === 200) {
            const api_data = await response.json();

            for (const item of api_data.items || []) {
                const meta_data = item.meta;
                const title = "by " + item.username;
                const img = item.url;
                const description = item.username + " " + item.id;
                let prompt = "";
                let prompt_negative = "";
                if (meta_data) {
                    if ('prompt' in meta_data) {
                        prompt = encodeURIComponent(meta_data.prompt.replace(/'/g, '%27'));
                    }
                    if ('negativePrompt' in meta_data) {
                        prompt_negative = encodeURIComponent(meta_data.negativePrompt.replace(/'/g, '%27'));
                    }
                }
                // Generate a unique style ID based on the URL and title
                const styleID = `${item.id}`;
                if (
                    decodeURIComponent(prompt) !== "" &&
                    decodeURIComponent(prompt_negative) !== "" &&
                    loadedStyleIDs.indexOf(styleID) === -1
                ) {
                    let style_html = `
                    <div class="style_card" style="min-height:${Cardslider.value}px;max-height:${Cardslider.value}px;min-width:${Cardslider.value}px;max-width:${Cardslider.value}px;">
                        <img class="styles_thumbnail" src="${img}" onerror="this.src='file=${nopreview}'">
                        <div class="EditStyleJson">
                            <button onclick="editStyle('${title}','${img}','${description}','${prompt}','${prompt_negative}','subfolder_name','encoded_filename','CivitAI')">🖉</button>
                        </div>
                        <div onclick="applyStyle('${prompt}','${prompt_negative}','CivitAI')" onmouseenter="event.stopPropagation(); hoverPreviewStyle('${prompt}','${prompt_negative}','CivitAI')" onmouseleave="hoverPreviewStyleOut()" class="styles_overlay"></div>
                        <div class="styles_title">${title}</div>
                        <p class="styles_description">${description}</p>
                    </div>`;
                    cardholderElement.innerHTML += style_html;
                    loadedStyleIDs.push(styleID);
                }
            }
            isLoading = false; // Allow the next request
        } else {
        console.error(`Request failed with status: ${response.status}`);
        }
    loadingElement.style.display = "none";
    } catch (error) {
        isLoading = false; // Handle error and allow the next request
        console.log(`Error occurred: ${error}`);
        loadingElement.style.display = "none";
    }
}

function setupcivitapi () {
    const cardholderElement = document.getElementById("civitai_cardholder");
    const dataNopreviewValue = cardholderElement.getAttribute("data-nopreview");
    nopreview = encodeURIComponent(dataNopreviewValue)
    fetchCivitai("None", "Most Reactions", "AllTime", "1")
   
}