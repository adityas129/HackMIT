
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
db.collection("data1")
.get()
.then(querySnapshot => {
    if (!querySnapshot.empty) {
        //We know there is one doc in the querySnapshot
        const queryDocumentSnapshot = querySnapshot.docs[0].label_distribution;
        return console.log(queryDocumentSnapshot);
    } else {
        console.log("No document corresponding to the query!");
        return null;
    }
});
console.log("NONLADASKNONLADASKNONLADASKNONLADASKNONLADASKNONLADASKNONLADASKNONLADASK");

db.collection('data1').get()
  .then((snapshot) => {
    
    snapshot.forEach((doc) => {
        var fragment = create('<option value="label_option_1">${doc}</option>'); 

        var generateHere = document.getElementById("generate-datapoint_labels")
        generateHere.insertBefore(fragment, generateHere.firstChild);
        console.log(doc.id, '=>', doc.data());
    });
  })
  .catch((err) => {
    console.log('Error getting documents', err);
  });



window.onload = function () {

    var chart = new CanvasJS.Chart("chartContainer", {
        title: {
            text: "Realit"
        },
        axisY: {
            title: "Temperature",
            suffix: " °C"
        },
        data: [{
            type: "column",	
            yValueFormatString: "#,### °C",
            indexLabel: "{y}",
            dataPoints: [
                { label: "boiler1", y: 206 },
                { label: "boiler2", y: 163 },
                { label: "boiler3", y: 154 },
                { label: "boiler4", y: 176 },
                { label: "boiler5", y: 184 },
                { label: "boiler6", y: 122 }
            ]
        }]
    });
    
    var pie_chart = new CanvasJS.Chart("chartContainer", {
        theme: "dark2", // "light1", "light2", "dark1", "dark2"
        exportEnabled: true,
        animationEnabled: true,
        title: {
            text: "Cats" //dynamic according to the label that the user is in
        },
        data: [{
            type: "pie",
            startAngle: 25,
            toolTipContent: "<b>{label}</b>: {y}%",
            showInLegend: "true",
            legendText: "{label}",
            indexLabelFontSize: 16,
            indexLabel: "{label} - {y}%",
            dataPoints: [
                { y: 51.08, label: "Chrome" },
                { y: 27.34, label: "Internet Explorer" },
                { y: 10.62, label: "Firefox" },
                { y: 5.02, label: "Microsoft Edge" },
                { y: 4.07, label: "Safari" },
                { y: 1.22, label: "Opera" },
                { y: 0.44, label: "Others" }
            ]
        }]
    });
    pie_chart.render();
    
    function updateChart() {
        var boilerColor, deltaY, yVal;
        var dps = chart.options.data[0].dataPoints;
        for (var i = 0; i < dps.length; i++) {
            deltaY = Math.round(2 + Math.random() *(-2-2));
            yVal = deltaY + dps[i].y > 0 ? dps[i].y + deltaY : 0;
            boilerColor = yVal > 200 ? "#FF2500" : yVal >= 170 ? "#FF6000" : yVal < 170 ? "#6B8E23 " : null;
            dps[i] = {label: "Boiler "+(i+1) , y: yVal, color: boilerColor};
        }
        chart.options.data[0].dataPoints = dps; 
        chart.render();
    };
    updateChart();
    var generateHere = document.getElementById("generate-here");
    generateHere.insertBefore(fragment, generateHere.firstChild);
    setInterval(function() {updateChart()}, 500);
    
    }