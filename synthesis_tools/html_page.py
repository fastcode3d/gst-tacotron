# -*- coding: utf-8 -*-
# html_page.py


html_body = '''<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="毛志强">

    <title>南京硅基智能语音合成引擎</title>

    <!-- Bootstrap core CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" 
     integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous" rel="stylesheet">

    <!-- Custom styles for this template -->
    <style>
      body {
        padding-top: 54px;
      }
      @media (min-width: 992px) {
        body {
          padding-top: 56px;
        }
      }

    </style>
  </head>
  
  <body>

    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div class="container">
        <a class="navbar-brand" href="#">硅基智能TTS</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive"
         aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item active">
              <a class="nav-link" href="http://www.guiji.ai/">主页
                <span class="sr-only">(current)</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <div class="container">
      <div class="row">
        <div class="col-lg-12 text-center">
          <h3 class="mt-5">硅基智能语音合成引擎</h3>
          <p class="lead">请在下面输入框里输入您想要合成的内容</p>
          <ul class="list-unstyled">
          </ul>
          <input id="text" type="text" size="40" placeholder="输入文字" onKeyPress='IsEnterKeyPress()'>
          <button id="button" name="synthesize">合成</button><br/><br/>
          <audio id="audio" controls autoplay hidden></audio>
          <p id="message"></p>
        </div>
      </div>
    </div>
<body>
<p id="message"></p>
  <h8 style="text-align:rignt">
     &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
     &emsp;&emsp;&emsp;用法:
     <br>
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;数字：不需要加标记符号
         <br>
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;电话号码：(#83278311)注意里面的1读幺
         <br>
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;按位读法：($32673) 按数字读法 2读二 1读一
         <br>
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2两读法：(@32673) 按数字读法 2读两
         <br>
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2两读法：(!32673) 按数字读法 2读两,一读幺
         <br>
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
         &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;合成支持英文字母，数字，汉字组合
         <br>
  </h8>
<script>

function q(selector) {return document.querySelector(selector)}
q('#text').focus()
q('#button').addEventListener('click', function(e) {
      text = q('#text').value.trim()
      if (text) {
        q('#message').textContent = '合成中...'
        q('#button').disabled = true
        q('#audio').hidden = true
        synthesize(text)
      } 
  e.preventDefault()
  return false
})
function IsEnterKeyPress(){
  var event=event||window.event;
  console.log(event.keyCode);
  if(event.keyCode==13){
      text = q('#text').value.trim()
      if (text) {
        q('#message').textContent = '合成中...'
        q('#button').disabled = true
        q('#audio').hidden = true
        synthesize(text)
      }
  }
  return false
}
function synthesize(text) {
  url = '/synthesize'
  // url = '/synthesize?text=' + encodeURIComponent(text)
  console.log('feching ' + url)
  fetch(url, {
    method: 'POST',
    body: JSON.stringify({text: text}),
    cache: 'no-cache'
  })
    .then(function(res) {
      if (!res.ok) throw Error(response.statusText)
      return res.blob()
    }).then(function(blob) {
      q('#message').textContent = ''
      q('#button').disabled = false
      q('#audio').src = URL.createObjectURL(blob)
      q('#audio').hidden = false
    }).catch(function(err) {
      q('#message').textContent = 'Error: ' + err.message
      q('#button').disabled = false
    })
}
</script></body></html>
'''
