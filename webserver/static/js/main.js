let myChannel = "greenhouse";
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

			if (msg["temp_range"]) {
				document.getElementById("temp-range").innerText = msg["temp_range"];

				if (!msg["temp_range"].includes("OK")) {
					document.getElementById("temp-box").style.border = "3px solid #fe9693"
				}
			}

			if (msg["Ph"]) {
				document.getElementById("cur-ph").innerText = msg["Ph"]
			}

			if (msg["hum_range"]) {
				document.getElementById("humidity-range").innerText = msg["hum_range"];

				if (!msg["hum_range"].includes("OK")) {
					document.getElementById("humidity-box").style.border = "3px solid #fe9693"
				}
			}

			if (msg["Ph_range"]) {
				document.getElementById("ph-range").innerText = msg["Ph_range"];

				if (!msg["hum_range"].includes("OK")) {
					document.getElementById("ph-box").style.border = "3px solid #fe9693"
				}
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
