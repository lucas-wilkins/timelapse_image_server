
var xhttp = new XMLHttpRequest();
var status = 2;

window.onload = function() {
    xhttp.onreadystatechange = function() {

        // Convert string in /status to a number
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText === "active") {
                status = 1;
            } else if (this.responseText == "paused") {
                status = 0;
            } else if (this.responseText == "crashed") {
                status = -1;
            } else if (this.responseText == "starting") {
                status = 3;
            } else if (this.responseText == "pausing") {
                status = 4;
            }
        }

        //console.log(this.responseText);

        refreshStatusbar();

    }

    // This will happen when timeouts are hit, not seen this yet
    xhttp.ontimeout = function (e) {
        status = -2;
        refreshStatusbar();
    };

    // This will happen when the server connection is lost
    xhttp.onerror = function (e){
        status = -2;
        refreshStatusbar();
    };

    var refreshStatusbar = function() {
        document.getElementById("state-2").style.display = (status == -2) ? "block" : "none";
        document.getElementById("state-1").style.display = (status == -1) ? "block" : "none";
        document.getElementById("state0").style.display = (status == 0) ? "block" : "none";
        document.getElementById("state1").style.display = (status == 1) ? "block" : "none";
        document.getElementById("state2").style.display = (status == 2) ? "block" : "none";
        document.getElementById("state3").style.display = (status == 3) ? "block" : "none";
        document.getElementById("state4").style.display = (status == 4) ? "block" : "none";

    };

    // Schedule refresh
    setInterval(function () {

        var divtag = document.getElementById("thumbnail-outer");
        if (status >= 0) {
            divtag.style.display = "block";
            document.getElementById("thumbnail").src = "/thumb-nocache.png";
        } else {
            divtag.style.display = "none";
        }

        refreshStatusbar();

        xhttp.open("GET", "/status.txt", true);
        //xhttp.timeout = 1000;
        xhttp.send();

	//console.log("Sent message!")

    }, 1000);


    var checkStatus = function() {
        xhttp.open("POST", "/cgi-bin/status.py", true);
        xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhttp.send();
    };

    setInterval(checkStatus, 2000);
};


var setStatus = function(statusValue) {


    xhttp.open("POST", "/cgi-bin/status.py", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send("state=".concat(statusValue));

    if (statusValue == 0) {
        status = 4;
    } else if (statusValue == 1) { 
        status = 3;
    }

    refreshStatusbar();

};


