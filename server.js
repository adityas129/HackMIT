var http = require("http");
var fs = require('fs');

var firebase = require('firebase');

var firebaseConfig = {
  apiKey: "AIzaSyCvIgWTTi16ESUYEhbQlRda9ItjXgvRgyU",
  authDomain: "minerva-7ae74.firebaseapp.com",
  databaseURL: "https://minerva-7ae74.firebaseio.com",
  projectId: "minerva-7ae74",
  storageBucket: "",
  messagingSenderId: "1018992044633",
  appId: "1:1018992044633:web:dcdfdb4754bde54e095f48"
};
  
firebase.initializeApp(firebaseConfig);
var database = firebase.database();
var ref = database.ref('fruits/');

var data;
ref.on("value", function(snapshot) {
  data = snapshot.val();
  console.log(data);
}, function (error) {
  console.log("Error: " + error.code);
});
  
http.createServer(function (request, response) {
   // Send the HTTP header 
   // HTTP Status: 200 : OK
   // Content Type: text/plain
   response.writeHead(200, {'Content-Type': 'text/html'});
   
   // Send the response body as "Hello World"
   // response.end('Hello World\n');

   fs.readFile('./sample_html.html', null, function (error, data) {
        if (error) {
            response.writeHead(404);
            respone.write('Whoops! File not found!');
        } else {
            response.write(data);
        }
        response.end();
    });
}).listen(3000, '172.16.149.63');

// Console will print the message
console.log('Server running at http://127.0.0.1:8081/');
