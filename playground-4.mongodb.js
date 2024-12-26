(async () => {
    let cl1  = await db.users.findOne({ username: "cl1"   })
    let cl2  = await db.users.findOne({ username: "cl2"   })
    let hub3 = await db.hubs .findOne({     name: "Hub 3" })

    await db.orders.insertOne({
          senderInfo: {
            userId :  cl1._id                              ,
            name   : "Client 1"                            ,
            address:          "Can Tho, Vietnam"           ,
            phone  :                           "0903089085",
        },
        receiverInfo: {
            userId :  cl2._id                              ,
            name   : "Client 2"                            ,
            address:          "Can Gio, Vietnam"           ,
            phone  :                           "0903089085",
        },
        deliveryInfo: {
            shipmentType: "Document"  ,
            deliveryType: "Standard"  ,
            status      : "pending"   ,
            packageSize :          10 ,
            pickupDate  : "2025-01-01",
            pickupTime  :      "00:00",
            value       :          10 ,
        },
        hubId    :  hub3._id,
        message  : "message",
        payStatus: "pending",
        payWith  : "cash"   ,
    })
})()








