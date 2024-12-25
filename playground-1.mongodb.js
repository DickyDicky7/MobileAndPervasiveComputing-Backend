let shippers = [];
db.users.find().forEach(user => {
                    if (user.role === "shipper") {
    shippers.push(user);
                                                 };
});

function splitArrayIntoGroups(array, n) {
    if (n <= 0) {
        throw new Error("Group size must be greater than zero.");
    }

    const  result = [];
    for (let i = 0; i < array.length;  i += n) {
           result.push( array.slice(i, i +  n));
    }
    return result;
}

let groups = splitArrayIntoGroups(shippers, 5);
// console.log(groups)

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomBool() {
    return Math.random() < 0.5;
}

groups.forEach((  group,   groupIndex) => {
group .forEach((shipper, shipperIndex) => {
        let hub = db.hubs.findOne({ name: `Hub ${groupIndex + 1}` })
        db.staffs.insertOne({
            name              : `SHIPPER ${shipperIndex + 1} HUB ${groupIndex + 1}`,
            age               : getRandomInt( 18,  50)             ,
            gender            : getRandomBool() ? "male" : "female",
            weight            : getRandomInt( 50, 100)             ,
            motorcycleCapacity: getRandomInt(100, 400)             ,
             hubId            :     hub._id,
            userId            : shipper._id,
        })
    })
})
