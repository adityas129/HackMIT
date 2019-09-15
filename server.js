var ip_address = '18.20.216.61';

var http = require("http");
var fs = require('fs');

var firebase = require('firebase');
var admin = require('firebase-admin');
var funcs = require('firebase-functions');

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

let db = firebase.firestore();
db.collection('cats').get()
  .then((snapshot) => {
    snapshot.forEach((doc) => {
      console.log(doc.id, '=>', doc.data());
    });
  })
  .catch((err) => {
    console.log('Error getting documents', err);
  });



  //this is how you write to db!!!
  let docRef = db.collection('cats').doc('writing_first_time');
  let writing_first_time = docRef.set({
    'Adi': 'bad',
    'bad': 15,
    'good': 10, 
    predicted_label: 'bad'
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

}).listen(3000, ip_address);

// Console will print the message
console.log('Server running at http://127.0.0.1:8081/');