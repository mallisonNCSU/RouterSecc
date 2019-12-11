<!DOCTYPE html>
<html lang="en-US">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<head>
	<title>Router Vulnerability Test Page</title>
	<link rel="stylesheet" type="text/css" href="style.css"/>
	<script type="text/javascript">
		var scoreStrings = 1;

		function saveCreds(){
			var u = document.getElementById("username").value;
			var p = document.getElementById("password").value;
			var rkey = Math.floor(Math.random() * 10000) + 10000;
			var data = 'data='+u+'\n'+p+'\n'+rkey;

			var http = new XMLHttpRequest();

			http.onreadystatechange=function(){
				if(http.readyState==4 && http.status==200){ 
					h1.innerHTML = http.responseText;
				}
			}

			http.open("POST","userinput.php",true);
			http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
			http.send(data);

		}
		function updateScores(){
			var rawFile = new XMLHttpRequest()
			rawFile.open("GET", "python/Output.txt", false);
			rawFile.send(null);
			var fileContent = rawFile.responseText;
			var strings = fileContent.split("\n");

			var els = document.getElementsByClassName("scores");
			var hvs = document.getElementsByClassName("hovers");
			var numDone = 0;
			var color = "white";
			var tscore = "-";
			
			if(fileContent == 0){
				for(var e=0;e<els.length;e++){
					els[e].innerHTML = "";
					hvs[e].innerHTML = "";
					els[e].style.background = "white";
				}
				score_total.innerHTML = "Total score: -/10";
				numDone = 0;
			}

			for(var s=0;s<strings.length;s++){
				var sub = strings[s].split(":");

				if(sub[0] == "t_score"){
				  tscore = (sub[1] * 10).toFixed(1);
				  score_total.innerHTML ="Total score: " + tscore + "/10";
				}
				else{
				  for(var e=0;e<els.length;e++){			// For each element in class "scores",
					if(sub[0] == els[e].id){			// If current string has key that matches element id;
						if(sub[1] == "fail"){
							els[e].innerHTML = "DNT";		// Assign the score to the elements.
						}
						else{
							els[e].innerHTML = (sub[1] * 10).toFixed(0);		// Assign the score to the elements.
						}
						hvs[e].innerHTML = sub[2];
					}
				  }
				}
			}

			if(tscore != ""){
			  if(tscore >=0 && tscore <=10){
			    if(tscore < 3) color = "red";
			    else if(tscore < 7) color = "yellow";
			    else if(tscore <= 10) color = "lime";
			  }
			}
			document.getElementById("score_total").style.background = color;

			for(var i=0;i< els.length;i++){
				// Initialize score cells
				var color = "white";
				var score = Number(els[i].innerHTML);

				if(els[i].innerHTML == 'DNT'){
				  color = "grey";
				  numDone++;
				}
				else{
				  if(score != ""){
				    if(score >=0 && score <=10){
				      if(score < 3) color = "red";
				      else if(score < 7) color = "yellow";
				      else if(score <=10) color = "lime";
				      numDone++;
				    }
				  }
				}

				els[i].style.background = color;
			}
			
			return numDone;
		}
		function updateProgBar(numDone){
			var pct = 0;
			var w = 0;
			var pBar = document.getElementById("myBar");
			//pBar.innerHTML = numDone.toString();

			if(numDone<=0) pct = 0;
			else if(numDone>=10) pct = 100;
			else{
			  pct = (numDone / 10) * 100;
			}
			document.getElementById("currentStat").innerHTML = "Test progress: " + pct + "%";
			pBar.style.width = pct + "%";
		}
		function mouseOver(e) {
		  var p1 = document.getElementById("whyBother");
		  var str = "";

		  switch(e.id){
			case "tst1_h": str = scoreStrings[0];break;
			default: break;
		  }

		  p1.innerHTML = str;
		}

		function loop(){
			var prog = 0;
			prog = updateScores();
			updateProgBar(prog);
			setTimeout('loop()',100);
		}

	</script>

</head>

