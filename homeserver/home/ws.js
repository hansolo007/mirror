function wsconnect(){
	var ws = new WebSocket("ws://localhost:8888/ws");
        ws.onopen = function() {
                ws.send("Hello, world");
        };

        ws.onmessage = function (evt) {
        	console.log(evt.data);
			if (evt.data.indexOf('}') != -1){
				var sms = JSON.parse(evt.data.toString());
        		writeToContainer(sms);
			};
		}
}


function writeToContainer(sms_list){

	var MAX_TABLE_ROW = 35;
	var box = document.getElementById('smsbox');
	var table = document.getElementById('sms-table');
	if (!table){
		table = document.createElement('table');
		table.id = 'sms-table';
	}
    var size = table.children.length;
    var list_size = sms_list.length;
	var indexRemove = size + list_size - MAX_TABLE_ROW;
	if (indexRemove > MAX_TABLE_ROW){
		indexRemove = MAX_TABLE_ROW;
	}

	if (indexRemove > -1 && size != 0){
		for (var i=0; i < indexRemove; i++){
		  	table.children[0].remove();
		}

		for (var i=0; i < table.children.length; i++){
			table.children[i].setAttribute('class','smsbox-container-oldText');
		}

	}
	var ind = list_size - MAX_TABLE_ROW;
	if (ind < 0){
		ind = 0;
	}

	for (var i = ind ; i< list_size; i++){
			var tr = document.createElement("tr");
			var name_th = document.createElement("th");
			var text_th = document.createElement("th");
			name_th.setAttribute('class', 'smsbox-container-name');
			tr.setAttribute('class', 'smsbox-container-newText');
			name_th.innerHTML = sms_list[i].name;
			text_th.innerHTML = sms_list[i].text;
			tr.appendChild(name_th);
			tr.appendChild(text_th);
			table.appendChild(tr);
	}
	box.appendChild(table);


}
