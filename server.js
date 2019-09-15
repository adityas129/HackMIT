var ip_address = '18.20.216.61';

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

let db = firebase.firestore();


// db.collection('cats').get()
//   .then((snapshot) => {
//     snapshot.forEach((doc) => {
//       console.log(doc.id, '=>', doc.data());
//       console.log("ldsakfjjasdfjlfsd")
//     });
//   })
//   .catch((err) => {
//     console.log('Error getting documents', err);
//   });



//   //this is how you write to db!!!
//   let docRef = db.collection('cats').doc('writing_first_time');
//   let writing_first_time = docRef.set({
//     'Adi': 'bad',
//     'bad': 15,
//     'good': 10, 
//     predicted_label: 'bad'
//   });  npm install express --save





// http.createServer(function (request, response) {
//    // Send the HTTP header 
//    // HTTP Status: 200 : OK
//    // Content Type: text/plain
//    response.writeHead(200, {'Content-Type': 'text/html'});
//    // Send the response body as "Hello World"
//    // response.end('Hello World\n');

//    fs.readFile('./upload.html', null, function (error, data) {
//         if (error) {
//             response.writeHead(404);
//             respone.write('Whoops! File not found!');
//         } else {
//             response.write(data);

//             // response.write(data);
//         }
//         response.end();
//     });

// }).listen(3000, ip_address);


// Console will print the message
console.log('Server running at http://127.0.0.1:8081/');




console.log('Server-side code running');

const express = require('express');

const app = express();

app.use(express.static('public'));

// start the express web server listening on 8080
app.listen(8080, () => {
  console.log('listening on 8080');
});

// serve the homepage
app.get('/', (req, res) => {

  res.sendFile(__dirname + '/welcome.html');
});


app.get('/clicked', (req, res) => {
  const click = {clickTime: new Date()};
  console.log(click);
  console.log("kkmkmmkm");

  // db.collection('data1').doc('express-test');
  let docRef = db.collection('test').doc()

  let writing_first_time = docRef.set({
    'Adi': 'bad',
    'bad': 15,
    'good': 10, 
    predicted_label: 'bad'
  });
  res.sendFile(__dirname + '/labelling_session.html');

});

app.post('/submit', (req, res) => {
  console.log("kkmkmmkm");
  res.sendFile(__dirname + '/labelling_session.html');

});
var path = process.cwd();

app.route('/uploading')
 	.get(function (req, res) {
      
    res.sendFile(__dirname + '/upload.html');
	});

  app.route('/login')
 	.get(function (req, res) {
      
    res.sendFile(__dirname + '/login.html');
	});


app.route('/goData')
 	.get(function (req, res) {

var sentiment = {negative_c: 0, positive_c:0, neutral_c:0}
var ejs_i = 0;
var data_json = [{},sentiment, ejs_i];
var index = 0;
      
db.collection('data1').get()
  .then((snapshot) => {
    snapshot.forEach((doc) => {
      sentiment.negative_c = sentiment.negative_c + parseInt(JSON.stringify(doc.data().label_distribution.Negative));
      sentiment.neutral_c = sentiment.neutral_c + parseInt(JSON.stringify(doc.data().label_distribution.Neutral));
      sentiment.positive_c = sentiment.positive_c + parseInt(JSON.stringify(doc.data().label_distribution.Positive));
    });
})
  

  .catch((err) => {
    console.log('Error getting documents', err);
  });
      
  console.log("outside fo the db read");
  
  db.collection('data1').get()
    .then((snapshot) => {
      console.log("in the snapshot");
      
      snapshot.forEach((doc) => {
        data_json[0][index] = doc.data();
        index++;
        // console.log('bruh', data_json.data)
        // options = data_json.label_distribution
        // const html_gen = window.document.createElement('<option value="label_option_3">${options}</option>')
        // console.log(html_gen)
      });
      
      app.set('view engine', 'ejs');
      console.log(Object.keys(data_json[0]).length);
      res.render(path + '/labelling_session.ejs', {dynamic : data_json});
      })
    .catch((err) => {
      console.log('Error getting documents', err);
    });
});



  