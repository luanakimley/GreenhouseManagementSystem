let aliveSecond = 0;
let heartbeatRate = 1000;

let myChannel = "greenhouse";
let pubnub;

const setupPubNub = () => {
	pubnub = new PubNub({
		subscribeKey: 'sub-c-5832596e-d4b6-4552-b2c0-a28a18fadd40',
		publishKey: 'pub-c-dab1a887-ba42-48aa-b99d-e42ecf3dedb3',
		userId: "e6f98bfc-65f6-11ed-9022-0242ac120002",
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
		},
		presence: (presenceEvent) => {
			// Handle presence
		}
	}
	pubnub.addListener(listener)

	// subscribe to a channel
	pubnub.subscribe({
		channels: [myChannel]
	});
}

window.onload = setupPubNub;
