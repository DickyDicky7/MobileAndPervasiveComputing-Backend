import * as express from "express";
import axios from "axios";

const router = express.Router();

router.post("/assign", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
        const response = await axios.post("http://pythonserver:27018/assign", req.body);
        res.status(response.status).json(response.data);
    } catch (err) {
        next(err);
    }
});

export default router;
