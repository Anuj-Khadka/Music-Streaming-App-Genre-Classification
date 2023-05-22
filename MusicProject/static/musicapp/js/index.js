const allSongsMiniPlayer = document.querySelector(".mini-audio");
window.addEventListener("load", e=>{
    // allSongsMiniPlayer.pause();
})

const searchFormContainer = document.getElementById("search-form-container")
const searchField = document.getElementById("search-field")
searchField.addEventListener("focus", e=>{
    searchFormContainer.style.boxShadow = "2px 3px 20px 5px #1412123e"
})

