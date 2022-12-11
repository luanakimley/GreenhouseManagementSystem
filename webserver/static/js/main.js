let aliveSecond = 0;
let heartbeatRate = 1000;

let myChannel = "greenhouse";
let tempGraphChannel = "temp-graph"
let humGraphChannel = "hum-graph"
let pHGraphChannel = "ph-graph"
let pubnub;

const setupPubNub = () => {
	pubnub = new PubNub({
		subscribeKey: 'sub-c-5832596e-d4b6-4552-b2c0-a28a18fadd40',
		publishKey: 'pub-c-dab1a887-ba42-48aa-b99d-e42ecf3dedb3',
		userId: "e6f98bfc-65f6-11ed-9022-0242ac120002",
		//cipherKey: "myCipherKey"
	});

	const listener = {
		status: (statusEvent) => {
			if (statusEvent.category === "PNConnectedCategory") {
				console.log("Connected to PubNub")
			}
		},
		message: (message) => {
			let msg = message.message;
			console.log(msg)
			if (msg["Soil is"]) {
				document.getElementById("cur-moisture").innerText = msg["Soil is"];
			}

			if (msg["atmos"]) {
				document.getElementById("cur-temp").innerText = msg["atmos"]["temp"] + "°C";
				document.getElementById("cur-humidity").innerText = msg["atmos"]["hum"] + "%";
			}

			if (msg["Ph"]) {
				document.getElementById("cur-ph").innerText = msg["Ph"]
			}

			if (msg["Motion"]) {
				
			}
		},
		presence: (presenceEvent) => {
			// Handle presence
		}
	}
	pubnub.addListener(listener)

	// subscribe to a channel
	pubnub.subscribe({
		channels: [myChannel, tempGraphChannel, humGraphChannel, pHGraphChannel]
	});

	eon.chart({
		pubnub: pubnub,
		channels: [tempGraphChannel], // the pubnub channel for real time data
	  	generate: {           // c3 chart object
			bindto: '#temp-graph',
	  	},
	  	xType: 'custom',
	  	xId: 'datetime'
	});

	eon.chart({
	  	pubnub: pubnub,
	  	channels: [humGraphChannel], // the pubnub channel for real time data
	  	generate: {           // c3 chart object
			bindto: '#humidity-graph',
		  	axis: {
				y: {
					min: 10,
					max: 100
				}
			}
	  	},
	  	xType: 'custom',
	  	xId: 'datetime'
	});

	eon.chart({
		pubnub: pubnub,
		channels: [pHGraphChannel], // the pubnub channel for real time data
		generate: {           // c3 chart object
			bindto: '#ph-graph',
		},
		xType: 'custom',
		xId: 'datetime'
	})
}

window.onload = setupPubNub;
