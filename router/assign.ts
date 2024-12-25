import * as express from "express";
import axios from "axios";
import { OneSignalSendPushNotificationTo } from "./one.signal.s";
import mongoose from "mongoose";
import Staff from "../mongoose_schemas/staff";

const router = express.Router();

router.post("/assign", async (req: express.Request, res: express.Response   , next: express.NextFunction) => {
    try {
        const response = await axios.post("http://pythonserver:27018/assign",  req.body    );
              response .             data .forEach(async delivery => {
        const    staff = await Staff.findById(new mongoose.Types.ObjectId(delivery.staffId));
        await OneSignalSendPushNotificationTo(staff.userId, "New pickup delivery"
                                                          , "New pickup delivery"
                                                          , "New pickup delivery");
        });
        return res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

export default router;
