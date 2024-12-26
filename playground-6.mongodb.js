(async () => {
    const hub1 = await db.hubs.findOne({ name: "Hub 1" })
    const hub2 = await db.hubs.findOne({ name: "Hub 2" })
    const hub3 = await db.hubs.findOne({ name: "Hub 3" })
    const hub4 = await db.hubs.findOne({ name: "Hub 4" })

    const coordinator1 = await db.users.findOne({ username: "co1" })
    const coordinator2 = await db.users.findOne({ username: "co2" })
    const coordinator3 = await db.users.findOne({ username: "co3" })
    const coordinator4 = await db.users.findOne({ username: "co4" })

    await db.coordinators.insertOne({
        coordinatorUserId: coordinator1._id,
        coordinator_HubId:         hub1._id,
        __v:0
    })
    
    await db.coordinators.insertOne({
        coordinatorUserId: coordinator2._id,
        coordinator_HubId:         hub2._id,
        __v:0
    })

    await db.coordinators.insertOne({
        coordinatorUserId: coordinator3._id,
        coordinator_HubId:         hub3._id,
        __v:0
    })

    await db.coordinators.insertOne({
        coordinatorUserId: coordinator4._id,
        coordinator_HubId:         hub4._id,
        __v:0
    })
})()