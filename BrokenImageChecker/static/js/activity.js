$(document).ready(function(){
    $("button").click(function(){
        $.ajax({url: "/linkcheck", success: function(result){
        console.log(result);
        }});
    });
});
  