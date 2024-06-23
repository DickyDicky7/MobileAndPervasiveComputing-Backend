import * as redis from "redis";

const redisUrl    = process.env.REDIS_URL || "redis://localhost:6379";
const redisClient =   redis.createClient({
url : redisUrl    ,
});

redisClient.on("connect", (   ) => {
    console.log("REDIS CONNECTED!"     );
});
redisClient.on( "error" , (err) => {
    console.log("REDIS BUG-ERROR:", err);
});

export default redisClient;




