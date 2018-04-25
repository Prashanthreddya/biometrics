$(document).ready(function()
{
    $("#drop-area").on('dragenter', function (e){
        console.log('dragenter');
        e.preventDefault();
        $(this).css('background', 'lightgrey');
    });

    $("#drop-area").on('dragover', function (e){
        console.log('dragover');
        e.preventDefault();
    });

    $("#drop-area").on('drop', function (e){
        $(this).css('background', 'silver');
        $(".drop-text").html('Predicting class...');
        e.preventDefault();
        console.log('drop');
        var file = e.originalEvent.dataTransfer.files[0];
        console.log(file);

        var reader = new FileReader();
        reader.onload = function(){
            var data = { 'file': reader.result };
            $.ajax({
                type: 'POST',
                url: 'run-test',
                data: data,
                cache: false,
                success: function(data){
                    console.log(data);
                    document.write(data);
                }
            });
        };

        reader.readAsDataURL(file);

    });
});
