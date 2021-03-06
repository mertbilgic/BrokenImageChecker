let namespace = '/events';
let socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
var room;

$(document).ready(function(){
    $("button").click(function(){
        
        var url =$('input[name="url"]').val();
        $.ajax({
            type: "POST",        
            data: {
                url: url,
                room: room,
            },
            url: "/taskrun", success: function(result){
        }});
        $("#progress").show();
        demo();
    });
});
var progressbar = new Nanobar({target: document.getElementById('progress')});
var start = 10;
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
async function demo() {
    for(var i=1;i<=10;i++){
        status= start*i
        progressbar.go(status);
        await sleep(1000);
    }
    $("#progress").hide();
    progressbar.go(0);
}

function update_progress() {
    console.log("Update");
    var element = $('#result');
    $(element[0].childNodes[1]).text('%100');
    $(element[0].childNodes[1]).next().text("Update_progress Demo");
}

socket.on('connect', function() {
   console.log("Connection Start");
});

socket.on('crawlerstatus', function(msg) {
    msg.Result = JSON.parse(msg.Result);
    writeResponse(msg);
});

socket.on('room', function(msg) {
    room = msg.room;
    //socket.emit('join', {room:room});
    console.log("Join Room",room);
});

var tagsToReplace = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
};
function replaceTag(tag) {
    return tagsToReplace[tag] || tag;
}

function safe_tags_replace(str) {
    return str.replace(/[&<>]/g, replaceTag);
}
function writeResponse(response){
    $(".result")
    .removeClass("d-none")
    .addClass("d-block")
    document.getElementById("response").innerHTML = safe_tags_replace(JSON.stringify(response, undefined, 2));
}