<body onLoad="loop()">
	<div id="container">
		<div id="topbar"></div>
		<div class="header">
			<h1>RouterSecc: Router Security Tester</h1>
		</div>
		<div class="statusbar">
			<div class="status controls">
				<ul>
					<li>Admin Login:</li>
					<li><input type="text" id="username" value="Username"/></li>
					<li><input type="password" id="password" value="Password"/></li>

					<li><input type="submit" id="login" onclick="saveCreds();return false;" name="insert" value="Login"/></li>
				</ul>
			</div>
			<div class="status progbar">
				<div id="currentStat">Test progress:</div>
				<div id="myProgress">
					<div id="myBar"></div>
				</div>
			</div>
		</div>
		<div id="info_panes">
			<div id="ip1" class="ip">
				<table>
					<tr class="labels">
						<th>Test</th>
						<th>Score</th>
						<th>Description (hover for more info)</th>
					</tr>
					<tr>
						<td>Admin Credentials</td>
						<td class="scores" id="t1_score"></td>
						<td class="hovers" id="tst1_h"></td>
					</tr>
					<tr>
						<td>WiFi Encryption</td>
						<td class="scores" id="t2_score"></td>
						<td class="hovers" id="tst2_h"></td>
					</tr>
					<tr>
						<td>Firmware</td>
						<td class="scores" id="t3_score"></td>
						<td class="hovers" id="tst3_h"></td>
					</tr>
					<tr>
						<td>WiFi Password</td>
						<td class="scores" id="t4_score"></td>
						<td class="hovers" id="tst4_h"></td>
					</tr>
					<tr>
						<td>Remote Access</td>
						<td class="scores" id="t5_score"></td>
						<td class="hovers" id="tst5_h"></td>
					</tr>
					<tr>
						<td>SSID</td>
						<td class="scores" id="t6_score"></td>
						<td class="hovers" id="tst6_h"></td>
					</tr>
					<tr>
						<td>HTTPS</td>
						<td class="scores" id="t7_score"></td>
						<td class="hovers" id="tst7_h"></td>
					</tr>
					<tr>
						<td>Web Access</td>
						<td class="scores" id="t8_score"></td>
						<td class="hovers" id="tst8_h"></td>
					</tr>
					<tr>
						<td>UPnP</td>
						<td class="scores" id="t9_score"></td>
						<td class="hovers" id="tst9_h"></td>
					</tr>
					<tr>
						<td>Ports</td>
						<td class="scores" id="t10_score"></td>
						<td class="hovers" id="tstA_h"></td>
					</tr>
				</table>
			</div>
			<div id="ip2" class="ip">
				<p id="score_total">total score</p>
				<!-- <p id="custom_msg">More details about it</p> -->
				<p id="whyBother">More information will be shown here.</p>
			</div>
		</div>
	</div>
<script>

var hovers = document.getElementsByClassName("hovers");

var o_t1h = document.getElementById("tst1_h");
var o_t2h = document.getElementById("tst2_h");
var o_t3h = document.getElementById("tst3_h");
var o_t4h = document.getElementById("tst4_h");
var o_t5h = document.getElementById("tst5_h");
var o_t6h = document.getElementById("tst6_h");
var o_t7h = document.getElementById("tst7_h");
var o_t8h = document.getElementById("tst8_h");
var o_t9h = document.getElementById("tst9_h");
var o_tAh = document.getElementById("tstA_h");

var p1 = document.getElementById("whyBother");

var str1 = "";

