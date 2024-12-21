import * as express from "express"               ;
import        axios from         "axios"         ;
import     mongoose from               "mongoose";

const router = express.Router();

router.post("/pay/momo", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post(`http://pythonserver:27018/pay/momo?amount=${req.query.amount}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.post("/pay/momo/check", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post(`http://pythonserver:27018/pay/momo/check?orderId=${req.query.orderId}`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.get("/pay/momo/orderId", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.get(`http://pythonserver:27018/pay/momo/orderId`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

router.post("/pay/momo/check/latest", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post(`http://pythonserver:27018/pay/momo/check/latest`);
        res.json(response.data);
    } catch (err) {
        next(err);
    }
});

export default router;