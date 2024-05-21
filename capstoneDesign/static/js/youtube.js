// 2. This code loads the IFrame Player API code asynchronously.

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '360',
        width: '100%',
        videoId: youtubeLink,
        events: {
            'onReady': onPlayerReady,
        },

    });
}

var num = 0;

function setNum(num) {
    this.num = num;
    onPlayerReady()
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    //event.target.seekTo(20 , true)
}


function moveTime(time) {
    if (player) {
        player.seekTo(parseFloat(time), true);
    }
}



function getCurrentTime() {
    if (player && player.getPlayerState() === YT.PlayerState.PLAYING) {
        return player.getCurrentTime();
    }
    return 0;
}


// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
var done = false;
