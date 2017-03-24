var express = require('express');
var app = express();
var path = require('path');
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.use(express.static('public'))

var PythonShell = require('python-shell');

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});

io.on('connection', function(socket){
  socket.on('reset', function(res){
    console.log('reset? ' + res);
  });
});

io.on('connection', function(socket){
  socket.on('speed', function(msg){
    var options = {
      mode: 'text',
      args: [msg]
    };
    PythonShell.run('child.py', options, function (err, results) {
      if (err) throw err;
      
      console.log('results: %j', results);
    });
    console.log('speed: ' + msg);
  });
});


