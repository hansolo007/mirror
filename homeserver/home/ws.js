

function wsconnect(){
	var ws = new WebSocket("ws://localhost:8888/ws");
        ws.onopen = function() {
                ws.send("Hello, world");
        };

        ws.onmessage = function (evt) {
                console.log(evt.data);
		if (evt.data.indexOf('}') != -1){
			var sms = JSON.parse(evt.data.toString());
			var box = document.getElementById('smsbox');
			var table = document.createElement('table');
			for (var i=0; i < sms.length; i++){
				var tr = document.createElement("tr");
				var name_th = document.createElement("th");
				var text_th = document.createElement("th");
				name_th.setAttribute('class','smsbox-container-name')
				text_th.setAttribute('class','smsbox-container-text')
				name_th.innerHTML = sms[i].name;
				text_th.innerHTML = sms[i].text;
				tr.appendChild(name_th);
				tr.appendChild(text_th);
				table.appendChild(tr);
			}
			box.appendChild(table);
		}
        };
}
