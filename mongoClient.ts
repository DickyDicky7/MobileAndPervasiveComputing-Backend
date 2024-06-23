import mongoose from "mongoose";

const mongoClient = {
    connect: () : void => {
        const            mongoURL = process.env.MONGO_URL || "mongodb://user:pass@localhost:27017/?directConnection=true";
        mongoose.connect(mongoURL, {
        }).then ((   ) => {
            console.log("MONGODB ATLAS CLUSTER CONNECTED!"     );
        }).catch((err) => {
            console.log("MONGODB ATLAS CLUSTER BUG-ERROR:", err);
        });
    },
};

export default mongoClient;




