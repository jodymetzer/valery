var express = require('express');
var app = express();
var path = require('path');
var http = require('http').Server(app);
var io = require('socket.io')(http);
var PythonShell = require('python-shell');

app.use(express.static('public'))

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
  socket.on('speed', function(msg){
    console.log('speed: ' + msg);
    

    var options = {
        mode: 'text',
        args: ['--option=' + msg]
    };

    PythonShell.run('child.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
    });
  });
});

io.on('connection', function(socket){
  socket.on('reset', function(msg){
    console.log('reset? ' + msg);
  });
});