<html><head><script src="http://code.jquery.com/jquery-latest.js"></script><script src="http://gettopup.com/releases/latest/top_up-min.js"></script>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<style type="text/css">
.cell
{
float: left;
width: 200px;
height: 300px;
padding-top: 50px;
}
</style>

</head><body>
<form>
<select id="class_name">
    %import base64
    %for c in classes:
        <option value={{base64.b16encode(c)}}>{{c}}</option>
    %end
</select>


<select id="feature_classifier_name">
    %import base64
    %for c in feature_classifiers:
        <option value={{base64.b16encode(c)}}>{{c}}</option>
    %end
</select>

<select id="page_num">
  <option>{{0}}</option>
</select>
</form>

<div id="graphs"></div>

<div id="main"></div>

<script>

function update_page_nums(myOptions) {
    if (jQuery.isEmptyObject(myOptions)) {
        return;
    }
    $('#page_num >option').remove();
    $.each(myOptions, function(val, text) {
        $('#page_num').append(
            $('<option></option>').val(val).html(text)
        );
    });
}

function update_main() {
    var url = 'body/' + $('#class_name').val() + '/' + $('#feature_classifier_name').val() + '/' + $('#page_num').val() + '/?callback=?';
    $.getJSON(url, function(data) {
        update_page_nums(data.page_nums);
        $('#main').html(data.data);
        $('#graphs').html('');
        $.each(data.graphs, function(index, value) { 
            $('#graphs').append(value.html);
            eval(value.js);
        });
    });
}
$('#class_name').change(update_main);
$('#feature_classifier_name').change(update_main);
$('#page_num').change(update_main);
$(update_main);
</script>
</body></html>
