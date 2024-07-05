import * as express from "express";
import axios from "axios";
import mongoose from "mongoose";

const router = express.Router();

router.post("/delivery/update_status", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.post("http://pythonserver:27018/delivery/update_status", req.body);
    res.json(response.data);
});

export default router;
