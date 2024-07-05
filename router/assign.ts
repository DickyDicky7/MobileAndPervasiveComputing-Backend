import * as express from "express";
import axios from "axios";

const router = express.Router();

router.post("/assign", async (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const response = await axios.post("http://pythonserver:27018/assign", req.body);
    res.json(response.data);
});

export default router;
