// function documentReady() {
//     let map_ready = $('#map');
//     console.log('I ran');
//     if(map_ready && map_ready.length > 0) {
//         console.log('I ran too')
//         var script = document.createElement('script');
//         script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyDdirJ_CHq2uFNRHMch-l-xwAih7-iT-cY&callback=initMap';
//         script.async = true;
//         script.defer = true;
//         window.initMap = function() {
//                 var map = new google.maps.Map(document.getElementById("map"), {
//                     center: { lat: 53.477385717110856, lng: -2.6035911593546963 },
//                     zoom: 8,
//                 });
//         };
//         document.body.appendChild(script);
//         clearInterval(refreshID);
//     }
// };

// let refreshID = setInterval(documentReady(), 250)

// $(document).ready(function() {
//     setTimeout(() => {
//         var script = document.createElement('script');
//         script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyDdirJ_CHq2uFNRHMch-l-xwAih7-iT-cY&callback=initMap';
//         script.async = true;
//         script.defer = true;
//         window.initMap = function() {
//                 var map = new google.maps.Map(document.getElementById("map"), {
//                     center: { lat: 53.477385717110856, lng: -2.6035911593546963 },
//                     zoom: 8,
//                 });
//         };
//         $('#markerButton').click(function() {
//             addMarker()
//         });
//         document.body.appendChild(script);
//         var map = new google.maps.Map(document.getElementById("map"))

//         function addMarker() {
//             const marker = new google.maps.Marker({
//                 position: office,
//                 map: map,
//             });
//         };

//     }, 5000);
// });

// const office = {lat: 53.477369754208965, lng: -2.6035697014869266}


// const office = {lat: 53.477369754208965, lon: -2.6035697014869266}
// const marker = new google.maps.Marker({
//     position: office,
//     map: map,
// });



// This works somewhat but you have to run initMap in console after the page has loaded, for some reason, despite the custom.js file being in the footer the dom does not seem to be loaded
//when this function is called, despite it being after the map-div in the DOM, need someway to have the function be called only after the full document is loaded explicitly or with a deliverate
// time delay placed on it, like wait 30 secionds after load and then run the function 04/11/1500

//Managed to get working to some degree by putting a delay on the innitMap funciton, I will likely just keep this to save any further headaches and have a loading screen where the map is when
// the page is opened.

//Serious problem with they way dash loads javascript, despite it being at the end of the document it is running before anything else in the document causing it to error, their is a way to ignore assets and then perhaps call the script
// at the end of the document to avert this

//Unlikely I will be able to get the js running at the end of the document, a better solution to increase speed slightly would be to have some function that is run at the start of the document that tests repeatedly to see if the rest of
//document has loaded before allowing the rest of the javascript to execute

// function addMarker(lat, lng) {
//     var latlng = {lat: lat, lon: lng}
//     var marker = new google.maps.Marker({
//         position: latlng,
//         map: map,
//     });
// }
