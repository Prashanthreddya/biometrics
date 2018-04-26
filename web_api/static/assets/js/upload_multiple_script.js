$(document).ready(function()
{
    var ready = false;
    var b64_files = [];
    var check = function() {
        if (ready === true) {
            var name = $('#inputname')[0].value;
            var res = {'files': JSON.stringify(b64_files), 'class_id': $(".class_id")[0].innerHTML, 'name': name};
            console.log(res);
            $.ajax({
                type: 'POST',
                url: 'add-datapoint',
                data: res,
                cache: false,
                success: function(data){
                    console.log(data);
                    $(".drop-text").html("Images uploaded. Performing training.");
                    window.location="retrain-model";
                }
            });
            return;
        }
        setTimeout(check, 1000);
    }

    check();

    document.getElementById("inputfile").onchange = function(e) {
        var files = $(this)[0].files;
        $("#drop-area").css('background', 'silver');
        $(".drop-text").html('Uploading images...');
        e.preventDefault();

        for(var i=0 ; i<files.length ; i++){
            var reader = new FileReader();
            reader.onloadend = function(e){
                b64_files.push(e.target.result)
            };
            reader.readAsDataURL(files[i]);

            if(i==files.length-1){
                ready = true;
            }
        }
    };
});
