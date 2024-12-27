function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomBool() {
    return Math.random() < 0.5;
}

function getRandomCoordinates() {
    const lat = (Math.random() * 180 -  90).toFixed(6);
    const lng = (Math.random() * 360 - 180).toFixed(6);
    return {
        lat: parseFloat(lat),
        lng: parseFloat(lng),
    }
}

const axios = require("axios").default;


(async () => {
    const response0 = await axios.get("http://geodb-free-service.wirefreethought.com/v1/geo/cities?hateoasMode=off")
    const payWithLists = [        "cash","momo", "wallet"   ]
    const clientCursor = (db.users.find({ role : "client" }))
    const clients      = [                                  ]
    while (clientCursor.hasNext()) {
           clients     .   push  (
           clientCursor.   next())
    }
    console.log(clients)
    console.log(clients.length)
    //   let client =  clients[0]
    for (let client of clients) {
        let      otherClients =      clients.filter(otherClient => otherClient._id !== client._id)
        for (let otherClient of otherClients) {

            



            const response1 = await axios.get(`http://geodb-free-service.wirefreethought.com/v1/geo/cities?limit=1&offset=${getRandomInt(0, response0.data.metadata.totalCount - 1)}&hateoasMode=off`
            );
            const response2 = await axios.get(`http://geodb-free-service.wirefreethought.com/v1/geo/cities?limit=1&offset=${getRandomInt(0, response0.data.metadata.totalCount - 1)}&hateoasMode=off`
            );
            const address1 = `${response1.data.data[0].city}, ${response1.data.data[0].country}`;
            const address2 = `${response2.data.data[0].city}, ${response2.data.data[0].country}`;

            // const response3 = await axios.get("https://waseminarcnpm2.azurewebsites.net/protected/hub/near", {
            //     params: {
            //         address: address1,
            //     }
            // })

            let rn = getRandomInt(1, 4)
            let hu = await db.hubs.findOne({ name: `Hub ${rn}` })

            await db.orders.insertOne({
                  senderInfo: {
                    userId :      client._id     ,
                    name   :      client.username,
                    address:             address1,
                    phoneNumber    : "0903089085",
                    _id: ObjectId(),
                    __v: 0         ,
                },
                receiverInfo: {
                    userId : otherClient._id     ,
                    name   : otherClient.username,
                    address:             address2,
                    phoneNumber    : "0903089085",
                    _id: ObjectId(),
                    __v: 0         ,
                },
                deliveryInfo: {
                    shipmentType: "Document"           ,
                    deliveryType: "Standard"           ,
                    status      :             "pending",
                    packageSize : getRandomInt(10, 100),
                    pickupDate  : "2025-01-01"         ,
                    pickupTime  :      "00:00"         ,
                    value       : getRandomInt(10, 100),
                    _id: ObjectId(),
                    __v: 0         ,
                },
                hubId    :  hu._id           ,
                message  : "message"         ,
                payStatus: "pending"         ,
                payWith  : payWithLists[getRandomInt(0, 2)],
                __v: 0,
            })
        }
    }
})()








