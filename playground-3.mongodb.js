db.   deliveries.deleteMany({})
db.notifications.deleteMany({})
db.orders       .deleteMany({})

// db.orders.updateMany({}, {$rename: { 'senderInfo.phone': 'senderInfo.phoneNumber', 'receiverInfo.phone': 'receiverInfo.phoneNumber' }})