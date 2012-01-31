%import base64
%for result in results:
     <div class="cell">
         <a href="/content/{{base64.b16encode(result['data_id'])}}.b16.html" class="top_up" toptions="effect=hide, modal=1" target="_blank"><img src="/content/{{base64.b16encode(result['data_id'])}}.b16.thumb.jpg" alt="{{result['data_id']}}" /></a>
         Conf[{{result['conf']}}]<br>
         Polarity[{{result['polarity']}}]<br>
         <!-- DataID[{{result['data_id']}}] -->
     </div>
%end