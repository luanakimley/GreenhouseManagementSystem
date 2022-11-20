let aliveSecond = 0;
let heartbeatRate = 1000;

let myChannel  ="greenhouse";

function keepAlive()
{
	fetch('/keep_alive')
	.then(response=>{
		if(response.ok){
			let date = new Date();
			aliveSecond = date.getTime();
			return response.json();
		}
		throw new Error("Server offline")
	})
//	.then(responseJson => {
//		if(responseJson.motion == 1){
//			document.getElementById("motion_id").innerHTML = "Motion Detected";
//		}
//		else
//		{
//
//			document.getElementById("motion_id").innerHTML = "No Motion Detected";
//		}
//
//		console.log(responseJson)})
//	.catch(error => console.log(error));
	setTimeout('keepAlive()', heartbeatRate);

}

function time()
{
	let d = new Date();
	let currentSec = d.getTime();
	console.log(currentSec - aliveSecond)
	if(currentSec - aliveSecond > heartbeatRate + 1000)
	{

		document.getElementById("Connection_id").innerHTML = "DEAD";
	}
	else
	{
		document.getElementById("Connection_id").innerHTML = "ALIVE";
	}
	setTimeout('time()', 1000);
}

function handleClick(cb){
	if(cb.checked){
		value = true;
	}else{
		value = false;
	}
	var btnStatus = new Object();
	btnStatus[cb.id] = value;
	var event = new Object();
	event.event = btnStatus;
	publishUpdate(event, myChannel);
}


const pubnub = new PubNub({
subscribeKey:  'sub-c-5832596e-d4b6-4552-b2c0-a28a18fadd40',
publishKey: 'pub-c-dab1a887-ba42-48aa-b99d-e42ecf3dedb3',
uuid : "e6f98bfc-65f6-11ed-9022-0242ac120002"

});

pubnub.addListener({
    status: function(statusEvent){
        if(statusEvent.category === "PNConnectedCategory"){
            console.log("connected to pubnub")
        }
    },
    message: function(message){
        var msg = message.message;
        console.log(msg)
        document.getElementById("motion_id").innerHTML = msg["motion"];
        document.getElementById("temp_id").innerHTML = msg["motion"];
    },
    presence: function(presenceEvent){

    }
})

// paste below "subscribe to a channel" comment
pubnub.subscribe({
    channels: [myChannel]
});

function publishUpdate(data, channel){
    pubnub.publish({
        channel: channel,
        message: data
        },
        function(status, response){
            if(status.error){
                console.log(status)
            }
            else{
                console.log("Message published with timetoken", response.timetoken)
                }
            }
        );
}
