
var xhttp = new XMLHttpRequest();
var status = 1;

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
            }
        }

        refreshStatusbar();
        //document.getElementById("statusbar").innerHTML = this.responseText;

        //console.log("CGI Response:", this.responseText)

    }

    // This will happen when timeouts are hit, not seen this yet
    xhttp.ontimeout = function (e) {
        status = -2;
        //console.log("Timeout error");
        refreshStatusbar();
    };

    // This will happen when the server connection is lost
    xhttp.onerror = function (e){
        status = -2;
        //console.log("Unknown error");
        refreshStatusbar();
    };

    var refreshStatusbar = function() {
        document.getElementById("state-2").style.display = (status == -2) ? "block" : "none";
        document.getElementById("state-1").style.display = (status == -1) ? "block" : "none";
        document.getElementById("state0").style.display = (status == 0) ? "block" : "none";
        document.getElementById("state1").style.display = (status == 1) ? "block" : "none";
        document.getElementById("state2").style.display = (status == 2) ? "block" : "none";

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

        //console.log(status);

        refreshStatusbar();


        xhttp.open("GET", "status.txt", true);
        xhttp.timeout = 1000;
        xhttp.send();

    }, 1000);
};


var setStatus = function(statusValue) {
    xhttp.open("POST", "/cgi-bin/status.py", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send("state=".concat(statusValue));
};