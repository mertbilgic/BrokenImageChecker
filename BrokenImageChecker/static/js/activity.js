$(document).ready(function(){
    $("button").click(function(){
        $.ajax({type: "POST",url: "/taskrun", success: function(result){
        console.log(result);
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
  