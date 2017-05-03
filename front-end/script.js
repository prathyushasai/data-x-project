// Globals.
var urlFormId = '#url-form';
var urlFormInputId = '#url-form-input';
var videoIFrameId = '#video-iframe';
var labelsListId = '#labels-list';
var initialVideoURL = 'https://www.youtube.com/watch?v=YbcxU1IK7s4';
var startLabelIndex = 0;
var endLabelIndex = 5;
var colors = ['red', 'orange', 'green', 'blue', 'purple'];

function setVideoTime(seconds) {
    var iframe = $(videoIFrameId);
    var currentSrc = iframe.attr('src');
    var newSrc = currentSrc.split('?').shift();
    newSrc += "?start=" + seconds + "&autoplay=1";
    iframe.attr('src', newSrc);
    iframe.contentWindow.location.reload();
    return false; // Prevents page reload
}

function secondsToHms(d) {
    d = Number(d);
    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);
    return ((h > 0 ? h + ":" + (m < 10 ? "0" : "") : "") + m + ":" + (s < 10 ? "0" : "") + s);
}

function loadVideo(id) {
    var urlFormInput = $(urlFormInputId);
    urlFormInput.val('http://youtu.be/' + id);
    urlFormInput.submit();
}

$(document).ready(function() {

    var urlForm = $(urlFormId);
    var urlFormInput = $(urlFormInputId);
    var videoIFrame = $(videoIFrameId);
    var labelsList = $(labelsListId);

    $('.row.content').height($(window).height());

    // Set up submit Handler
    urlForm.submit(function urlFormSubmit(event) {
        var label = 'test';
        var timeLinks = [0, 1, 2, 0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2];
        var listItems = [];
        for(var i in colors) {
            var toAdd = '';
            if (i % 5 == 0) {
                toAdd += '<div class="col-md-2 col-md-offset-1" style="height:200px;"><h4 style="background-color:' + colors[i] + '; padding: 2px; width: 80%; margin: 0 auto; color: white">' + label + i + '</h4><div style="overflow-y: scroll; height: 80%; margin-top:5%;"><ul class="list-unstyled">';
            } else {
                toAdd += '<div class="col-md-2" style="height:200px;"><h4 style="background-color:' + colors[i] + '; padding: 2px; width: 80%; margin: 0 auto; color: white">' + label + i + '</h4><div style="overflow-y: scroll; height: 80%; margin-top:5%;"><ul class="list-unstyled">';
            }
            
            for (var j in timeLinks) {
                toAdd += '<li>' + timeLinks[j] + '</li>';
            }
            toAdd += '</ul></div></div>';

            listItems.push(toAdd);
        }
        labelsList.html(listItems);

        // Don't reload the page.
        event.preventDefault();

        // Set the video URL
        // User gives: https://www.youtube.com/watch?v=YbcxU1IK7s4
        // Embed frame needs: https://www.youtube.com/embed/YbcxU1IK7s4
        var url = urlFormInput.val()
        var videoId = url.split("v=").length == 2 ? url.split("v=").pop() : url.split('/').pop()

        var embedURL = 'https://www.youtube.com/embed/' + videoId;
        videoIFrame.attr('src', embedURL);

        // Define the request
        var reqBody = {
            url: urlFormInput.val()
        };

        // Post the request
        axios.post('/video', reqBody)
            .then(function responseHandler(response) {
                var displayLabels;
                if (response.data.hasOwnProperty('sortedLabels')) {
                    displayLabels = response.data.sortedLabels.slice(startLabelIndex, endLabelIndex); // {0 : "label"}
                }
                else {
                    alert("Response wasn't good");
                    console.log(response.data);
                }
                var listItems = [];
                var label;
                var info;
                for(var i in displayLabels) {
                    label = displayLabels[i];
                    info = response.data.labels[label];
                    // Create the links for each list item.
                    var timeLinks = info.times.map(function(time) {
                        var hms = secondsToHms(time);
                        return '<a class="" onclick="setVideoTime(' + time + ')" href="javascript:void(0)">' +
                            hms + '</a>';
                    });
                    // Capitalize the first letter.
                    label = _.upperFirst(label);
                    var toAdd = '';
                    if (i % 5 == 0) {
                        toAdd += '<div class="col-md-2 col-md-offset-1" style="height:200px;"><h4 style="background-color:' + colors[i] + '; padding: 2px; width: 80%; margin: 0 auto; color: white">' + label + '</h4><div style="overflow-y: scroll; height: 80%; margin-top:5%;"><ul class="list-unstyled">';
                    } else {
                        toAdd += '<div class="col-md-2" style="height:200px;"><h4 style="background-color:' + colors[i] + '; padding: 2px; width: 80%; margin: 0 auto; color: white">' + label + '</h4><div style="overflow-y: scroll; height: 80%; margin-top:5%;"><ul class="list-unstyled">';
                    }
                    
                    for (var j in timeLinks) {
                        toAdd += '<li>' + timeLinks[j] + '</li>';
                    }
                    toAdd += '</ul></div></div>';

                    listItems.push(toAdd);
                }

                // Insert the list items.
                labelsList.html(listItems);
            });

    });

    // Send an initial fake request.
    urlFormInput.val(initialVideoURL);
    urlForm.submit();
});
