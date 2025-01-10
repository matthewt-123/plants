
/*************************
 WEBSOCKET SETUP
**************************/
let chatSocket = 0;
if (window.location.protocol == "https:") {
    chatSocket = new WebSocket(
        'wss://'
        + window.location.host
        + '/ws/sensors'
    );
} else {
    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/sensors'
    );
}


chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(`${data['module']}: ${data['content']}`)
    switch(data['module'])
    {
        case 'humidity':
            document.getElementById('humidity').innerHTML = data['content'];
        case 'temperature':
            document.getElementById('temperature').innerHTML = data['content'];
        case 'light':
            document.getElementById('light').innerHTML = data['content'];    
    }
};
chatSocket.onerror = function(evt) {
    console.log(evt)
}
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
    console.error(e)
    self.close(e)
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/sensors'
    );
};