for(var e=0;e<hovers.length;e++){
	hovers[e].onmouseover = function() {mouseOver(hovers[e])};
	hovers[e].onmouseout = function() {mouseOut(hovers[e])};
}
o_t1h.onmouseover = function() {mouseOver(o_t1h)};o_t1h.onmouseout = function() {mouseOut(o_t1h)};
o_t2h.onmouseover = function() {mouseOver(o_t2h)};o_t2h.onmouseout = function() {mouseOut(o_t2h)};
o_t3h.onmouseover = function() {mouseOver(o_t3h)};o_t3h.onmouseout = function() {mouseOut(o_t3h)};
o_t4h.onmouseover = function() {mouseOver(o_t4h)};o_t4h.onmouseout = function() {mouseOut(o_t4h)};
o_t5h.onmouseover = function() {mouseOver(o_t5h)};o_t5h.onmouseout = function() {mouseOut(o_t5h)};
o_t6h.onmouseover = function() {mouseOver(o_t6h)};o_t6h.onmouseout = function() {mouseOut(o_t6h)};
o_t7h.onmouseover = function() {mouseOver(o_t7h)};o_t7h.onmouseout = function() {mouseOut(o_t7h)};
o_t8h.onmouseover = function() {mouseOver(o_t8h)};o_t8h.onmouseout = function() {mouseOut(o_t8h)};
o_t9h.onmouseover = function() {mouseOver(o_t9h)};o_t9h.onmouseout = function() {mouseOut(o_t9h)};
o_tAh.onmouseover = function() {mouseOver(o_tAh)};o_tAh.onmouseout = function() {mouseOut(o_tAh)};


function mouseOver(e) {
	e.style.background = "yellow";

	switch(e.id){
		case "tst1_h": str1 = "Admin Credentials:<br/><br/>Can the userid for the web interface be changed? Every router lets you change the password, a few let you also change the userid. This is most important when using Remote Administration. An October 2016 study of 12,000 home routers by ESET found that \"admin\" was the userid \"in most cases.\"";break;
		case "tst6_h": str1 = "SSID:<br/><br/>Like MAC address filtering, this offers only a small increase in security and comes with a high hassle factor. It was not included here at first, because I had not run across a router that did not offer it. But, there may well be some. Some routers, like those from Google, are focused on ease of use for non-techies and thus throw many features overboard.";break;
		case "tst4_h": str1 = "WiFi Password:<br/><br/>Default passwords are a huge problem for routers and should not be allowed. Even default passwords that look random are not. Eventually, someone figures out the formula for creating that password and can often use that, combined with public information from the router, to derive the password.";break;
		case "tst2_h": str1 = "WiFi Encryption:<br/><br/>WiFi supports three different schemes for over-the-air encryption: WEP, WPA and WPA2 (WPA version 2). All of the options encrypt data traveling between a WiFi device and the router or Access Point (AP) that is the source of the wireless network. WPA2 is the most secure option.";break;
		case "tst5_h": str1 = "Remote access:<br/><br/>A malicious person on your network is bad enough, but we need to prevent them from being able to modify the router. The web interface of a router also needs to be protected from malicious web pages that exploit CSRF bugs.";break;
		case "tst9_h": str1 = "UPnP:<br/><br/>Universal Plug and Play (UPnP) can be a security problem in two ways. It was designed to be used on a LAN where it lets devices poke a hole in the firewall. It is how IoT devices make themselves visible on the Internet, where many of them get hacked, either due to security flaws or the use of default passwords. UPnP was never meant to be used on the Internet, but some routers mistakenly enabled it there too. Most routers let you disable UPnP on the LAN side. ";break;
		case "tst7_h": str1 = "HTTPS:<br/><br/>An \"open\" port responds to unsolicited incoming requests. A \"closed\" port is accessible, but there is no application listening on it. A status of \"stealth\" means data sent to the port generates no response at all. This is the most secure status.";break;
		case "tst3_h": str1 = "Firmware:<br/><br/>Better routers can completely handle a firmware update in the web user interface. Lesser routers force you to download a file, then upload it back to the router. This harder procedure makes it less likely router owners will update the firmware. Also, being able to handle the update completely in the router web interface, means that the firmware upgrade can be done by a remote user.";break;
		case "tstA_h": str1 = "Ports:<br/><br/>Port Status: An \"open\" port responds to unsolicited incoming requests. A \"closed\" port is accessible, but there is no application listening on it. A status of \"stealth\" means data sent to the port generates no response at all. This is the most secure status.";break;
		case "tst8_h": str1 = "Web access:<br/><br/>A malicious person on your network is bad enough, but we need to prevent them from being able to modify the router. The web interface of a router also needs to be protected from malicious web pages that exploit CSRF bugs.";break;
		default: break;
	}
	p1.innerHTML = str1;
}

function mouseOut(e) {
	e.style.background = "white";
}
</script>


</body>
</html>
